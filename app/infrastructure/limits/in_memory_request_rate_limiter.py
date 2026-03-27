from __future__ import annotations

import time
from collections.abc import Callable

from app.application.ports.request_rate_limiter import RequestRateLimiter


class InMemoryRequestRateLimiter(RequestRateLimiter):
    def __init__(self, now_provider: Callable[[], int] | None = None) -> None:
        self._now_provider = now_provider or (lambda: int(time.time()))
        self._windows: dict[str, tuple[int, int]] = {}

    def allow_request(self, deployment_id: str, requests_per_second: int) -> int | None:
        current_second = self._now_provider()
        window_start, count = self._windows.get(deployment_id, (current_second, 0))
        if window_start != current_second:
            window_start, count = current_second, 0

        if count >= requests_per_second:
            self._windows[deployment_id] = (window_start, count)
            return max((window_start + 1) - current_second, 1)

        self._windows[deployment_id] = (window_start, count + 1)
        return None
