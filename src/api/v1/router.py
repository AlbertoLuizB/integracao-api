from fastapi import APIRouter
from . import health

api_router = APIRouter()

api_router.include_router(health.router)
# Posteriormente adicionaremos aqui as rotas de "cidades" e "clima"
