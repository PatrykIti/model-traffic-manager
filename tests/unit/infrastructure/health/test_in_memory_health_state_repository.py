from __future__ import annotations

from app.domain.value_objects.failure_classification import FailureReason
from app.domain.value_objects.health_state import HealthState, HealthStatus
from app.infrastructure.health.in_memory_health_state_repository import (
    InMemoryHealthStateRepository,
)


def test_in_memory_health_state_repository_stores_and_loads_states() -> None:
    repository = InMemoryHealthStateRepository()
    repository.set_state(
        "deployment-a",
        "upstream-a",
        HealthState(
            status=HealthStatus.RATE_LIMITED,
            cooldown_until=160,
            last_failure_reason=FailureReason.RATE_LIMITED,
        ),
    )

    states = repository.get_states("deployment-a", ("upstream-a", "upstream-b"))

    assert states == {
        "upstream-a": HealthState(
            status=HealthStatus.RATE_LIMITED,
            cooldown_until=160,
            last_failure_reason=FailureReason.RATE_LIMITED,
        )
    }
