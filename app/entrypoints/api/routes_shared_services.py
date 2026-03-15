from __future__ import annotations

from json import JSONDecodeError
from typing import cast

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

from app.application.dto.shared_service_request import SharedServiceRequest
from app.domain.errors import (
    ConcurrencyLimitExceededError,
    OutboundConnectionError,
    OutboundTimeoutError,
    RequestRateLimitExceededError,
    SecretResolutionError,
    SharedServiceExecutionDisabledError,
    SharedServiceNotFound,
    SharedServiceTransportMismatchError,
    TokenAcquisitionError,
    UnsupportedAuthModeError,
    UpstreamSelectionError,
)
from app.infrastructure.bootstrap.container import BootstrapContainer

router = APIRouter(tags=["shared-services"])


class SharedServiceSummaryResponse(BaseModel):
    name: str
    transport: str
    access_mode: str
    routing_strategy: str | None
    provider_managed_availability: bool
    router_callable: bool
    upstream_count: int
    providers: list[str]
    regions: list[str]
    endpoint: str | None
    auth_mode: str | None


@router.get("/shared-services", response_model=list[SharedServiceSummaryResponse])
def list_shared_services(request: Request) -> list[SharedServiceSummaryResponse]:
    container = cast(BootstrapContainer, request.app.state.container)
    summaries = container.list_shared_services_use_case.execute()
    return [
        SharedServiceSummaryResponse(
            name=summary.name,
            transport=summary.transport,
            access_mode=summary.access_mode,
            routing_strategy=summary.routing_strategy,
            provider_managed_availability=summary.provider_managed_availability,
            router_callable=summary.router_callable,
            upstream_count=summary.upstream_count,
            providers=list(summary.providers),
            regions=list(summary.regions),
            endpoint=summary.endpoint,
            auth_mode=summary.auth_mode,
        )
        for summary in summaries
    ]


@router.post("/v1/shared-services/{service_id}")
async def execute_shared_service(request: Request, service_id: str) -> Response:
    try:
        payload = await request.json()
    except JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail="Request body must be valid JSON.") from exc

    container = cast(BootstrapContainer, request.app.state.container)

    try:
        outbound_response = container.route_shared_service_use_case.execute(
            SharedServiceRequest(
                service_id=service_id,
                payload=payload,
                request_id=request.state.request_id,
            )
        )
    except SharedServiceNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except SharedServiceExecutionDisabledError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except SharedServiceTransportMismatchError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except SecretResolutionError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except RequestRateLimitExceededError as exc:
        raise HTTPException(
            status_code=429,
            detail=str(exc),
            headers={"Retry-After": str(exc.retry_after_seconds or 1)},
        ) from exc
    except ConcurrencyLimitExceededError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except UnsupportedAuthModeError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except TokenAcquisitionError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except UpstreamSelectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except OutboundTimeoutError as exc:
        raise HTTPException(status_code=504, detail=str(exc)) from exc
    except OutboundConnectionError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    if outbound_response.json_body is not None:
        return JSONResponse(
            status_code=outbound_response.status_code,
            content=outbound_response.json_body,
        )

    return Response(
        status_code=outbound_response.status_code,
        content=outbound_response.text_body or "",
        media_type=outbound_response.content_type or "text/plain",
    )
