from datetime import datetime
from pydantic import BaseModel
from project.entities.user_entity import valid_roles


class Payload(BaseModel):
    iat: datetime
    exp: datetime
    sub: str
    role: valid_roles
