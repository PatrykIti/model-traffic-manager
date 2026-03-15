from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from app.domain.errors import DomainInvariantError
from app.domain.value_objects.failure_classification import FailureReason


class HealthStatus(StrEnum):
    HEALTHY = "healthy"
    HALF_OPEN = "half_open"
    RATE_LIMITED = "rate_limited"
    QUOTA_EXHAUSTED = "quota_exhausted"
    COOLDOWN = "cooldown"
    UNHEALTHY = "unhealthy"
    CIRCUIT_OPEN = "circuit_open"


@dataclass(frozen=True, slots=True)
class HealthState:
    status: HealthStatus = HealthStatus.HEALTHY
    consecutive_failures: int = 0
    cooldown_until: int | None = None
    circuit_open_until: int | None = None
    last_failure_reason: FailureReason | None = None

    def __post_init__(self) -> None:
        if self.consecutive_failures < 0:
            raise DomainInvariantError(
                "Consecutive failures must be greater than or equal to zero."
            )
        if self.cooldown_until is not None and self.cooldown_until < 0:
            raise DomainInvariantError("Cooldown deadline must be greater than or equal to zero.")
        if self.circuit_open_until is not None and self.circuit_open_until < 0:
            raise DomainInvariantError(
                "Circuit-open deadline must be greater than or equal to zero."
            )

    def is_available(self) -> bool:
        return self.status in {HealthStatus.HEALTHY, HealthStatus.HALF_OPEN}
