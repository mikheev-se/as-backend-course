from fastapi import HTTPException, status
from project.service.operations_service import OperationsService
from project.service.products_service import ProductsService
from project.service.tanks_service import TanksService
from project.service.users_service import UsersService


def check_for_item(item_id: int,
                   service: TanksService | OperationsService | ProductsService | UsersService,
                   detail: str | None):
    """
    Вспомогательная функция для проверки на существование объекта в базе данных
    """
    item = service.get(item_id)
    error_msg = detail if detail else f'Объект с id={item_id} не найден!'
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=error_msg)
    return item
