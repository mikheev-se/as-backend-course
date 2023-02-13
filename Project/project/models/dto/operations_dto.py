from datetime import datetime
from pydantic import BaseModel
from project.models.dto.products_dto import ResponseProductDto
from project.models.dto.tanks_dto import ResponseTankDto
from project.models.dto.users_dto import ResponseUserDto
from project.utils.all_optional import AllOptional


class CreateOperationDto(BaseModel):
    mass: float
    date_start: datetime
    date_end: datetime
    tank_id: int
    product_id: int


class UpdateOperationDto(CreateOperationDto, metaclass=AllOptional):
    pass


class ResponseOperationDto(BaseModel):
    id: int
    mass: float
    date_start: datetime
    date_end: datetime
    tank_id: int
    tank: ResponseTankDto
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
