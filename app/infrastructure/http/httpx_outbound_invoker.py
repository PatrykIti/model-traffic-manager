from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import httpx
from opentelemetry import trace

from app.application.dto.outbound_response import OutboundResponse
from app.domain.errors import OutboundConnectionError, OutboundTimeoutError


class HttpxOutboundInvoker:
    def __init__(
        self,
        *,
        connect_timeout_ms: int = 5000,
        write_timeout_ms: int = 30000,
        pool_timeout_ms: int = 5000,
        max_connections: int = 100,
        max_keepalive_connections: int = 20,
        client: httpx.Client | None = None,
    ) -> None:
        self._connect_timeout_seconds = connect_timeout_ms / 1000
        self._write_timeout_seconds = write_timeout_ms / 1000
        self._pool_timeout_seconds = pool_timeout_ms / 1000
        self._limits = httpx.Limits(
            max_connections=max_connections,
            max_keepalive_connections=max_keepalive_connections,
        )
        self._client = client or httpx.Client(limits=self._limits)

    def post_json(
        self,
        endpoint: str,
        body: Any,
        headers: Mapping[str, str],
        timeout_ms: int,
    ) -> OutboundResponse:
        timeout = self._build_timeout(timeout_ms)
        tracer = trace.get_tracer(__name__)
        try:
            with tracer.start_as_current_span("outbound_http_post_json") as span:
                span.set_attribute("http.url", endpoint)
                span.set_attribute("router.timeout_ms", timeout_ms)
                response = self._client.post(
                    endpoint,
                    json=body,
                    headers=dict(headers),
                    timeout=timeout,
                )
                span.set_attribute("http.status_code", response.status_code)
        except httpx.TimeoutException as exc:
            raise OutboundTimeoutError(f"Upstream request timed out: {exc}") from exc
        except httpx.RequestError as exc:
            raise OutboundConnectionError(f"Upstream request failed: {exc}") from exc

        try:
            json_body = response.json()
            text_body = None
        except ValueError:
            json_body = None
            text_body = response.text

        return OutboundResponse(
            status_code=response.status_code,
            headers={key.lower(): value for key, value in response.headers.items()},
            json_body=json_body,
            text_body=text_body,
        )

    def close(self) -> None:
        self._client.close()

    def _build_timeout(self, timeout_ms: int) -> httpx.Timeout:
        request_timeout_seconds = timeout_ms / 1000
        return httpx.Timeout(
            connect=min(self._connect_timeout_seconds, request_timeout_seconds),
            read=request_timeout_seconds,
            write=min(self._write_timeout_seconds, request_timeout_seconds),
            pool=min(self._pool_timeout_seconds, request_timeout_seconds),
        )
