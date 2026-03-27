from __future__ import annotations

from typing import cast

from fastapi import APIRouter, Request
from pydantic import BaseModel

from app.infrastructure.bootstrap.container import BootstrapContainer

router = APIRouter(prefix="/deployments", tags=["deployments"])


class DeploymentSummaryResponse(BaseModel):
    id: str
    kind: str
    protocol: str
    consumer_role: str | None
    routing_strategy: str
    upstream_count: int
    providers: list[str]
    regions: list[str]


@router.get("", response_model=list[DeploymentSummaryResponse])
def list_deployments(request: Request) -> list[DeploymentSummaryResponse]:
    container = cast(BootstrapContainer, request.app.state.container)
    summaries = container.list_deployments_use_case.execute()
    return [
        DeploymentSummaryResponse(
            id=summary.id,
            kind=summary.kind,
            protocol=summary.protocol,
            consumer_role=summary.consumer_role,
            routing_strategy=summary.routing_strategy,
            upstream_count=summary.upstream_count,
            providers=list(summary.providers),
            regions=list(summary.regions),
        )
        for summary in summaries
    ]
