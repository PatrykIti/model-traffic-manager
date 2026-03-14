from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.entrypoints.api.error_handlers import register_error_handlers
from app.entrypoints.api.routes_chat import router as chat_router
from app.entrypoints.api.routes_deployments import router as deployments_router
from app.entrypoints.api.routes_embeddings import router as embeddings_router
from app.entrypoints.api.routes_health import router as health_router
from app.infrastructure.bootstrap.container import build_container
from app.infrastructure.config.settings import AppSettings, load_settings
from app.infrastructure.observability.logging import configure_logging, get_logger


def create_app(settings: AppSettings | None = None) -> FastAPI:
    settings = settings or load_settings()
    configure_logging(settings.log_level)
    logger = get_logger(__name__)
    container = build_container(settings)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.settings = settings
        app.state.container = container
        logger.info(
            "application_startup",
            environment=settings.environment,
            config_path=str(settings.config_path),
        )
        yield
        logger.info("application_shutdown", environment=settings.environment)

    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="Policy-driven AI traffic router for Azure and AKS",
        lifespan=lifespan,
    )
    app.include_router(chat_router)
    app.include_router(embeddings_router)
    app.include_router(health_router)
    app.include_router(deployments_router)
    register_error_handlers(app)
    return app


app = create_app()


def run() -> None:
    settings: AppSettings = load_settings()
    uvicorn.run(
        "app.entrypoints.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
    )


if __name__ == "__main__":
    run()
