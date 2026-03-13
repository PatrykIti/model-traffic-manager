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


def test_auth_header_builder_rejects_managed_identity_in_phase_2() -> None:
    builder = AuthHeaderBuilder(secret_provider=FakeSecretProvider({}))

    with pytest.raises(UnsupportedAuthModeError):
        builder.build(
            AuthPolicy(
                mode=AuthMode.MANAGED_IDENTITY,
                scope="https://cognitiveservices.azure.com/.default",
            )
        )
