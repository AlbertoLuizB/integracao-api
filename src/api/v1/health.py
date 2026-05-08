from fastapi import APIRouter
from datetime import datetime, timezone
from src.services.brasil_api import brasil_api_service

router = APIRouter()

@router.get("/health", tags=["Health"])
async def health_check():
    """
    Verifica o status de funcionamento da API e a disponibilidade dos serviços externos.
    """
    # Verifica o status da Brasil API
    is_brasil_api_up = await brasil_api_service.check_health()
    
    timestamp = datetime.now(timezone.utc).isoformat()
    
    if not is_brasil_api_up:
        return {
            "status": "degraded",
            "versao": "1.0.0",
            "timestamp": timestamp,
            "motivo": "Serviço externo indisponível (Brasil API)"
        }

    return {
        "status": "healthy",
        "versao": "1.0.0",
        "timestamp": timestamp
    }
