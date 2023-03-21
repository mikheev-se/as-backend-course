from fastapi.responses import RedirectResponse
from fastapi.routing import APIRouter
from project.api.logs_router import logs_router
from project.api.model_router import model_router
from project.api.users_router import users_router

base_router = APIRouter()

base_router.include_router(logs_router)
base_router.include_router(model_router)
base_router.include_router(users_router)


@base_router.get('/', include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse('/docs')
