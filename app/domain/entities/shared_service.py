from __future__ import annotations

from dataclasses import dataclass

from app.domain.errors import DomainInvariantError
from app.domain.value_objects.auth_policy import AuthPolicy


@dataclass(frozen=True, slots=True)
class SharedService:
    name: str
    endpoint: str
    auth: AuthPolicy

    def __post_init__(self) -> None:
        if not self.name:
            raise DomainInvariantError("Shared-service name must not be empty.")
        if not self.endpoint:
            raise DomainInvariantError("Shared-service endpoint must not be empty.")
