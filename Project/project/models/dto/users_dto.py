from datetime import datetime
from pydantic import BaseModel
from project.utils.all_optional import AllOptional
from project.models.roles import valid_roles


class RegistrationDto(BaseModel):
    username: str
    password: str


class CreateUserDto(RegistrationDto):
    role: valid_roles


class UpdateUserDto(CreateUserDto, metaclass=AllOptional):
    pass


class UserRef(BaseModel):
    id: int
    username: str
    role: valid_roles
    created_at: datetime
    created_by: int | None
    modified_at: datetime
    modified_by: int | None

    class Config:
        orm_mode = True


class ResponseUserDto(UserRef):
    creator: UserRef
    modifier: UserRef

    class Config:
        orm_mode = True
