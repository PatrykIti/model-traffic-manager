from __future__ import annotations

from fastapi import APIRouter, Response

from app.infrastructure.observability.runtime_event_recorder import metrics_payload

router = APIRouter(tags=["metrics"])


@router.get("/metrics")
async def metrics() -> Response:
    return Response(content=metrics_payload(), media_type="text/plain; version=0.0.4")
