from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from project.entities.dto.user_dto import CreateUserDto, RegistrationDto, ResponseUserDto, UpdateUserDto
from project.entities.user_entity import User, valid_roles
from project.service.jwt_service import JwtService
from project.service.users_service import UsersService
from fastapi.security import OAuth2PasswordRequestForm

users_router = APIRouter(
    prefix='/users',
    tags=['users']
)


@users_router.get('/', response_model=list[ResponseUserDto], status_code=status.HTTP_200_OK, name='Получить всех пользователей')
def get_all(users_service: UsersService = Depends(),
            requester_id: int = Depends(JwtService.get_current_user_id),
            requester_role: valid_roles = Depends(JwtService.check_if_admin)):
    """
    Возвращает список всех пользователей
    """
    return users_service.get_all()


@users_router.get('/me', response_model=ResponseUserDto, status_code=status.HTTP_200_OK, name='Получить текущего пользователя')
def me(users_service: UsersService = Depends(),
       requester_id: int = Depends(JwtService.get_current_user_id)):
    """
    Используя JWT и находящийся в нём идентификатор пользователя возвращает текущего пользователя
    """
    return users_service.get_by_id(requester_id)


@users_router.post('/register', response_model=ResponseUserDto, status_code=status.HTTP_201_CREATED, name='Регистрация')
def register(dto: RegistrationDto, users_service: UsersService = Depends()):
    """
    Регистрирует пользователя с заданными именем и паролем
    """
    return users_service.register(dto)


@users_router.post('/authorize', status_code=status.HTTP_200_OK, name='Авторизация')
def authorize(auth_schema: OAuth2PasswordRequestForm = Depends(), users_service: UsersService = Depends()):
    """
    Авторизация с заданными логином и паролем
    """
    return users_service.authorize(auth_schema.username, auth_schema.password)


@users_router.get('/{id}', response_model=ResponseUserDto, status_code=status.HTTP_200_OK, name='Получить пользователя с заданным id')
def get_by_id(id: int, users_service: UsersService = Depends(),
              requester_id: int = Depends(JwtService.get_current_user_id),
              requester_role: valid_roles = Depends(JwtService.check_if_admin)):
    """
    Возвращает пользователя с заданным идентификатором
    """
    return check_for_user(id, users_service)


@users_router.post('/', response_model=ResponseUserDto, status_code=status.HTTP_201_CREATED, name='Добавить пользователя')
def create(dto: CreateUserDto, users_service: UsersService = Depends(),
           requester_id: int = Depends(JwtService.get_current_user_id),
           requester_role: valid_roles = Depends(JwtService.check_if_admin)):
    """
    Создаёт в базе данных нового пользователя
    """
    return users_service.create(dto, requester_id)


@users_router.patch('/{id}', response_model=ResponseUserDto, status_code=status.HTTP_200_OK, name='Изменить информацию о пользователе')
def update(id: int, dto: UpdateUserDto, users_service: UsersService = Depends(),
           requester_id: int = Depends(JwtService.get_current_user_id),
           requester_role: valid_roles = Depends(JwtService.check_if_admin)):
    """
    Обновляет информацию о пользователе
    """
    check_for_user(id, users_service)
    return users_service.update(id, dto, requester_id)


@users_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, name='Удалить пользователя')
def delete(id: int, users_service: UsersService = Depends(),
           requester_id: int = Depends(JwtService.get_current_user_id),
           requester_role: valid_roles = Depends(JwtService.check_if_admin)):
    """
    Удаляет пользователя из базы данных
    """
    check_for_user(id, users_service)
    users_service.delete(id)


def check_for_user(id: int, users_service: UsersService) -> User:
    user = users_service.get_by_id(id)
    error_msg = f'Пользователь с {id=} не найден!'
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=error_msg)
    return user
