from fastapi import Request
from fastapi.responses import JSONResponse

class APIException(Exception):
    def __init__(self, status_code: int, code: str, message: str):
        self.status_code = status_code
        self.code = code
        self.message = message

async def api_exception_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"erro": {"codigo": exc.code, "mensagem": exc.message}},
    )
