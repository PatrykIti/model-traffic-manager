from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.infrastructure.observability.logging import get_logger


def register_error_handlers(app: FastAPI) -> None:
    logger = get_logger(__name__)

    @app.exception_handler(HTTPException)
    async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("unhandled_exception", error=str(exc))
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"},
        )
