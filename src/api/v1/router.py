from fastapi import APIRouter
from . import health, cidades, clima

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(cidades.router)
api_router.include_router(clima.router)
