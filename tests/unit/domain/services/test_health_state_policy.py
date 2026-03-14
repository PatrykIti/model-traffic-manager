from __future__ import annotations

from app.domain.services.health_state_policy import HealthStatePolicy
from app.domain.value_objects.failure_classification import FailureClassification, FailureReason
from app.domain.value_objects.health_state import HealthState, HealthStatus


def test_record_success_resets_state_to_healthy() -> None:
    policy = HealthStatePolicy(
        failure_threshold=3,
        cooldown_seconds=30,
        half_open_after_seconds=60,
        now_provider=lambda: 100,
    )

    state = policy.record_success(
        HealthState(
            status=HealthStatus.CIRCUIT_OPEN,
            consecutive_failures=3,
            circuit_open_until=160,
        )
    )

    assert state == HealthState(status=HealthStatus.HEALTHY, consecutive_failures=0)


def test_record_rate_limited_failure_sets_cooldown() -> None:
    policy = HealthStatePolicy(
        failure_threshold=3,
        cooldown_seconds=30,
        half_open_after_seconds=60,
        now_provider=lambda: 100,
    )

    state = policy.record_failure(
        HealthState(),
        FailureClassification(
            reason=FailureReason.RATE_LIMITED,
            retriable=True,
            retry_after_seconds=45,
        ),
    )

    assert state.status is HealthStatus.RATE_LIMITED
    assert state.cooldown_until == 145
    assert state.last_failure_reason is FailureReason.RATE_LIMITED


def test_record_unhealthy_failure_opens_circuit_at_threshold() -> None:
    policy = HealthStatePolicy(
        failure_threshold=2,
        cooldown_seconds=30,
        half_open_after_seconds=60,
        now_provider=lambda: 100,
    )

    first = policy.record_failure(
        HealthState(),
        FailureClassification(reason=FailureReason.UNHEALTHY, retriable=True),
    )
    second = policy.record_failure(
        first,
        FailureClassification(reason=FailureReason.NETWORK_ERROR, retriable=True),
    )

    assert first.status is HealthStatus.UNHEALTHY
    assert first.consecutive_failures == 1
    assert first.cooldown_until == 130
    assert second.status is HealthStatus.CIRCUIT_OPEN
    assert second.consecutive_failures == 2
    assert second.circuit_open_until == 160


def test_normalize_recovers_expired_states() -> None:
    policy = HealthStatePolicy(
        failure_threshold=2,
        cooldown_seconds=30,
        half_open_after_seconds=60,
        now_provider=lambda: 200,
    )

    rate_limited = policy.normalize(
        HealthState(
            status=HealthStatus.RATE_LIMITED,
            consecutive_failures=1,
            cooldown_until=150,
            last_failure_reason=FailureReason.RATE_LIMITED,
        )
    )
    circuit_open = policy.normalize(
        HealthState(
            status=HealthStatus.CIRCUIT_OPEN,
            consecutive_failures=2,
            circuit_open_until=190,
            last_failure_reason=FailureReason.UNHEALTHY,
        )
    )

    assert rate_limited.status is HealthStatus.HEALTHY
    assert rate_limited.consecutive_failures == 1
    assert circuit_open.status is HealthStatus.HEALTHY
    assert circuit_open.consecutive_failures == 2
