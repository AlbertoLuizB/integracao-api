from fastapi import APIRouter
from datetime import datetime, timezone
from src.services.brasil_api import brasil_api_service
from src.core.exceptions import APIException

router = APIRouter()

@router.get("/clima/{nome_cidade}", tags=["Clima"])
async def buscar_clima_cidade(nome_cidade: str):
    """
    Busca o clima de uma cidade pelo nome e combina com dados geográficos.
    """
    # Validação manual do nome da cidade (min: 2 caracteres)
    if len(nome_cidade) < 2:
        raise APIException(
            status_code=400,
            code="NOME_INVALIDO",
            message="O nome da cidade deve conter pelo menos 2 caracteres",
            extra_data={"nome_informado": nome_cidade}
        )
        
    # 1. Obter os dados da cidade (para pegar o código CPTEC, nome e uf)
    cidades_encontradas = await brasil_api_service.buscar_cidade_por_nome(nome_cidade)
    
    # Pegamos a primeira cidade retornada na busca
    cidade = cidades_encontradas[0]
    
    # 2. Obter os dados climáticos utilizando o código CPTEC da cidade
    clima_data = await brasil_api_service.buscar_clima_por_codigo(cidade["id"])
    
    # 3. Combinar os dados conforme o payload esperado (usamos o primeiro dia da previsão)
    hoje = clima_data["clima"][0]
    
    return {
        "nome": cidade["nome"],
        "estado": cidade["estado"],
        "clima": {
            "temperatura_min": hoje["min"],
            "temperatura_max": hoje["max"],
            "condicao": hoje["condicao_desc"],
            "unidades": {
                "temperatura": "°C"
            }
        },
        "consultado_em": datetime.now(timezone.utc).isoformat()
    }
