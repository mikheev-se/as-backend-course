from datetime import datetime
from pydantic import BaseModel
from project.models.dto.users_dto import ResponseUserDto
from project.utils.all_optional import AllOptional


class CreateProductDto(BaseModel):
    name: str


class UpdateProductDto(CreateProductDto, metaclass=AllOptional):
    pass


class ResponseProductDto(BaseModel):
    id: int
    name: str
    created_at: datetime
    created_by: int
    creator: ResponseUserDto
    modified_at: datetime
    modified_by: int
    modifier: ResponseUserDto

    class Config:
        orm_mode = True
