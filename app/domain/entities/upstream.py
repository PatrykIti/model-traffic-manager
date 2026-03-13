from __future__ import annotations

from dataclasses import dataclass

from app.domain.errors import DomainInvariantError
from app.domain.value_objects.auth_policy import AuthPolicy


@dataclass(frozen=True, slots=True)
class Upstream:
    id: str
    provider: str
    account: str
    region: str
    tier: int
    weight: int
    endpoint: str
    auth: AuthPolicy

    def __post_init__(self) -> None:
        if not self.id:
            raise DomainInvariantError("Upstream ID must not be empty.")
        if not self.provider:
            raise DomainInvariantError("Upstream provider must not be empty.")
        if not self.account:
            raise DomainInvariantError("Upstream account must not be empty.")
        if not self.region:
            raise DomainInvariantError("Upstream region must not be empty.")
        if not self.endpoint:
            raise DomainInvariantError("Upstream endpoint must not be empty.")
        if self.tier < 0:
            raise DomainInvariantError("Upstream tier must be greater than or equal to zero.")
        if self.weight <= 0:
            raise DomainInvariantError("Upstream weight must be greater than zero.")
