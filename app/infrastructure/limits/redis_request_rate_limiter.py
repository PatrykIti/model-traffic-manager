from __future__ import annotations

import time
from collections.abc import Callable
from typing import Protocol

from app.application.ports.request_rate_limiter import RequestRateLimiter


class RedisCounterStore(Protocol):
    def get(self, key: str) -> str | bytes | None:
        """Return the stored counter payload."""

    def set(self, key: str, value: str, *, ex: int | None = None) -> bool | None:
        """Persist the current counter payload."""


class RedisRequestRateLimiter(RequestRateLimiter):
    def __init__(
        self,
        redis_client: RedisCounterStore,
        key_prefix: str = "router:rate-limit",
        now_provider: Callable[[], int] | None = None,
    ) -> None:
        self._redis_client = redis_client
        self._key_prefix = key_prefix
        self._now_provider = now_provider or (lambda: int(time.time()))

    def allow_request(self, deployment_id: str, requests_per_second: int) -> int | None:
        current_second = self._now_provider()
        key = f"{self._key_prefix}:{deployment_id}:{current_second}"
        payload = self._redis_client.get(key)
        count = _parse_int(payload)
        if count >= requests_per_second:
            return 1

        self._redis_client.set(key, str(count + 1), ex=2)
        return None


def _parse_int(payload: str | bytes | None) -> int:
    if payload is None:
        return 0
    if isinstance(payload, bytes):
        payload = payload.decode("utf-8")
    return int(payload)
