from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RequestPrincipal:
    auth_mode: str
    principal_type: str
    principal_id: str
    display_name: str
    client_consumer_role: str | None = None
    token_id: str | None = None
    entra_client_app_id: str | None = None
    entra_tenant_id: str | None = None
    entra_roles: tuple[str, ...] = ()
