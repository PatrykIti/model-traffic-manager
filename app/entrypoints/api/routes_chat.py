from __future__ import annotations

from json import JSONDecodeError
from typing import cast

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse, Response

from app.application.dto.chat_completion_request import ChatCompletionRequest
from app.domain.errors import (
    DeploymentNotFound,
    OutboundConnectionError,
    OutboundTimeoutError,
    SecretResolutionError,
    UnsupportedAuthModeError,
)
from app.infrastructure.bootstrap.container import BootstrapContainer

router = APIRouter(prefix="/v1/chat/completions", tags=["chat"])


@router.post("/{deployment_id}")
async def chat_completions(request: Request, deployment_id: str) -> Response:
    try:
        payload = await request.json()
    except JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail="Request body must be valid JSON.") from exc

    container = cast(BootstrapContainer, request.app.state.container)

    try:
        outbound_response = container.route_chat_completion_use_case.execute(
            ChatCompletionRequest(deployment_id=deployment_id, payload=payload)
        )
    except DeploymentNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except SecretResolutionError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except UnsupportedAuthModeError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
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
