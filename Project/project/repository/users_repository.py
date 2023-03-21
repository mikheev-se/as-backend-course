from fastapi import Depends
from sqlalchemy.orm import Session
from project.db.db import get_session
from project.entities.dto.user_dto import CreateUserDto, RegistrationDto, UpdateUserDto
from project.entities.user_entity import User
from project.service.jwt_service import JwtService


class UsersRepository:
    def __init__(self, session: Session = Depends(get_session)) -> None:
        self.connection = session

    def get_all(self) -> list[User]:
        users = (self.connection
                 .query(User)
                 .order_by(User.id)
                 .all())

        return users

    def get_by_id(self, id: int) -> User:
        user = (self.connection
                .query(User)
                .filter(User.id == id)
                .first())

        return user

    def get_by_username(self, username: str) -> User:
        user = (self.connection
                .query(User)
                .filter(User.username == username)
                .first())

        return user

    def create(self, dto: CreateUserDto, requester_id: int) -> User:
        user = User(
            username=dto.username,
            password_hashed=JwtService.hash_password(dto.password),
            role=dto.role,
            created_by=requester_id,
            updated_by=requester_id,
        )
        self.connection.add(user)
        self.connection.commit()
        return user

    def update(self, id: int, dto: UpdateUserDto, requester_id: int) -> User:
        user = self.get_by_id(id)
        for field, value in dto:
            if value:
                if field != 'password':
                    setattr(user, field, value)
                else:
                    setattr(user, field, JwtService.hash_password(value))
        user.updated_by = requester_id
        self.connection.commit()
        return user

    def delete(self, id: int):
        user = self.get_by_id(id)
        self.connection.delete(user)
        self.connection.commit()

    def register(self, dto: RegistrationDto) -> User:
        user = User(
            username=dto.username,
            password_hashed=dto.password
        )
        self.connection.add(user)
        self.connection.commit()

        user.created_by = user.id
        user.updated_by = user.id

        self.connection.commit()
        return user
