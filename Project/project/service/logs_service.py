from datetime import datetime
from fastapi import Depends
from project.entities.dto.logs_dto import AddLogDto
from project.repository.logs_repository import LogsRepository


class LogsService:
    def __init__(self, repo: LogsRepository = Depends()) -> None:
        self.repo = repo

    def get_all(self):
        return self.repo.get_all()

    def get_by_id(self, id: int):
        return self.repo.get_by_id(id)

    def get_interval(self, start: datetime | None, end: datetime | None):
        if not start:
            start = datetime.min
        if not end:
            end = datetime.now()

        return self.repo.get_interval(start, end)

    def get_by_invoker_id(self, invoker_id: int):
        return self.repo.get_by_invoker_id(invoker_id)

    def add(self, dto: AddLogDto):
        return self.repo.add(dto)
