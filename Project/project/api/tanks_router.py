from fastapi import APIRouter, Depends, status
from project.api.utils.check_for_item import check_for_item
from project.models.dto.tanks_dto import CreateTankDto, ResponseTankDto, UpdateTankDto
from project.models.tank import Tank
from project.service.tanks_service import TanksService
from project.service.utils.jwt_service import JwtService

tanks_router = APIRouter(
    prefix='/tanks',
    tags=['tanks']
)


@tanks_router.get('/', response_model=list[ResponseTankDto], status_code=status.HTTP_200_OK, name='Получить все резервуары')
def all(service: TanksService = Depends(), user_id: int = Depends(JwtService.get_current_user_id)):
    """
    Возвращает все резервуары, их вместимость и связанные с ними продукты
    """
    return service.all()


@tanks_router.get('/{id}', response_model=ResponseTankDto, status_code=status.HTTP_200_OK, name='Получить резервуар с заданным id')
def get(id: int, service: TanksService = Depends(), user_id: int = Depends(JwtService.get_current_user_id)):
    """
    Возвращает резервуар с заданным идентификатором, его вместимость и связанный с ним продукт
    """
    return check_for_tank(id, service)

# почему get?


@tanks_router.get('', response_model=ResponseTankDto, status_code=status.HTTP_200_OK, name='Обновить current_capacity резервуара')
def update_capacity(id: int, current_capacity: float, service: TanksService = Depends(), user_id: int = Depends(JwtService.get_current_user_id)):
    """
    Обновляет значение current_capacity резервуара и возвращает резервуар
    """
    check_for_tank(id, service)
    dto = UpdateTankDto(
        current_capacity=current_capacity
    )
    return service.update(id, user_id, dto)


@tanks_router.post('/', response_model=ResponseTankDto, status_code=status.HTTP_201_CREATED, name='Добавить резервуар')
def add(dto: CreateTankDto, service: TanksService = Depends(), user_id: int = Depends(JwtService.get_current_user_id)):
    """
    Добавляет в базу данных резервуар с заданными параметрами
    """
    return service.add(user_id, dto)


@tanks_router.patch('/{id}', response_model=ResponseTankDto, status_code=status.HTTP_200_OK, name='Изменить информацию о резервуаре')
def update(id: int, dto: UpdateTankDto, service: TanksService = Depends(), user_id: int = Depends(JwtService.get_current_user_id)):
    """
    Заменяет значения резервуара в тех полях, которые были переданы в запросе
    """
    check_for_tank(id, service)
    return service.update(id, user_id, dto)


@tanks_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, name='Удалить резервуар')
def delete(id: int, service: TanksService = Depends(), user_id: int = Depends(JwtService.get_current_user_id)):
    """
    Удаляет резервуар с заданным id
    """
    check_for_tank(id, service)
    service.delete(id)


def check_for_tank(tank_id: int, tanks_service: TanksService) -> Tank:
    return check_for_item(tank_id, tanks_service, f'Резервуар с id={tank_id} не найден!')
