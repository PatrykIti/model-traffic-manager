from __future__ import annotations

from app.domain.value_objects.failure_classification import FailureReason
from app.domain.value_objects.health_state import HealthState, HealthStatus
from app.infrastructure.health.redis_health_state_repository import RedisHealthStateRepository


class FakeRedisClient:
    def __init__(self) -> None:
        self.storage: dict[str, str] = {}

    def get(self, key: str) -> str | None:
        return self.storage.get(key)

    def set(self, key: str, value: str) -> bool:
        self.storage[key] = value
        return True


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
