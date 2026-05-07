from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="API de Agregação de Dados Climáticos e Geográficos",
    description="API que consome dados da Brasil API e Open-Meteo para retornar dados climáticos enriquecidos.",
    version="1.0.0"
)

# Configuração CORS (Habilitado para testes via navegador)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "API de Dados Climáticos e Geográficos em funcionamento."}
