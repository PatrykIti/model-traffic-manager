from __future__ import annotations

import time
from collections.abc import Awaitable, Callable
from typing import Any, cast
from uuid import uuid4

import structlog
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from opentelemetry import trace

from app.application.dto.request_principal import RequestPrincipal
from app.domain.errors import InboundAuthenticationError, InboundAuthorizationError
from app.infrastructure.bootstrap.container import BootstrapContainer
from app.infrastructure.observability.logging import get_logger
from app.infrastructure.observability.runtime_event_recorder import observe_request_duration


async def request_context_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    request_id = request.headers.get("x-request-id", uuid4().hex)
    request.state.request_id = request_id
    endpoint_kind = _resolve_endpoint_kind(request.url.path)
    start = time.perf_counter()
    tracer = trace.get_tracer(__name__)
    logger = get_logger(__name__)
    container = cast(BootstrapContainer, request.app.state.container)

    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(request_id=request_id, endpoint_kind=endpoint_kind)

    with tracer.start_as_current_span(
        f"{request.method} {request.url.path}",
        kind=trace.SpanKind.SERVER,
    ) as span:
        span.set_attribute("http.method", request.method)
        span.set_attribute("http.url", str(request.url))
        span.set_attribute("http.target", request.url.path)
        span.set_attribute("router.request_id", request_id)
        span.set_attribute("router.endpoint_kind", endpoint_kind)

        if _requires_client_auth(request.url.path) and container.inbound_authenticator.enabled:
            principal = _authenticate_request(
                request=request,
                container=container,
                request_id=request_id,
                logger=logger,
            )
            if principal is None:
                auth_response: Response = _auth_failure_response(
                    request_id=request_id,
                    detail=str(getattr(request.state, "auth_failure_detail", "Unauthorized")),
                    status_code=int(getattr(request.state, "auth_failure_status_code", 401)),
                )
                span.set_attribute("http.status_code", auth_response.status_code)
                return auth_response
            request.state.principal = principal
            _bind_principal_context(principal, span)
        else:
            request.state.principal = None

        response = await call_next(request)
        span.set_attribute("http.status_code", response.status_code)

    duration = time.perf_counter() - start
    observe_request_duration(endpoint_kind, duration)
    response.headers["x-request-id"] = request_id
    return response


def _requires_client_auth(path: str) -> bool:
    return not (path.startswith("/health") or path == "/metrics")


def _authenticate_request(
    *,
    request: Request,
    container: BootstrapContainer,
    request_id: str,
    logger: Any,
) -> RequestPrincipal | None:
    try:
        return container.inbound_authenticator.authenticate(
            request.headers.get("authorization")
        )
    except (InboundAuthenticationError, InboundAuthorizationError) as exc:
        status_code = 403 if isinstance(exc, InboundAuthorizationError) else 401
        logger.info(
            "inbound_auth_rejected",
            request_id=request_id,
            endpoint_kind=_resolve_endpoint_kind(request.url.path),
            reason=str(exc),
            status_code=status_code,
        )
        request.state.auth_failure_status_code = status_code
        request.state.auth_failure_detail = str(exc)
        return None


def _bind_principal_context(principal: RequestPrincipal, span: trace.Span) -> None:
    structlog.contextvars.bind_contextvars(
        caller_auth_mode=principal.auth_mode,
        caller_principal_id=principal.principal_id,
        caller_display_name=principal.display_name,
        caller_consumer_role=principal.client_consumer_role,
    )
    span.set_attribute("router.caller_auth_mode", principal.auth_mode)
    span.set_attribute("router.caller_principal_id", principal.principal_id)
    if principal.client_consumer_role is not None:
        span.set_attribute("router.caller_consumer_role", principal.client_consumer_role)
    span.set_attribute("router.caller_display_name", principal.display_name)


def _auth_failure_response(
    *,
    request_id: str,
    detail: str,
    status_code: int,
) -> JSONResponse:
    headers = {"x-request-id": request_id}
    if status_code == 401:
        headers["WWW-Authenticate"] = "Bearer"
    return JSONResponse(
        status_code=status_code,
        content={"detail": detail},
        headers=headers,
    )


def _resolve_endpoint_kind(path: str) -> str:
    if path.startswith("/v1/chat/completions"):
        return "chat_completions"
    if path.startswith("/v1/embeddings"):
        return "embeddings"
    if path.startswith("/v1/shared-services"):
        return "shared_service"
    if path.startswith("/shared-services"):
        return "shared_service_registry"
    if path.startswith("/health"):
        return "health"
    if path == "/metrics":
        return "metrics"
    return "unknown"
