from __future__ import annotations

import pytest

from app.domain.errors import SecretResolutionError, UnsupportedAuthModeError
from app.domain.value_objects.auth_policy import AuthMode, AuthPolicy
from app.infrastructure.auth.auth_header_builder import AuthHeaderBuilder


class FakeSecretProvider:
    def __init__(self, secrets: dict[str, str]) -> None:
        self._secrets = secrets

    def get_secret(self, secret_ref: str) -> str:
        if secret_ref not in self._secrets:
            raise SecretResolutionError(f"Secret '{secret_ref}' was not found.")
        return self._secrets[secret_ref]


class FakeTokenProvider:
    def __init__(self, token: str = "managed-identity-token") -> None:
        self._token = token
        self.calls: list[tuple[str, str | None]] = []

    def get_token(self, scope: str, client_id: str | None = None) -> str:
        self.calls.append((scope, client_id))
        return self._token


def test_auth_header_builder_returns_empty_headers_for_none() -> None:
    builder = AuthHeaderBuilder(secret_provider=FakeSecretProvider({}))

    assert builder.build(AuthPolicy(mode=AuthMode.NONE)) == {}


def test_auth_header_builder_builds_api_key_header() -> None:
    builder = AuthHeaderBuilder(
        secret_provider=FakeSecretProvider({"env://UPSTREAM_API_KEY": "top-secret"})
    )

    headers = builder.build(
        AuthPolicy(
            mode=AuthMode.API_KEY,
            header_name="api-key",
            secret_ref="env://UPSTREAM_API_KEY",
        )
    )

    assert headers == {"api-key": "top-secret"}


def test_auth_header_builder_builds_managed_identity_header() -> None:
    token_provider = FakeTokenProvider()
    builder = AuthHeaderBuilder(
        secret_provider=FakeSecretProvider({}),
        token_provider=token_provider,
    )

    headers = builder.build(
        AuthPolicy(
            mode=AuthMode.MANAGED_IDENTITY,
            scope="https://cognitiveservices.azure.com/.default",
            client_id="user-assigned-client-id",
        )
    )

    assert headers == {"Authorization": "Bearer managed-identity-token"}
    assert token_provider.calls == [
        ("https://cognitiveservices.azure.com/.default", "user-assigned-client-id")
    ]


def test_auth_header_builder_rejects_managed_identity_without_token_provider() -> None:
    builder = AuthHeaderBuilder(secret_provider=FakeSecretProvider({}))

    with pytest.raises(UnsupportedAuthModeError):
        builder.build(
            AuthPolicy(
                mode=AuthMode.MANAGED_IDENTITY,
                scope="https://cognitiveservices.azure.com/.default",
            )
        )
