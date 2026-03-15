from __future__ import annotations

import json
from typing import Protocol
from uuid import uuid4

from app.application.ports.concurrency_limiter import ConcurrencyLimiter


class RedisLeaseStore(Protocol):
    def get(self, key: str) -> str | bytes | None:
        """Return the stored lease payload."""

    def set(self, key: str, value: str, *, ex: int | None = None) -> bool | None:
        """Persist the current lease payload."""


class RedisConcurrencyLimiter(ConcurrencyLimiter):
    def __init__(
        self,
        redis_client: RedisLeaseStore,
        key_prefix: str = "router:concurrency",
        lease_ttl_seconds: int = 60,
    ) -> None:
        self._redis_client = redis_client
        self._key_prefix = key_prefix
        self._lease_ttl_seconds = lease_ttl_seconds

    def acquire(self, deployment_id: str, max_concurrency: int) -> str | None:
        key = self._build_key(deployment_id)
        active_leases = self._load_leases(key)
        if len(active_leases) >= max_concurrency:
            return None

        lease_id = uuid4().hex
        active_leases.append(lease_id)
        self._redis_client.set(
            key,
            json.dumps(active_leases, separators=(",", ":")),
            ex=self._lease_ttl_seconds,
        )
        return lease_id

    def release(self, deployment_id: str, lease_id: str) -> None:
        key = self._build_key(deployment_id)
        active_leases = self._load_leases(key)
        updated_leases = [active for active in active_leases if active != lease_id]
        self._redis_client.set(
            key,
            json.dumps(updated_leases, separators=(",", ":")),
            ex=self._lease_ttl_seconds if updated_leases else 1,
        )

    def _build_key(self, deployment_id: str) -> str:
        return f"{self._key_prefix}:{deployment_id}"

    def _load_leases(self, key: str) -> list[str]:
        payload = self._redis_client.get(key)
        if payload is None:
            return []
        if isinstance(payload, bytes):
            payload = payload.decode("utf-8")
        raw = json.loads(payload)
        return [str(value) for value in raw]
