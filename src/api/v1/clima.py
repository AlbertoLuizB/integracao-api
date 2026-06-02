from fastapi import APIRouter
from src.core.exceptions import APIException
from src.services.brasil_api_service import brasil_api_service
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

    # 1. Busca a cidade pelo nome usando CPTEC para pegar o ID, Nome correto e Estado
    cidade_info = await brasil_api_service.get_cidade_cptec(nome_cidade)
    city_code = cidade_info.get("id")
    nome = cidade_info.get("nome")
    estado = cidade_info.get("estado")

    # 2. Busca a previsão do clima usando o ID da cidade
    clima_data = await brasil_api_service.get_clima_cptec(city_code)
    
    previsoes = clima_data.get("clima", [])
    
    if not previsoes:
        raise APIException(
            status_code=404,
            code="CLIMA_NAO_ENCONTRADO",
            message="Não foi possível encontrar a previsão do tempo para esta cidade.",
            extra_data={"cidade": nome}
        )

    # Pegamos a previsão do dia atual (o primeiro da lista)
    previsao_hoje = previsoes[0]
    
    temp_min = previsao_hoje.get("min")
    temp_max = previsao_hoje.get("max")
    condicao_texto = previsao_hoje.get("condicao_desc", "Não informada")

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
