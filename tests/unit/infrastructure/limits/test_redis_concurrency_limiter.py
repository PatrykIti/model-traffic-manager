from __future__ import annotations

from app.infrastructure.limits.redis_concurrency_limiter import RedisConcurrencyLimiter


class FakeRedisClient:
    def __init__(self) -> None:
        self.storage: dict[str, str] = {}

    def get(self, key: str) -> str | None:
        return self.storage.get(key)

    def set(self, key: str, value: str, *, ex: int | None = None) -> bool:
        self.storage[key] = value
        return True


def test_redis_concurrency_limiter_tracks_and_releases_leases() -> None:
    limiter = RedisConcurrencyLimiter(redis_client=FakeRedisClient())

    first = limiter.acquire("deployment-a", max_concurrency=1)
    second = limiter.acquire("deployment-a", max_concurrency=1)

    assert first is not None
    assert second is None

    limiter.release("deployment-a", first)

    assert limiter.acquire("deployment-a", max_concurrency=1) is not None
