from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from app.domain.errors import DomainInvariantError


class HealthStatus(StrEnum):
    HEALTHY = "healthy"
    RATE_LIMITED = "rate_limited"
    QUOTA_EXHAUSTED = "quota_exhausted"
    COOLDOWN = "cooldown"
    UNHEALTHY = "unhealthy"
    CIRCUIT_OPEN = "circuit_open"


@dataclass(frozen=True, slots=True)
class HealthState:
    status: HealthStatus = HealthStatus.HEALTHY
    consecutive_failures: int = 0

    def __post_init__(self) -> None:
        if self.consecutive_failures < 0:
            raise DomainInvariantError(
                "Consecutive failures must be greater than or equal to zero."
            )

    def is_available(self) -> bool:
        return self.status is HealthStatus.HEALTHY
