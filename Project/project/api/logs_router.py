from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from project.entities.dto.logs_dto import ResponseLogDto
from project.entities.dto.user_dto import valid_roles
from project.entities.log_entity import Log
from project.service.jwt_service import JwtService
from project.service.logs_service import LogsService

logs_router = APIRouter(
    prefix='/logs',
    tags=['logs']
)


@logs_router.get('/', response_model=list[ResponseLogDto], status_code=status.HTTP_200_OK, name='Получить всю историю операций')
def get_all(logs_service: LogsService = Depends(),
            requester_id: int = Depends(JwtService.get_current_user_id),
            requester_role: valid_roles = Depends(JwtService.check_if_admin)):
    """
    Возвращает все операции
    """
    return logs_service.get_all()


@logs_router.get('/interval/', response_model=list[ResponseLogDto], status_code=status.HTTP_200_OK, name='Получить историю операций за определённый период')
def get_interval(start: datetime | None = None, end: datetime | None = None, logs_service: LogsService = Depends(),
                 requester_id: int = Depends(JwtService.get_current_user_id),
                 requester_role: valid_roles = Depends(JwtService.check_if_admin)):
    """
    Возвращает все операции в заданном интервале
    """
    return logs_service.get_interval(start, end)


@logs_router.get('/invoker/', response_model=list[ResponseLogDto], status_code=status.HTTP_200_OK, name='Получить историю операций определённого пользователя')
def get_by_invoker_id(invoker_id: int, logs_service: LogsService = Depends(),
                      requester_id: int = Depends(
                          JwtService.get_current_user_id),
                      requester_role: valid_roles = Depends(JwtService.check_if_admin)):
    """
    Возвращает все операции, совершённые определённым пользователем
    """
    return logs_service.get_by_invoker_id(invoker_id)


@logs_router.get('/{id}', response_model=ResponseLogDto, status_code=status.HTTP_200_OK, name='Получить операцию по заданному id')
def get_by_id(id: int, logs_service: LogsService = Depends(),
              requester_id: int = Depends(JwtService.get_current_user_id),
              requester_role: valid_roles = Depends(JwtService.check_if_admin)):
    """
    Возвращает операцию с заданным id
    """
    return check_for_log(id, logs_service)


def check_for_log(id: int, logs_service: LogsService) -> Log:
    user = logs_service.get_by_id(id)
    error_msg = f'Операция с {id=} не найдена!'
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=error_msg)
    return user
