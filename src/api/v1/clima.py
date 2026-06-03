from fastapi import APIRouter
from src.core.exceptions import APIException
from src.services.open_meteo_service import open_meteo_service
from datetime import datetime, timezone

router = APIRouter()

@router.get("/clima/{nome_cidade}", summary="Informações da Cidade com Clima")
async def get_clima_cidade(nome_cidade: str):
    if len(nome_cidade) < 2:
        raise APIException(
            status_code=400,
            code="NOME_INVALIDO",
            message="O nome da cidade deve conter pelo menos 2 caracteres",
            extra_data={"nome_informado": nome_cidade}
        )

    geo_data = await open_meteo_service.get_coordenadas(nome_cidade)
    
    clima_data = await open_meteo_service.get_clima(
        latitude=geo_data["latitude"],
        longitude=geo_data["longitude"]
    )

    return {
        "nome": geo_data["nome"],
        "estado": geo_data["estado"],
        "clima": {
            "temperatura_min": clima_data["temperatura_min"],
            "temperatura_max": clima_data["temperatura_max"],
            "condicao": clima_data["condicao"],
            "unidades": {
                "temperatura": "°C"
            }
        },
        "consultado_em": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }
