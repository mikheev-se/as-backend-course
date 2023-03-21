from datetime import datetime
from pydantic import BaseModel
from project.entities.user_entity import valid_roles
from project.utils.AllOptional import AllOptional


class CreateUserDto(BaseModel):
    username: str
    password: str
    role: valid_roles | None


class UpdateUserDto(CreateUserDto, metaclass=AllOptional):
    pass


class RegistrationDto(BaseModel):
    username: str
    password: str


class UserRef(BaseModel):
    id: int
    username: str
    role: valid_roles
    created_by: int | None
    created_at: datetime | None
    updated_by: int | None
    updated_at: datetime | None

    class Config:
        orm_mode = True


class ResponseUserDto(UserRef, BaseModel):
    creator: UserRef | None
    updater: UserRef | None

    class Config:
        orm_mode = True
