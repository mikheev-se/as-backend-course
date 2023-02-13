from fastapi import Depends
from sqlalchemy.orm import Session

from project.db.db import get_session
from project.models.dto.tanks_dto import CreateTankDto, UpdateTankDto
from project.models.tank import Tank


class TanksService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def all(self) -> list[Tank]:
        tanks = (
            self.session
            .query(Tank)
            .order_by(
                Tank.id.desc()
            )
            .all()
        )

        return tanks

    def get(self, tank_id: int) -> Tank:
        tank = (
            self.session
            .query(Tank)
            .filter(Tank.id == tank_id)
            .first()
        )

        return tank

    def add(self, user_id: int, dto: CreateTankDto) -> Tank:
        tank = Tank(**dto.dict())
        tank.created_by = user_id
        tank.modified_by = user_id
        self.session.add(tank)
        self.session.commit()
        return tank

    def update(self, tank_id: int, user_id: int, dto: UpdateTankDto) -> Tank:
        tank = self.get(tank_id)
        for field, value in dto:
            if value:
                setattr(tank, field, value)
        tank.modified_by = user_id
        self.session.commit()
        return tank

    def delete(self, tank_id: int):
        tank = self.get(tank_id)
        self.session.delete(tank)
        self.session.commit()
