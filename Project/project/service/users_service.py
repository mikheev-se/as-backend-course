from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from project.core.settings import settings
from project.db.db import get_session
from project.models.dto.users_dto import CreateUserDto, RegistrationDto, UpdateUserDto
from project.models.user import User
from project.models.utils.jwt_token import JwtToken
from project.service.utils.jwt_service import JwtService


class UsersService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def all(self) -> list[User]:
        users = (
            self.session
            .query(User)
            .order_by(
                User.id.desc()
            )
            .all()
        )

        return users

    def get(self, id: int) -> User:
        user = (
            self.session
            .query(User)
            .filter(User.id == id)
            .first()
        )

        return user

    def get_by_name(self, username: str) -> User:
        user = (
            self.session
            .query(User)
            .filter(User.username == username)
            .first()
        )

        return user

    def add(self, user_id: int, dto: CreateUserDto) -> User:
        if self.get_by_name(dto.username):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail='Пользователь с таким именем уже существует')
        user = User(
            username=dto.username,
            password_hashed=JwtService.hash_password(dto.password),
            role=dto.role,
            created_by=user_id,
            modified_by=user_id
        )
        self.session.add(user)
        self.session.commit()
        return user

    def register(self, dto: RegistrationDto) -> User:
        if self.get_by_name(dto.username):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail='Пользователь с таким именем уже существует')
        user = User(
            username=dto.username,
            password_hashed=JwtService.hash_password(dto.password)
        )
        self.session.add(user)
        self.session.commit()

        # костыль))))
        user.created_by = user.id
        user.modified_by = user.id

        self.session.commit()
        return user

    def authorize(self, username: str, password: str) -> JwtToken:
        user = self.get_by_name(username)

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=f'Пользователя с {username=} не существует')
        if not JwtService.check_password(password, user.password_hashed):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=f'Неверный пароль')

        return JwtService.create_token(user.id, user.role)

    def update(self, id: int, user_id: int, dto: UpdateUserDto) -> User:
        user = self.get(id)
        for field, value in dto:
            if value:
                if field != 'password':
                    setattr(user, field, value)
                else:
                    setattr(user, field, JwtService.hash_password(value))
        user.modified_by = user_id
        self.session.commit()
        return user

    def delete(self, id: int):
        user = self.get(id)
        self.session.delete(user)
        self.session.commit()

    def get_admins(self) -> list[User]:
        admins = (
            self.session
            .query(User)
            .filter(User.role == 'admin')
            .order_by(
                User.id.desc()
            )
            .all()
        )

        return admins

    def create_admin(self) -> User:
        if not self.get_admins():
            print('No admins detected. creating...')
            admin_dto = CreateUserDto(
                username=settings.username,
                password=settings.password,
                role='admin'
            )
            admin = self.add(None, admin_dto)
            admin.created_by = admin.id
            admin.modified_by = admin.id
            self.session.commit()
        else:
            print('Admins detected')
