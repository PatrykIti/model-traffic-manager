from __future__ import annotations

import pytest

from app.domain.errors import DomainInvariantError
from app.domain.value_objects.health_state import HealthState, HealthStatus


def test_healthy_state_is_available() -> None:
    state = HealthState()

    assert state.status is HealthStatus.HEALTHY
    assert state.is_available() is True


def test_non_healthy_state_is_not_available() -> None:
    state = HealthState(status=HealthStatus.CIRCUIT_OPEN, consecutive_failures=2)

    assert state.is_available() is False


def test_half_open_state_is_available_for_probe_selection() -> None:
    state = HealthState(status=HealthStatus.HALF_OPEN, consecutive_failures=2)

    assert state.is_available() is True


def test_consecutive_failures_must_be_non_negative() -> None:
    with pytest.raises(DomainInvariantError):
        HealthState(consecutive_failures=-1)


def test_deadlines_must_be_non_negative() -> None:
    with pytest.raises(DomainInvariantError):
        HealthState(cooldown_until=-1)

    with pytest.raises(DomainInvariantError):
        HealthState(circuit_open_until=-1)
