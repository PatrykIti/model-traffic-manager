from __future__ import annotations

from typing import cast

from fastapi import APIRouter, Request
from pydantic import BaseModel

from app.infrastructure.bootstrap.container import BootstrapContainer

router = APIRouter(prefix="/shared-services", tags=["shared-services"])


class SharedServiceSummaryResponse(BaseModel):
    name: str
    endpoint: str
    auth_mode: str


@router.get("", response_model=list[SharedServiceSummaryResponse])
def list_shared_services(request: Request) -> list[SharedServiceSummaryResponse]:
    container = cast(BootstrapContainer, request.app.state.container)
    summaries = container.list_shared_services_use_case.execute()
    return [
        SharedServiceSummaryResponse(
            name=summary.name,
            endpoint=summary.endpoint,
            auth_mode=summary.auth_mode,
        )
        for summary in summaries
    ]
