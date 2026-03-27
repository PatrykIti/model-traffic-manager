from __future__ import annotations

from app.domain.value_objects.failure_classification import FailureReason
from app.domain.value_objects.health_state import HealthState, HealthStatus
from app.infrastructure.health.redis_health_state_repository import RedisHealthStateRepository


class FakeRedisClient:
    def __init__(self) -> None:
        self.storage: dict[str, str] = {}

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


def test_redis_health_state_repository_serializes_and_loads_state() -> None:
    redis_client = FakeRedisClient()
    repository = RedisHealthStateRepository(redis_client=redis_client)
    repository.set_state(
        "deployment-a",
        "upstream-a",
        HealthState(
            status=HealthStatus.CIRCUIT_OPEN,
            consecutive_failures=3,
            circuit_open_until=220,
            last_failure_reason=FailureReason.UNHEALTHY,
        ),
    )

    states = repository.get_states("deployment-a", ("upstream-a",))

    assert states == {
        "upstream-a": HealthState(
            status=HealthStatus.CIRCUIT_OPEN,
            consecutive_failures=3,
            circuit_open_until=220,
            last_failure_reason=FailureReason.UNHEALTHY,
        )
    }


def test_redis_health_state_repository_tracks_half_open_probe_reservations() -> None:
    redis_client = FakeRedisClient()
    repository = RedisHealthStateRepository(redis_client=redis_client)

    assert repository.try_acquire_half_open_probe("deployment-a", "upstream-a", 30) is True
    assert repository.try_acquire_half_open_probe("deployment-a", "upstream-a", 30) is False

    repository.clear_half_open_probe("deployment-a", "upstream-a")

    assert repository.try_acquire_half_open_probe("deployment-a", "upstream-a", 30) is True
