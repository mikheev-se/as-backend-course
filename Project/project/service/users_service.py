from fastapi import Depends, HTTPException, status
from project.entities.dto.user_dto import CreateUserDto, RegistrationDto, UpdateUserDto
from project.entities.user_entity import User
from project.entities.utils.jwt_token import JwtToken
from project.repository.users_repository import UsersRepository
from project.service.jwt_service import JwtService


class UsersService:
    def __init__(self, repo: UsersRepository = Depends()) -> None:
        self.repo = repo

    def get_all(self) -> list[User]:
        return self.repo.get_all()

    def get_by_id(self, id: int) -> User:
        return self.repo.get_by_id(id)

    def get_by_username(self, username: str) -> User:
        return self.repo.get_by_username(username)

    def create(self, dto: CreateUserDto, requester_id: int) -> User:
        if self.get_by_username(dto.username):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail='Пользователь с таким именем уже существует')
        return self.repo.create(dto, requester_id)

    def update(self, id: int, dto: UpdateUserDto, requester_id: int) -> User:
        if not self.get_by_id(id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Пользователь с {id=} не существует!')
        return self.repo.update(id, dto, requester_id)

    def delete(self, id: int):
        self.repo.delete(id)

    def register(self, dto: RegistrationDto) -> User:
        if self.get_by_username(dto.username):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail='Пользователь с таким именем уже существует')

        dto_hashed = dto.copy()
        dto_hashed.password = JwtService.hash_password(dto.password)
        return self.repo.register(dto_hashed)

    def authorize(self, username: str, password: str) -> JwtToken:
        user = self.get_by_username(username)

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=f'Пользователя с {username=} не существует')
        if not JwtService.check_password(password, user.password_hashed):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=f'Неверный пароль')

        return JwtService.create_token(user.id, user.role)
