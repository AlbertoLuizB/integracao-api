from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter()

@router.get("/health", tags=["Health"])
async def health_check():
    """
    Verifica o status de funcionamento da API.
    """
    # A lógica de falha externa ("degraded") será inserida na Fase 3, 
    # quando os serviços externos forem efetivamente configurados.
    return {
        "status": "healthy",
        "versao": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
