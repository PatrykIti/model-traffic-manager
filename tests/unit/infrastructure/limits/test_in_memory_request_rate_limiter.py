from __future__ import annotations

from app.infrastructure.limits.in_memory_request_rate_limiter import InMemoryRequestRateLimiter


def test_in_memory_request_rate_limiter_allows_until_limit_then_rejects() -> None:
    limiter = InMemoryRequestRateLimiter(now_provider=lambda: 100)

    assert limiter.allow_request("deployment-a", requests_per_second=2) is None
    assert limiter.allow_request("deployment-a", requests_per_second=2) is None
    assert limiter.allow_request("deployment-a", requests_per_second=2) == 1


def test_in_memory_request_rate_limiter_resets_on_new_second() -> None:
    current_second = 100
    limiter = InMemoryRequestRateLimiter(now_provider=lambda: current_second)

    assert limiter.allow_request("deployment-a", requests_per_second=1) is None
    assert limiter.allow_request("deployment-a", requests_per_second=1) == 1

    current_second = 101
    assert limiter.allow_request("deployment-a", requests_per_second=1) is None
