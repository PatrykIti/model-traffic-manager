from __future__ import annotations

import time
from collections.abc import Awaitable, Callable
from uuid import uuid4

import structlog
from fastapi import Request, Response
from opentelemetry import trace

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

    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(request_id=request_id, endpoint_kind=endpoint_kind)

    with tracer.start_as_current_span(f"{request.method} {request.url.path}") as span:
        span.set_attribute("http.method", request.method)
        span.set_attribute("http.target", request.url.path)
        span.set_attribute("router.request_id", request_id)
        span.set_attribute("router.endpoint_kind", endpoint_kind)

        response = await call_next(request)

    duration = time.perf_counter() - start
    observe_request_duration(endpoint_kind, duration)
    response.headers["x-request-id"] = request_id
    return response


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
