from __future__ import annotations

import os

import pytest

from app.domain.value_objects.auth_policy import AuthMode, AuthPolicy
from app.infrastructure.auth.auth_header_builder import AuthHeaderBuilder
from app.infrastructure.auth.managed_identity_token_provider import ManagedIdentityTokenProvider


def _require_integration_azure() -> None:
    if os.getenv("RUN_INTEGRATION_AZURE") != "1":
        pytest.skip("integration-azure is only enabled in the dedicated Azure workflow")


class UnusedSecretProvider:
    def get_secret(self, secret_ref: str) -> str:  # pragma: no cover - defensive stub
        raise AssertionError("Secret provider should not be used for managed_identity")


def test_managed_identity_token_provider_gets_real_token() -> None:
    _require_integration_azure()
    scope = os.environ["INTEGRATION_AZURE_SCOPE"]

    provider = ManagedIdentityTokenProvider()
    first = provider.get_token(scope)
    second = provider.get_token(scope)

    assert first
    assert second
    assert first == second


def test_auth_header_builder_uses_live_azure_token() -> None:
    _require_integration_azure()
    scope = os.environ["INTEGRATION_AZURE_SCOPE"]

    builder = AuthHeaderBuilder(
        secret_provider=UnusedSecretProvider(),
        token_provider=ManagedIdentityTokenProvider(),
    )

    headers = builder.build(
        AuthPolicy(
            mode=AuthMode.MANAGED_IDENTITY,
            scope=scope,
        )
    )

    assert headers["Authorization"].startswith("Bearer ")
