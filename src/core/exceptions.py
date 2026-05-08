from fastapi import Request
from fastapi.responses import JSONResponse
from typing import Optional

class APIException(Exception):
    def __init__(self, status_code: int, code: str, message: str, extra_data: Optional[dict] = None):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.extra_data = extra_data or {}

async def api_exception_handler(request: Request, exc: APIException):
    content = {
        "erro": True,
        "codigo": exc.code,
        "mensagem": exc.message
    }
    content.update(exc.extra_data)
    
    return JSONResponse(
        status_code=exc.status_code,
        content=content,
    )
