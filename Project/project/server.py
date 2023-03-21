from fastapi import FastAPI
from project.api.base_router import base_router

app = FastAPI()

app.include_router(base_router)
