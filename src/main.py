from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.router import api_router
from src.core.exceptions import APIException, api_exception_handler

app = FastAPI(
    title="API de Agregação de Dados Climáticos e Geográficos",
    description="API que consome dados da Brasil API e Open-Meteo para retornar dados climáticos enriquecidos.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(APIException, api_exception_handler)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "API de Dados Climáticos e Geográficos em funcionamento."}
