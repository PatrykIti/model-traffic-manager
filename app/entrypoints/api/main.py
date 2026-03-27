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
from app.entrypoints.api.routes_metrics import router as metrics_router
from app.entrypoints.api.routes_shared_services import router as shared_services_router
from app.infrastructure.bootstrap.container import build_container
from app.infrastructure.config.settings import AppSettings, load_settings
from app.infrastructure.observability.logging import get_logger
from app.infrastructure.observability.request_context import request_context_middleware
from app.infrastructure.observability.startup_snapshot import emit_startup_topology_snapshot
from app.infrastructure.observability.telemetry import configure_observability


def create_app(settings: AppSettings | None = None) -> FastAPI:
    settings = settings or load_settings()
    observability = configure_observability(settings)
    logger = get_logger(__name__)
    container = build_container(settings)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.settings = settings
        app.state.container = container
        app.state.observability = observability
        logger.info(
            "application_startup",
            environment=settings.environment,
            config_path=str(settings.config_path),
        )
        app.state.startup_topology_snapshot = emit_startup_topology_snapshot(
            container=container,
            observability=observability,
        )
        yield
        container.outbound_invoker.close()
        container.inbound_authenticator.close()
        if container.redis_client is not None:
            container.redis_client.close()
        observability.shutdown()
        logger.info("application_shutdown", environment=settings.environment)

    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="Policy-driven AI traffic router for Azure and AKS",
        lifespan=lifespan,
    )
    app.middleware("http")(request_context_middleware)
    app.include_router(chat_router)
    app.include_router(embeddings_router)
    app.include_router(health_router)
    app.include_router(metrics_router)
    app.include_router(deployments_router)
    app.include_router(shared_services_router)
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
