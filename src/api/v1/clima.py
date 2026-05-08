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

    # 1. Busca código e estado da cidade
    cidade_info = await brasil_api_service.get_cidade_cptec(nome_cidade)
    city_code = cidade_info.get("id")
    estado = cidade_info.get("estado")
    nome = cidade_info.get("nome")

    if not city_code:
        raise APIException(
            status_code=404,
            code="CIDADE_NAO_ENCONTRADA",
            message="Nenhuma cidade encontrada com o nome informado",
            extra_data={"nome_informado": nome_cidade}
        )

    # 2. Busca previsão do clima (hoje)
    previsao_info = await brasil_api_service.get_clima_cptec(city_code)
    
    # A Brasil API CPTEC Clima retorna uma lista "clima", usaremos o primeiro dia (hoje)
    lista_clima = previsao_info.get("clima", [])
    if not lista_clima:
         raise APIException(
            status_code=404,
            code="CLIMA_NAO_ENCONTRADO",
            message="Dados climáticos não encontrados para a cidade",
            extra_data={"nome_informado": nome_cidade}
        )
        
    clima_hoje = lista_clima[0]

    return {
        "nome": nome,
        "estado": estado,
        "clima": {
            "temperatura_min": clima_hoje.get("min"),
            "temperatura_max": clima_hoje.get("max"),
            "condicao": clima_hoje.get("condicao_desc", clima_hoje.get("condicao")),
            "unidades": {
                "temperatura": "°C"
            }
        },
        "consultado_em": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }
