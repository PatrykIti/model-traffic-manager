from __future__ import annotations

from app.infrastructure.limits.redis_request_rate_limiter import RedisRequestRateLimiter


class FakeRedisClient:
    def __init__(self) -> None:
        self.storage: dict[str, str] = {}

    def get(self, key: str) -> str | None:
        return self.storage.get(key)

    def set(self, key: str, value: str, *, ex: int | None = None) -> bool:
        self.storage[key] = value
        return True


def test_redis_request_rate_limiter_counts_requests_per_second() -> None:
    limiter = RedisRequestRateLimiter(
        redis_client=FakeRedisClient(),
        now_provider=lambda: 100,
    )

    assert limiter.allow_request("deployment-a", requests_per_second=1) is None
    assert limiter.allow_request("deployment-a", requests_per_second=1) == 1
