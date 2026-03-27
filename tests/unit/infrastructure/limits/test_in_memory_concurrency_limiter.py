from __future__ import annotations

from app.infrastructure.limits.in_memory_concurrency_limiter import InMemoryConcurrencyLimiter


def test_in_memory_concurrency_limiter_rejects_when_limit_is_reached() -> None:
    limiter = InMemoryConcurrencyLimiter()

    first = limiter.acquire("deployment-a", max_concurrency=1)
    second = limiter.acquire("deployment-a", max_concurrency=1)

    assert first is not None
    assert second is None


def test_in_memory_concurrency_limiter_releases_slots() -> None:
    limiter = InMemoryConcurrencyLimiter()

    lease_id = limiter.acquire("deployment-a", max_concurrency=1)
    assert lease_id is not None

    limiter.release("deployment-a", lease_id)

    assert limiter.acquire("deployment-a", max_concurrency=1) is not None
