from datetime import datetime
from pydantic import BaseModel
from project.models.dto.products_dto import ResponseProductDto
from project.models.dto.users_dto import ResponseUserDto
from project.utils.all_optional import AllOptional


class CreateTankDto(BaseModel):
    name: str
    max_capacity: float
    current_capacity: float
    product_id: int


class UpdateTankDto(CreateTankDto, metaclass=AllOptional):
    pass


class ResponseTankDto(BaseModel):
    id: int
    name: str
    max_capacity: float
    current_capacity: float
    product_id: int
    product: ResponseProductDto
    created_at: datetime
    created_by: int
    creator: ResponseUserDto
    modified_at: datetime
    modified_by: int
    modifier: ResponseUserDto

    class Config:
        orm_mode = True
