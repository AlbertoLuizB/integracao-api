from fastapi import FastAPI

app = FastAPI(
    title="API de Agregação de Dados Climáticos e Geográficos",
    version="0.1.0"
)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Dados Climáticos e Geográficos"}
