from fastapi import APIRouter, Depends, status
from project.api.utils.check_for_item import check_for_item
from project.models.dto.users_dto import CreateUserDto, RegistrationDto, ResponseUserDto, UpdateUserDto
from project.models.user import User
from project.service.users_service import UsersService
from fastapi.security import OAuth2PasswordRequestForm
from project.service.utils.jwt_service import JwtService
from project.models.roles import valid_roles

users_router = APIRouter(
    prefix='/users',
    tags=['users']
)


@users_router.get('/', response_model=list[ResponseUserDto], status_code=status.HTTP_200_OK, name='Получить всех пользователей')
def all(service: UsersService = Depends(),
        user_id: int = Depends(JwtService.get_current_user_id),
        user_role: valid_roles = Depends(JwtService.check_if_admin)):
    """
    Возвращает всех пользоваталей
    """
    return service.all()


@users_router.get('/{id}', response_model=ResponseUserDto, status_code=status.HTTP_200_OK, name='Получить пользователя с заданным id')
def get(id: int, service: UsersService = Depends(),
        user_id: int = Depends(JwtService.get_current_user_id),
        user_role: valid_roles = Depends(JwtService.check_if_admin)):
    """
    Возвращает пользователя с заданным идентификатором
    """
    return check_for_user(id, service)


@users_router.post('/', response_model=ResponseUserDto, status_code=status.HTTP_201_CREATED, name='Добавить пользователя')
def add(dto: CreateUserDto, service: UsersService = Depends(),
        user_id: int = Depends(JwtService.get_current_user_id),
        user_role: valid_roles = Depends(JwtService.check_if_admin)):
    """
    Создаёт в базе данных нового пользователя
    """
    return service.add(user_id, dto)


@users_router.post('/register', response_model=ResponseUserDto, status_code=status.HTTP_201_CREATED, name='Регистрация')
def register(dto: RegistrationDto, service: UsersService = Depends()):
    """
    Регистрирует пользователя с заданными именем и паролем
    """
    return service.register(dto)


@users_router.post('/authorize', status_code=status.HTTP_200_OK, name='Авторизация')
def authorize(auth_schema: OAuth2PasswordRequestForm = Depends(), users_service: UsersService = Depends()):
    """
    Авторизация с заданными логином и паролем
    """
    return users_service.authorize(auth_schema.username, auth_schema.password)


@users_router.patch('/{id}', response_model=ResponseUserDto, status_code=status.HTTP_200_OK, name='Изменить информацию о пользователе')
def update(id: int, dto: UpdateUserDto, service: UsersService = Depends(),
           user_id: int = Depends(JwtService.get_current_user_id),
           user_role: valid_roles = Depends(JwtService.check_if_admin)):
    """
    Обновляет информацию о пользователе
    """
    check_for_user(id, service)
    return service.update(id, user_id, dto)


@users_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, name='Удалить пользователя')
def delete(id: int, service: UsersService = Depends(),
           user_id: int = Depends(JwtService.get_current_user_id),
           user_role: valid_roles = Depends(JwtService.check_if_admin)):
    """
    Удаляет пользователя из базы данных
    """
    check_for_user(id, service)
    service.delete(id)


def check_for_user(id: int, users_service: UsersService) -> User:
    return check_for_item(id, users_service, f'Пользователь с {id=} не найден!')
