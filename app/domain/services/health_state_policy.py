from __future__ import annotations

import time
from collections.abc import Callable

from app.domain.value_objects.failure_classification import FailureClassification, FailureReason
from app.domain.value_objects.health_state import HealthState, HealthStatus


class HealthStatePolicy:
    def __init__(
        self,
        failure_threshold: int,
        cooldown_seconds: int,
        half_open_after_seconds: int,
        now_provider: Callable[[], int] | None = None,
    ) -> None:
        self._failure_threshold = failure_threshold
        self._cooldown_seconds = cooldown_seconds
        self._half_open_after_seconds = half_open_after_seconds
        self._now_provider = now_provider or (lambda: int(time.time()))

    def normalize(self, state: HealthState) -> HealthState:
        now = self._now_provider()
        if (
            state.status
            in {
                HealthStatus.RATE_LIMITED,
                HealthStatus.QUOTA_EXHAUSTED,
                HealthStatus.COOLDOWN,
                HealthStatus.UNHEALTHY,
            }
            and state.cooldown_until is not None
            and state.cooldown_until <= now
        ):
            return HealthState(
                status=HealthStatus.HEALTHY,
                consecutive_failures=state.consecutive_failures,
                last_failure_reason=state.last_failure_reason,
            )

        if (
            state.status is HealthStatus.CIRCUIT_OPEN
            and state.circuit_open_until is not None
            and state.circuit_open_until <= now
        ):
            return HealthState(
                status=HealthStatus.HEALTHY,
                consecutive_failures=state.consecutive_failures,
                last_failure_reason=state.last_failure_reason,
            )

        return state

    def record_success(self, state: HealthState) -> HealthState:
        _ = self.normalize(state)
        return HealthState(status=HealthStatus.HEALTHY, consecutive_failures=0)

    def record_failure(
        self,
        state: HealthState,
        failure: FailureClassification,
    ) -> HealthState:
        normalized_state = self.normalize(state)
        now = self._now_provider()

        if failure.reason is FailureReason.RATE_LIMITED:
            cooldown_until = now + (
                failure.retry_after_seconds
                if failure.retry_after_seconds is not None
                else self._cooldown_seconds
            )
            return HealthState(
                status=HealthStatus.RATE_LIMITED,
                consecutive_failures=normalized_state.consecutive_failures,
                cooldown_until=cooldown_until,
                last_failure_reason=failure.reason,
            )

        if failure.reason is FailureReason.QUOTA_EXHAUSTED:
            return HealthState(
                status=HealthStatus.QUOTA_EXHAUSTED,
                consecutive_failures=normalized_state.consecutive_failures,
                cooldown_until=now + self._cooldown_seconds,
                last_failure_reason=failure.reason,
            )

        if failure.reason in {
            FailureReason.TIMEOUT,
            FailureReason.NETWORK_ERROR,
            FailureReason.UNHEALTHY,
        }:
            consecutive_failures = normalized_state.consecutive_failures + 1
            if consecutive_failures >= self._failure_threshold:
                return HealthState(
                    status=HealthStatus.CIRCUIT_OPEN,
                    consecutive_failures=consecutive_failures,
                    circuit_open_until=now + self._half_open_after_seconds,
                    last_failure_reason=failure.reason,
                )

            return HealthState(
                status=HealthStatus.UNHEALTHY,
                consecutive_failures=consecutive_failures,
                cooldown_until=now + self._cooldown_seconds,
                last_failure_reason=failure.reason,
            )

        return normalized_state
