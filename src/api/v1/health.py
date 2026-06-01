from fastapi import APIRouter
from datetime import datetime, timezone
import httpx

router = APIRouter()

@router.get("/health", tags=["Health"])
async def health_check():
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get("https://geocoding-api.open-meteo.com/v1/search?name=a&count=1")
            resp.raise_for_status()
            
            return {
                "status": "healthy",
                "versao": "1.0.0",
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            }
    except Exception:
        return {
            "status": "degraded",
            "versao": "1.0.0",
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "motivo": "Serviço externo indisponível"
        }
