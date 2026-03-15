from __future__ import annotations

from pathlib import Path

from app.infrastructure.bootstrap.container import build_container
from app.infrastructure.config.settings import AppSettings
from app.infrastructure.health.redis_health_state_repository import RedisHealthStateRepository
from app.infrastructure.limits.redis_concurrency_limiter import RedisConcurrencyLimiter
from app.infrastructure.limits.redis_request_rate_limiter import RedisRequestRateLimiter


class FakeRedisClient:
    def __init__(self) -> None:
        self.storage: dict[str, str] = {}
        self.closed = False

    def get(self, key: str) -> str | None:
        return self.storage.get(key)

    def set(
        self,
        key: str,
        value: str,
        *,
        nx: bool = False,
        ex: int | None = None,
    ) -> bool:
        if nx and key in self.storage:
            return False
        self.storage[key] = value
        return True

    def delete(self, key: str) -> int:
        existed = key in self.storage
        self.storage.pop(key, None)
        return 1 if existed else 0

    def close(self) -> None:
        self.closed = True


def test_build_container_uses_redis_backed_runtime_state(
    monkeypatch,
) -> None:
    fake_redis = FakeRedisClient()
    monkeypatch.setattr(
        "app.infrastructure.bootstrap.container.Redis.from_url",
        lambda *args, **kwargs: fake_redis,
    )

    settings = AppSettings(
        config_path=Path("configs/example.router.yaml"),
        environment="test",
        log_level="WARNING",
        runtime_state_backend="redis",
        redis_url="redis://example.invalid:6379/0",
    )

    container = build_container(settings)

    assert container.redis_client is fake_redis
    assert isinstance(container.health_state_repository, RedisHealthStateRepository)
    assert isinstance(container.request_rate_limiter, RedisRequestRateLimiter)
    assert isinstance(container.concurrency_limiter, RedisConcurrencyLimiter)
