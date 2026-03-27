from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol

from app.application.dto.outbound_response import OutboundResponse


class OutboundInvoker(Protocol):
    def post_json(
        self,
        endpoint: str,
        body: Any,
        headers: Mapping[str, str],
        timeout_ms: int,
    ) -> OutboundResponse:
        """Send a JSON POST request to the upstream endpoint."""
