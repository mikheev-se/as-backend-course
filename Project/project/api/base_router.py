from fastapi import APIRouter, Depends
from project.api.tanks_router import tanks_router
from project.api.operations_router import operations_router
from project.api.products_router import products_router
from project.api.users_router import users_router
from project.service.users_service import UsersService

router = APIRouter()

router.include_router(tanks_router)
router.include_router(operations_router)
router.include_router(products_router)
router.include_router(users_router)
