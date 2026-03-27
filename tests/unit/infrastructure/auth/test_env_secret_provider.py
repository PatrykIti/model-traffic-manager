from __future__ import annotations

import pytest

from app.domain.errors import SecretResolutionError
from app.infrastructure.auth.env_secret_provider import EnvSecretProvider


def test_env_secret_provider_reads_env_secret(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("UPSTREAM_API_KEY", "secret-value")

    provider = EnvSecretProvider()

    assert provider.get_secret("env://UPSTREAM_API_KEY") == "secret-value"


def test_env_secret_provider_rejects_non_env_secret_ref() -> None:
    provider = EnvSecretProvider()

    with pytest.raises(SecretResolutionError):
        provider.get_secret("keyvault://secret-name")


def test_env_secret_provider_rejects_missing_env_var() -> None:
    provider = EnvSecretProvider()

    with pytest.raises(SecretResolutionError):
        provider.get_secret("env://MISSING_SECRET")
