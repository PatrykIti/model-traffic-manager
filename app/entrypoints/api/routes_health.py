from __future__ import annotations

from typing import cast

from fastapi import APIRouter, Request
from pydantic import BaseModel

from app.infrastructure.bootstrap.container import BootstrapContainer

router = APIRouter(prefix="/health", tags=["health"])


class HealthResponse(BaseModel):
    status: str
    kind: str
    service: str


def _build_response(request: Request, kind: str) -> HealthResponse:
    container = cast(BootstrapContainer, request.app.state.container)
    return HealthResponse(
        status="ok",
        kind=kind,
        service=container.settings.app_name,
    )


@router.get("/live", response_model=HealthResponse)
def live(request: Request) -> HealthResponse:
    return _build_response(request, "live")


@router.get("/ready", response_model=HealthResponse)
def ready(request: Request) -> HealthResponse:
    return _build_response(request, "ready")
