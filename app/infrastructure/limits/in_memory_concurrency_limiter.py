from __future__ import annotations

from uuid import uuid4

from app.application.ports.concurrency_limiter import ConcurrencyLimiter


class InMemoryConcurrencyLimiter(ConcurrencyLimiter):
    def __init__(self) -> None:
        self._active_leases: dict[str, set[str]] = {}

    def acquire(self, deployment_id: str, max_concurrency: int) -> str | None:
        active = self._active_leases.setdefault(deployment_id, set())
        if len(active) >= max_concurrency:
            return None

        lease_id = uuid4().hex
        active.add(lease_id)
        return lease_id

    def release(self, deployment_id: str, lease_id: str) -> None:
        active = self._active_leases.get(deployment_id)
        if active is None:
            return
        active.discard(lease_id)
