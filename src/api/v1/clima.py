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

    cidade_info = await open_meteo_service.get_coordinates_by_city_name(nome_cidade)
    lat = cidade_info.get("latitude")
    lon = cidade_info.get("longitude")
    estado = cidade_info.get("estado")
    nome = cidade_info.get("nome")

    clima_data = await open_meteo_service.get_weather_by_coordinates(lat, lon)
    
    current = clima_data.get("current", {})
    daily = clima_data.get("daily", {})

    temp_max = daily.get("temperature_2m_max", [None])[0]
    temp_min = daily.get("temperature_2m_min", [None])[0]
    
    if temp_max is not None:
        temp_max = round(temp_max)
    if temp_min is not None:
        temp_min = round(temp_min)
        
    weather_code = current.get("weather_code")
    condicao_texto = open_meteo_service.get_condicao_descricao(weather_code)

    return {
        "nome": nome,
        "estado": estado,
        "clima": {
            "temperatura_min": temp_min,
            "temperatura_max": temp_max,
            "condicao": condicao_texto,
            "unidades": {
                "temperatura": "°C"
            }
        },
        "consultado_em": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }
