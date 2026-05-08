from fastapi import APIRouter
<<<<<<< features
from src.core.exceptions import APIException
from src.services.brasil_api_service import brasil_api_service
from datetime import datetime, timezone

router = APIRouter()

@router.get("/clima/{nome_cidade}", summary="Informações da Cidade com Clima")
async def get_clima_cidade(nome_cidade: str):
=======
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
>>>>>>> main
    if len(nome_cidade) < 2:
        raise APIException(
            status_code=400,
            code="NOME_INVALIDO",
            message="O nome da cidade deve conter pelo menos 2 caracteres",
            extra_data={"nome_informado": nome_cidade}
        )
<<<<<<< features

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
=======
        
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
>>>>>>> main
            "unidades": {
                "temperatura": "°C"
            }
        },
<<<<<<< features
        "consultado_em": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
=======
        "consultado_em": datetime.now(timezone.utc).isoformat()
>>>>>>> main
    }
