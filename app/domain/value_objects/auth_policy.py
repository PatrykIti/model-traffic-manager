from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from app.domain.errors import DomainInvariantError


class AuthMode(StrEnum):
    MANAGED_IDENTITY = "managed_identity"
    API_KEY = "api_key"
    NONE = "none"


@dataclass(frozen=True, slots=True)
class AuthPolicy:
    mode: AuthMode
    scope: str | None = None
    client_id: str | None = None
    header_name: str | None = None
    secret_ref: str | None = None

    def __post_init__(self) -> None:
        if self.mode is AuthMode.MANAGED_IDENTITY:
            if not self.scope:
                raise DomainInvariantError("Managed Identity auth requires a scope.")
            if self.header_name or self.secret_ref:
                raise DomainInvariantError(
                    "Managed Identity auth must not define API key header or secret reference."
                )
            return

        if self.mode is AuthMode.API_KEY:
            if not self.header_name or not self.secret_ref:
                raise DomainInvariantError("API key auth requires both header_name and secret_ref.")
            if self.scope or self.client_id:
                raise DomainInvariantError("API key auth must not define Managed Identity fields.")
            return

        if self.scope or self.client_id or self.header_name or self.secret_ref:
            raise DomainInvariantError("Auth mode 'none' must not define auth material.")
