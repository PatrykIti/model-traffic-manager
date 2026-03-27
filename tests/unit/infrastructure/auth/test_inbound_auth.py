from __future__ import annotations

from datetime import UTC, datetime, timedelta

import httpx
import jwt
import pytest
import respx
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from app.domain.errors import InboundAuthenticationError, InboundAuthorizationError
from app.infrastructure.auth.env_secret_provider import EnvSecretProvider
from app.infrastructure.auth.inbound_auth import InboundAuthenticator
from app.infrastructure.config.models import InboundAuthConfigModel


def _generate_rsa_material() -> tuple[str, dict[str, object]]:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    numbers = public_key.public_numbers()

    def encode_int(value: int) -> str:
        import base64

        raw = value.to_bytes((value.bit_length() + 7) // 8, "big")
        return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")
    jwk = {
        "kty": "RSA",
        "use": "sig",
        "alg": "RS256",
        "kid": "test-key",
        "n": encode_int(numbers.n),
        "e": encode_int(numbers.e),
    }
    return private_pem, jwk


def _entra_config() -> InboundAuthConfigModel:
    return InboundAuthConfigModel.model_validate(
        {
            "providers": [
                {
                    "kind": "entra_id",
                    "tenant_id": "test-tenant",
                    "audiences": ["router-api-client-id", "api://router-api-client-id"],
                    "applications": [
                        {
                            "client_app_id": "client-app-id",
                            "display_name": "Bot System Backend",
                            "consumer_role": "bot-system-be",
                            "required_app_roles": ["invoke.router"],
                        }
                    ],
                }
            ]
        }
    )


def _api_token_config() -> InboundAuthConfigModel:
    return InboundAuthConfigModel.model_validate(
        {
            "providers": [
                {
                    "kind": "api_bearer_token",
                    "token_id": "bot-system-be-token",
                    "display_name": "Bot System Backend Token",
                    "consumer_role": "bot-system-be",
                    "secret_ref": "env://ROUTER_INBOUND_TEST_TOKEN",
                }
            ]
        }
    )


def _build_entra_token(private_pem: str, *, roles: list[str]) -> str:
    now = datetime.now(UTC)
    claims = {
        "iss": "https://login.microsoftonline.com/test-tenant/v2.0",
        "aud": "router-api-client-id",
        "azp": "client-app-id",
        "tid": "test-tenant",
        "roles": roles,
        "iat": int(now.timestamp()),
        "nbf": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=15)).timestamp()),
    }
    return jwt.encode(
        claims,
        private_pem,
        algorithm="RS256",
        headers={"kid": "test-key"},
    )


def test_inbound_authenticator_accepts_api_bearer_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ROUTER_INBOUND_TEST_TOKEN", "super-secret-token")
    authenticator = InboundAuthenticator.from_config(
        _api_token_config(),
        secret_provider=EnvSecretProvider(),
    )

    principal = authenticator.authenticate("Bearer super-secret-token")

    assert principal.auth_mode == "api_bearer_token"
    assert principal.principal_id == "bot-system-be-token"
    assert principal.client_consumer_role == "bot-system-be"


def test_inbound_authenticator_rejects_unknown_api_bearer_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ROUTER_INBOUND_TEST_TOKEN", "super-secret-token")
    authenticator = InboundAuthenticator.from_config(
        _api_token_config(),
        secret_provider=EnvSecretProvider(),
    )

    with pytest.raises(InboundAuthenticationError):
        authenticator.authenticate("Bearer wrong-token")


@respx.mock
def test_inbound_authenticator_accepts_entra_access_token() -> None:
    private_pem, jwk = _generate_rsa_material()
    respx.get(
        "https://login.microsoftonline.com/test-tenant/v2.0/.well-known/openid-configuration"
    ).mock(
        return_value=httpx.Response(
            200,
            json={
                "issuer": "https://login.microsoftonline.com/test-tenant/v2.0",
                "jwks_uri": "https://login.microsoftonline.com/test-tenant/discovery/v2.0/keys",
            },
        )
    )
    respx.get("https://login.microsoftonline.com/test-tenant/discovery/v2.0/keys").mock(
        return_value=httpx.Response(200, json={"keys": [jwk]})
    )
    authenticator = InboundAuthenticator.from_config(
        _entra_config(),
        secret_provider=EnvSecretProvider(),
    )

    principal = authenticator.authenticate(
        f"Bearer {_build_entra_token(private_pem, roles=['invoke.router'])}"
    )

    assert principal.auth_mode == "entra_id"
    assert principal.principal_id == "client-app-id"
    assert principal.client_consumer_role == "bot-system-be"
    assert principal.entra_roles == ("invoke.router",)


@respx.mock
def test_inbound_authenticator_rejects_entra_token_without_required_role() -> None:
    private_pem, jwk = _generate_rsa_material()
    respx.get(
        "https://login.microsoftonline.com/test-tenant/v2.0/.well-known/openid-configuration"
    ).mock(
        return_value=httpx.Response(
            200,
            json={
                "issuer": "https://login.microsoftonline.com/test-tenant/v2.0",
                "jwks_uri": "https://login.microsoftonline.com/test-tenant/discovery/v2.0/keys",
            },
        )
    )
    respx.get("https://login.microsoftonline.com/test-tenant/discovery/v2.0/keys").mock(
        return_value=httpx.Response(200, json={"keys": [jwk]})
    )
    authenticator = InboundAuthenticator.from_config(
        _entra_config(),
        secret_provider=EnvSecretProvider(),
    )

    with pytest.raises(InboundAuthorizationError):
        authenticator.authenticate(
            f"Bearer {_build_entra_token(private_pem, roles=['wrong.role'])}"
        )
