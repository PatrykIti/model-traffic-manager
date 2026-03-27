from __future__ import annotations

from typing import Protocol


class ConcurrencyLimiter(Protocol):
    def acquire(self, deployment_id: str, max_concurrency: int) -> str | None:
        """Return a lease identifier when a slot is acquired, otherwise None."""

    def release(self, deployment_id: str, lease_id: str) -> None:
        """Release a previously acquired concurrency lease."""
