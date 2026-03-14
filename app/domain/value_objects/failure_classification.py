from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from app.domain.errors import DomainInvariantError


class FailureReason(StrEnum):
    TIMEOUT = "timeout"
    NETWORK_ERROR = "network_error"
    RATE_LIMITED = "rate_limited"
    QUOTA_EXHAUSTED = "quota_exhausted"
    UNHEALTHY = "unhealthy"
    NON_RETRIABLE = "non_retriable"


@dataclass(frozen=True, slots=True)
class FailureClassification:
    reason: FailureReason
    retriable: bool
    retry_after_seconds: int | None = None

    def __post_init__(self) -> None:
        if self.retry_after_seconds is not None and self.retry_after_seconds < 0:
            raise DomainInvariantError("Retry-After seconds must be greater than or equal to zero.")
