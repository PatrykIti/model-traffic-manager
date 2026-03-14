from __future__ import annotations

from typing import Protocol


class RequestRateLimiter(Protocol):
    def allow_request(self, deployment_id: str, requests_per_second: int) -> int | None:
        """Return a retry-after window in seconds when rejected, otherwise None."""
