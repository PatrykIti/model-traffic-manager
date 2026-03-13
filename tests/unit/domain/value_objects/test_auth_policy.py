from __future__ import annotations

import pytest

from app.domain.errors import DomainInvariantError
from app.domain.value_objects.auth_policy import AuthMode, AuthPolicy


def test_managed_identity_requires_scope() -> None:
    with pytest.raises(DomainInvariantError):
        AuthPolicy(mode=AuthMode.MANAGED_IDENTITY)


def test_api_key_requires_header_and_secret() -> None:
    with pytest.raises(DomainInvariantError):
        AuthPolicy(mode=AuthMode.API_KEY, header_name="api-key")


def test_none_rejects_extra_auth_material() -> None:
    with pytest.raises(DomainInvariantError):
        AuthPolicy(mode=AuthMode.NONE, scope="https://example.com/.default")


def test_api_key_accepts_valid_data() -> None:
    policy = AuthPolicy(
        mode=AuthMode.API_KEY,
        header_name="api-key",
        secret_ref="secret://router/api-key",
    )

    assert policy.mode is AuthMode.API_KEY
    assert policy.header_name == "api-key"
