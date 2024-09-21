from dotenv import load_dotenv

# Load environment variables

load_dotenv()

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from routes.api_conversations import router as conversations_router
from routes.api_query import router as query_router
from db.db import init_db, close_connection
from typing import Dict
from models.schemas import APIError
# Initialize FastAPI app
app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_details = []
    for error in exc.errors():
        error_details.append({
            "loc": error["loc"],
            "msg": error["msg"],
            "type": error["type"]
        })
    api_error = APIError(
        code=400,
        message="Invalid parameters provided",
        request={"method": request.method, "url": str(request.url)},
        details={"errors": error_details}
    )
    return JSONResponse(
        status_code=400,
        content=api_error.dict()
    )

# Include routers
app.include_router(conversations_router)
app.include_router(query_router)

# Initialize database connection on startup
@app.on_event("startup")
async def on_startup() -> None:
    await init_db()

# Close database connection on shutdown
@app.on_event("shutdown")
async def on_shutdown() -> None:
    close_connection()
