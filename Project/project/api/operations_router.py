from datetime import datetime
from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse
from project.api.tanks_router import check_for_tank
from project.api.utils.check_for_item import check_for_item
from project.models.dto.operations_dto import CreateOperationDto, ResponseOperationDto, UpdateOperationDto
from project.models.operation import Operation
from project.service.files_service import FilesService
from project.service.operations_service import OperationsService
from project.service.tanks_service import TanksService
from project.service.utils.jwt_service import JwtService

operations_router = APIRouter(
    prefix='/operations',
    tags=['operations']
)


@operations_router.get('/', response_model=list[ResponseOperationDto], status_code=status.HTTP_200_OK, name='Получить все операции')
def all(service: OperationsService = Depends(), user_id: int = Depends(JwtService.get_current_user_id)):
    """
    Возвращает данные о всех операциях, а также связанных с ними резервуарах и продуктах
    """
    return service.all()


@operations_router.get('/{id}', response_model=ResponseOperationDto, status_code=status.HTTP_200_OK, name='Получить операцию с заданным id')
def get(id: int, service: OperationsService = Depends(), user_id: int = Depends(JwtService.get_current_user_id)):
    """
    Возвращает данные об операции, а также связанных с ней резервуаром и продукте
    """
    return check_for_operation(id, service)


@operations_router.get('', response_model=list[ResponseOperationDto], status_code=status.HTTP_200_OK, name='Получить операции с заданным id резервуара')
def get_by_tank(tank_id: int,
                operations_service: OperationsService = Depends(),
                tanks_service: TanksService = Depends(),
                user_id: int = Depends(JwtService.get_current_user_id)):
    """
    Возвращает данные об операцииях, связанных с данным резервуаром
    """
    check_for_tank(tank_id, tanks_service)
    return operations_service.get_by_tank(tank_id)


@operations_router.get('/report/', status_code=status.HTTP_200_OK, name='Получить операции с заданным id резервуара')
def get_report(tank_id: int,
               product_id: int,
               date_start: datetime,
               date_end: datetime,
               operations_service: OperationsService = Depends(),
               files_service: FilesService = Depends(),
               user_id: int = Depends(JwtService.get_current_user_id)):
    """
    Возвращает данные об операцииях, связанных с данным резервуаром
    """
    report = operations_service.get_report(
        tank_id, product_id, date_start, date_end
    )
    report_stream = files_service.download(report)
    return StreamingResponse(report_stream, media_type='text/csv', headers={
        'Content-Disposition': f'attachment; filename=report_{datetime.utcnow()}.csv'
    })


@operations_router.post('/', response_model=ResponseOperationDto, status_code=status.HTTP_201_CREATED, name='Добавить операцию')
def add(dto: CreateOperationDto, service: OperationsService = Depends(), user_id: int = Depends(JwtService.get_current_user_id)):
    """
    Добавляет в базу данных операцию с заданными полями
    """
    return service.add(user_id, dto)


@operations_router.patch('/{id}', response_model=ResponseOperationDto, status_code=status.HTTP_200_OK, name='Изменить информацию об операции')
def update(id: int, dto: UpdateOperationDto, service: OperationsService = Depends(), user_id: int = Depends(JwtService.get_current_user_id)):
    """
    Заменяет параметры операции в тех полях, которые были переданы в запросе
    """
    check_for_operation(id, service)
    return service.update(id, user_id, dto)


@operations_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, name='Удалить операцию')
def delete(id: int, service: OperationsService = Depends(), user_id: int = Depends(JwtService.get_current_user_id)):
    """
    Удаляет операцию с заданным id
    """
    check_for_operation(id, service)
    service.delete(id)


def check_for_operation(operation_id: int, operations_service: OperationsService) -> Operation:
    return check_for_item(operation_id, operations_service, f'Операция с id={operation_id} не найдена!')
