from fastapi import APIRouter, Query
from src.core.exceptions import APIException
from src.services.brasil_api_service import brasil_api_service
from datetime import datetime, timezone

router = APIRouter()

@router.get("/cidades/{sigla_uf}", summary="Lista de Cidades por Estado")
async def get_cidades_por_estado(
    sigla_uf: str,
    limite: int = Query(10, description="Quantidade máxima de cidades (1-100)", ge=1, le=100)
):
    sigla_uf = sigla_uf.upper()
    
    if len(sigla_uf) != 2:
        raise APIException(
            status_code=400,
            code="SIGLA_UF_INVALIDA",
            message="A sigla do estado deve conter exatamente 2 letras",
            extra_data={"sigla_uf_informada": sigla_uf}
        )

    # Busca cidades no IBGE via Brasil API
    cidades_data = await brasil_api_service.get_cidades_por_estado(sigla_uf)
    
    # Limita o número de cidades
    cidades_limitadas = cidades_data[:limite]
    
    # Mapeia para o formato de saída exigido
    cidades_formatadas = [{"nome": cidade["nome"]} for cidade in cidades_limitadas]
    
    return {
        "uf": sigla_uf,
        "quantidade_retornada": len(cidades_formatadas),
        "cidades": cidades_formatadas,
        "consultado_em": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }
