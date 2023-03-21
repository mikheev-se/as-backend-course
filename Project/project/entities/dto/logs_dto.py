from datetime import datetime
from pydantic import BaseModel
from project.entities.dto.user_dto import ResponseUserDto
from project.entities.log_entity import valid_actions


class AddLogDto(BaseModel):
    action: valid_actions
    invoked_by: int


class ResponseLogDto(BaseModel):
    id: int
    action: valid_actions
    invoked_by: int
    invoked_at: datetime
    invoker: ResponseUserDto

    class Config:
        orm_mode = True
