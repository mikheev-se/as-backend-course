from datetime import datetime
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from project.db.db import get_session
from project.models.dto.operations_dto import CreateOperationDto, UpdateOperationDto
from project.models.operation import Operation


class OperationsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def all(self) -> list[Operation]:
        operations = (
            self.session
            .query(Operation)
            .order_by(
                Operation.id.desc()
            )
            .all()
        )

        return operations

    def get(self, operation_id: int) -> Operation:
        operation = (
            self.session
            .query(Operation)
            .filter(Operation.id == operation_id)
            .first()
        )

        return operation

    def get_by_tank(self, tank_id: int) -> list[Operation]:
        operations = (
            self.session
            .query(Operation)
            .filter(Operation.tank_id == tank_id)
            .order_by(
                Operation.id.desc()
            )
            .all()
        )

        return operations

    def get_report(self,
                   tank_id: int,
                   product_id: int,
                   date_start: datetime,
                   date_end: datetime) -> list[Operation]:
        operations = (
            self.session
            .query(Operation)
            .filter(
                Operation.tank_id == tank_id,
                Operation.product_id == product_id,
                Operation.date_start < date_start,
                Operation.date_end > date_end
            )
            .order_by(
                Operation.id.desc()
            )
            .all()
        )

        if not operations:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Не найдено операций соответствующих заданным параметрам')

        return operations

    def add(self, user_id: int, dto: CreateOperationDto) -> Operation:
        operation = Operation(**dto.dict())
        operation.created_by = user_id
        operation.modified_by = user_id
        self.session.add(operation)
        self.session.commit()
        return operation

    def update(self, operation_id: int, user_id: int, dto: UpdateOperationDto) -> Operation:
        operation = self.get(operation_id)
        for field, value in dto:
            if value:
                setattr(operation, field, value)
        operation.modified_by = user_id
        self.session.commit()
        return operation

    def delete(self, operation_id: int):
        operation = self.get(operation_id)
        self.session.delete(operation)
        self.session.commit()
