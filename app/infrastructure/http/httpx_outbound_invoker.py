from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import httpx

from app.application.dto.outbound_response import OutboundResponse
from app.domain.errors import OutboundConnectionError, OutboundTimeoutError


class HttpxOutboundInvoker:
    def post_json(
        self,
        endpoint: str,
        body: Any,
        headers: Mapping[str, str],
        timeout_ms: int,
    ) -> OutboundResponse:
        timeout = timeout_ms / 1000
        try:
            with httpx.Client(timeout=timeout) as client:
                response = client.post(endpoint, json=body, headers=dict(headers))
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
