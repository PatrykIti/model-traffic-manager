from __future__ import annotations

import time
from collections.abc import Callable

from azure.core.credentials import AccessToken, TokenCredential
from azure.identity import DefaultAzureCredential

from app.application.ports.token_provider import TokenProvider
from app.domain.errors import TokenAcquisitionError
from app.domain.value_objects.auth_policy import AuthMode


class ManagedIdentityTokenProvider(TokenProvider):
    def __init__(
        self,
        credential_factory: Callable[[str | None], TokenCredential] | None = None,
        refresh_buffer_seconds: int = 60,
        now_provider: Callable[[], int] | None = None,
    ) -> None:
        self._credential_factory = credential_factory or self._build_default_credential
        self._refresh_buffer_seconds = refresh_buffer_seconds
        self._now_provider = now_provider or (lambda: int(time.time()))
        self._credentials: dict[str | None, TokenCredential] = {}
        self._token_cache: dict[tuple[str, str | None, str], AccessToken] = {}

    def get_token(self, scope: str, client_id: str | None = None) -> str:
        cache_key = (AuthMode.MANAGED_IDENTITY.value, client_id, scope)
        cached_token = self._token_cache.get(cache_key)
        if cached_token is not None and self._is_reusable(cached_token):
            return cached_token.token

        credential = self._credentials.get(client_id)
        if credential is None:
            credential = self._credential_factory(client_id)
            self._credentials[client_id] = credential

        try:
            token = credential.get_token(scope)
        except Exception as exc:  # pragma: no cover - defensive wrapper for SDK errors
            raise TokenAcquisitionError(
                f"Failed to acquire Managed Identity token for scope '{scope}'."
            ) from exc

        self._token_cache[cache_key] = token
        return token.token

    def _is_reusable(self, token: AccessToken) -> bool:
        return token.expires_on - self._refresh_buffer_seconds > self._now_provider()

    @staticmethod
    def _build_default_credential(client_id: str | None) -> TokenCredential:
        return DefaultAzureCredential(managed_identity_client_id=client_id)
