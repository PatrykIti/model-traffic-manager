from __future__ import annotations

from app.application.ports.secret_provider import SecretProvider
from app.application.ports.token_provider import TokenProvider
from app.domain.errors import UnsupportedAuthModeError
from app.domain.value_objects.auth_policy import AuthMode, AuthPolicy


class AuthHeaderBuilder:
    def __init__(
        self,
        secret_provider: SecretProvider,
        token_provider: TokenProvider | None = None,
    ) -> None:
        self._secret_provider = secret_provider
        self._token_provider = token_provider

    def build(self, auth_policy: AuthPolicy) -> dict[str, str]:
        if auth_policy.mode is AuthMode.NONE:
            return {}

        if auth_policy.mode is AuthMode.API_KEY:
            secret = self._secret_provider.get_secret(auth_policy.secret_ref or "")
            return {auth_policy.header_name or "api-key": secret}

        if self._token_provider is None:
            raise UnsupportedAuthModeError(
                "Managed Identity auth is not available because no token provider is configured."
            )

        token = self._token_provider.get_token(
            scope=auth_policy.scope or "",
            client_id=auth_policy.client_id,
        )
        return {"Authorization": f"Bearer {token}"}
