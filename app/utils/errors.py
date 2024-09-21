
from models.schemas import APIError
from fastapi.responses import JSONResponse

def create_error_response(status_code: int, message: str, request: dict, error: Exception) -> JSONResponse:
    return APIError(
        code=status_code,
        message=message,
        request=request,
        details={"error": str(error)}
    )
