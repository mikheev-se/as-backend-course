from fastapi import APIRouter, Depends, status
from project.api.utils.check_for_item import check_for_item
from project.models.dto.products_dto import CreateProductDto, ResponseProductDto, UpdateProductDto
from project.models.product import Product
from project.service.products_service import ProductsService
from project.service.utils.jwt_service import JwtService

products_router = APIRouter(
    prefix='/products',
    tags=['products']
)


@products_router.get('/', response_model=list[ResponseProductDto], status_code=status.HTTP_200_OK, name='Получить все продукты')
def all(service: ProductsService = Depends(), user_id: int = Depends(JwtService.get_current_user_id)):
    """
    Возвращает все продукты
    """
    return service.all()


@products_router.get('/{id}', response_model=ResponseProductDto, status_code=status.HTTP_200_OK, name='Получить продукт с заданным id')
def get(id: int, service: ProductsService = Depends(), user_id: int = Depends(JwtService.get_current_user_id)):
    """
    Возвращает продукт с заданным идентификатором
    """
    return check_for_product(id, service)


@products_router.post('/', response_model=ResponseProductDto, status_code=status.HTTP_201_CREATED, name='Добавить продукт')
def add(dto: CreateProductDto, service: ProductsService = Depends(), user_id: int = Depends(JwtService.get_current_user_id)):
    """
    Добавляет в базу данных продукт с заданными параметрами
    """
    return service.add(user_id, dto)


@products_router.patch('/{id}', response_model=ResponseProductDto, status_code=status.HTTP_200_OK, name='Изменить информацию о продукте')
def update(id: int, dto: UpdateProductDto, service: ProductsService = Depends(), user_id: int = Depends(JwtService.get_current_user_id)):
    """
    Обновляет параметры продукта в соответствии с теми, которые были переданы в запросе
    """
    check_for_product(id, service)
    return service.update(id, user_id, dto)


@products_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, name='Удалить продукт')
def delete(id: int, service: ProductsService = Depends(), user_id: int = Depends(JwtService.get_current_user_id)):
    """
    Удаляет продукт с заданным id
    """
    check_for_product(id, service)
    service.delete(id)


def check_for_product(product_id: int, products_service: ProductsService) -> Product:
    return check_for_item(product_id, products_service, f'Продукт с id={product_id} не найден!')
