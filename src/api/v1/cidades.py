from fastapi import APIRouter, Query
from datetime import datetime, timezone
from src.services.brasil_api import brasil_api_service
from src.core.exceptions import APIException

router = APIRouter()

@router.get("/cidades/{sigla_uf}", tags=["Cidades"])
async def listar_cidades(
    sigla_uf: str,
    limite: int = Query(default=10, ge=1, le=100)
):
    """
    Lista cidades de um estado específico com paginação (limite).
    """
    # Validação manual para garantir a mensagem exata do requisito de 400
    if len(sigla_uf) != 2 or not sigla_uf.isalpha():
        raise APIException(
            status_code=400,
            code="SIGLA_UF_INVALIDA",
            message="A sigla do estado deve conter exatamente 2 letras",
            extra_data={"sigla_uf_informada": sigla_uf}
        )
        
    cidades_data = await brasil_api_service.get_cidades_por_estado(sigla_uf)
    
    # Extrair apenas os nomes para corresponder ao formato de saída esperado e aplicar o limite
    cidades_formatadas = [{"nome": c["nome"]} for c in cidades_data[:limite]]
    
    return {
        "uf": sigla_uf.upper(),
        "quantidade_retornada": len(cidades_formatadas),
        "cidades": cidades_formatadas,
        "consultado_em": datetime.now(timezone.utc).isoformat()
    }
