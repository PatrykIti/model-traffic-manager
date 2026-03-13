from __future__ import annotations

from app.application.ports.secret_provider import SecretProvider
from app.domain.errors import UnsupportedAuthModeError
from app.domain.value_objects.auth_policy import AuthMode, AuthPolicy


class AuthHeaderBuilder:
    def __init__(self, secret_provider: SecretProvider) -> None:
        self._secret_provider = secret_provider

    def build(self, auth_policy: AuthPolicy) -> dict[str, str]:
        if auth_policy.mode is AuthMode.NONE:
            return {}

        if auth_policy.mode is AuthMode.API_KEY:
            secret = self._secret_provider.get_secret(auth_policy.secret_ref or "")
            return {auth_policy.header_name or "api-key": secret}

        raise UnsupportedAuthModeError(
            "Managed Identity auth is not implemented in Phase 2."
        )
