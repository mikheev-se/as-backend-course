from datetime import datetime
from fastapi import Depends
from sqlalchemy.orm import Session
from project.db.db import get_session
from project.entities.dto.logs_dto import AddLogDto
from project.entities.log_entity import Log


class LogsRepository:
    def __init__(self, session: Session = Depends(get_session)) -> None:
        self.connection = session

    def get_all(self) -> list[Log]:
        logs = (self.connection
                .query(Log)
                .order_by(Log.id.desc())
                .all())

        return logs

    def get_by_id(self, id: int) -> Log:
        log = (self.connection
               .query(Log)
               .filter(Log.id == id)
               .first())

        return log

    def get_interval(self, start: datetime, end: datetime) -> list[Log]:
        logs = (self.connection
                .query(Log)
                .filter((Log.invoked_at > start) & (Log.invoked_at < end))
                .order_by(Log.id.desc())
                .all())

        return logs

    def get_by_invoker_id(self, invoker_id: int) -> list[Log]:
        logs = (self.connection
                .query(Log)
                .filter(Log.invoked_by == invoker_id)
                .order_by(Log.id.desc())
                .all())

        return logs

    def add(self, dto: AddLogDto) -> Log:
        log = Log(**dto.dict())
        self.connection.add(log)
        self.connection.commit()
