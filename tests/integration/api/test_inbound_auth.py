from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

import httpx
import jwt
import pytest
import respx
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient

from app.entrypoints.api.main import create_app
from app.infrastructure.config.settings import AppSettings


def _settings(config_path: Path) -> AppSettings:
    return AppSettings(config_path=config_path, environment="test", log_level="WARNING")


def _private_key() -> tuple[str, dict[str, object]]:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    numbers = public_key.public_numbers()

    def _b64(value: int) -> str:
        import base64

        raw = value.to_bytes((value.bit_length() + 7) // 8, "big")
        return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")
    return private_pem, {
        "kty": "RSA",
        "use": "sig",
        "alg": "RS256",
        "kid": "test-key",
        "n": _b64(numbers.n),
        "e": _b64(numbers.e),
    }


def _entra_token(private_pem: str, *, roles: list[str]) -> str:
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
    return jwt.encode(claims, private_pem, algorithm="RS256", headers={"kid": "test-key"})


def test_chat_route_rejects_missing_inbound_bearer_token(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ROUTER_INBOUND_TOKEN", "super-secret-token")
    config_path = tmp_path / "router.yaml"
    config_path.write_text(
        """
router:
  instance_name: inbound-auth-api-token-test
  timeout_ms: 30000
  max_attempts: 3
  retryable_status_codes: [429, 500, 502, 503, 504]
  health:
    failure_threshold: 3
    cooldown_seconds: 30
    half_open_after_seconds: 60
  inbound_auth:
    providers:
      - kind: api_bearer_token
        token_id: bot-system-be-token
        display_name: Bot System Backend Token
        consumer_role: bot-system-be
        secret_ref: env://ROUTER_INBOUND_TOKEN

deployments:
  - id: local-health-check
    kind: llm
    protocol: openai_chat
    routing:
      strategy: tiered_failover
    limits:
      max_concurrency: 10
      request_rate_per_second: 5
    upstreams:
      - id: local-upstream
        provider: internal_mock
        account: local
        region: local
        tier: 0
        weight: 100
        endpoint: https://example.invalid/openai/deployments/local-health-check/chat/completions
        auth:
          mode: none

shared_services: {}
""".strip(),
        encoding="utf-8",
    )

    app = create_app(_settings(config_path))
    with TestClient(app) as client:
        response = client.post(
            "/v1/chat/completions/local-health-check",
            json={"messages": [{"role": "user", "content": "Hello"}]},
        )

    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"


def test_deployments_route_is_protected_when_inbound_auth_is_enabled(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ROUTER_INBOUND_TOKEN", "super-secret-token")
    config_path = tmp_path / "router.yaml"
    config_path.write_text(
        """
router:
  instance_name: inbound-auth-deployments-test
  timeout_ms: 30000
  max_attempts: 3
  retryable_status_codes: [429, 500, 502, 503, 504]
  health:
    failure_threshold: 3
    cooldown_seconds: 30
    half_open_after_seconds: 60
  inbound_auth:
    providers:
      - kind: api_bearer_token
        token_id: bot-system-be-token
        display_name: Bot System Backend Token
        consumer_role: bot-system-be
        secret_ref: env://ROUTER_INBOUND_TOKEN

deployments:
  - id: local-health-check
    kind: llm
    protocol: openai_chat
    routing:
      strategy: tiered_failover
    limits:
      max_concurrency: 10
      request_rate_per_second: 5
    upstreams:
      - id: local-upstream
        provider: internal_mock
        account: local
        region: local
        tier: 0
        weight: 100
        endpoint: https://example.invalid/openai/deployments/local-health-check/chat/completions
        auth:
          mode: none

shared_services: {}
""".strip(),
        encoding="utf-8",
    )

    app = create_app(_settings(config_path))
    with TestClient(app) as client:
        response = client.get("/deployments")

    assert response.status_code == 401


def test_health_routes_remain_open_when_inbound_auth_is_enabled(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ROUTER_INBOUND_TOKEN", "super-secret-token")
    config_path = tmp_path / "router.yaml"
    config_path.write_text(
        """
router:
  instance_name: inbound-auth-health-open-test
  timeout_ms: 30000
  max_attempts: 3
  retryable_status_codes: [429, 500, 502, 503, 504]
  health:
    failure_threshold: 3
    cooldown_seconds: 30
    half_open_after_seconds: 60
  inbound_auth:
    providers:
      - kind: api_bearer_token
        token_id: bot-system-be-token
        display_name: Bot System Backend Token
        consumer_role: bot-system-be
        secret_ref: env://ROUTER_INBOUND_TOKEN

deployments:
  - id: local-health-check
    kind: llm
    protocol: openai_chat
    routing:
      strategy: tiered_failover
    limits:
      max_concurrency: 10
      request_rate_per_second: 5
    upstreams:
      - id: local-upstream
        provider: internal_mock
        account: local
        region: local
        tier: 0
        weight: 100
        endpoint: https://example.invalid/openai/deployments/local-health-check/chat/completions
        auth:
          mode: none

shared_services: {}
""".strip(),
        encoding="utf-8",
    )

    app = create_app(_settings(config_path))
    with TestClient(app) as client:
        response = client.get("/health/ready")

    assert response.status_code == 200


@respx.mock
def test_chat_route_accepts_valid_inbound_bearer_token(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ROUTER_INBOUND_TOKEN", "super-secret-token")
    config_path = tmp_path / "router.yaml"
    config_path.write_text(
        """
router:
  instance_name: inbound-auth-api-token-success
  timeout_ms: 30000
  max_attempts: 3
  retryable_status_codes: [429, 500, 502, 503, 504]
  health:
    failure_threshold: 3
    cooldown_seconds: 30
    half_open_after_seconds: 60
  inbound_auth:
    providers:
      - kind: api_bearer_token
        token_id: bot-system-be-token
        display_name: Bot System Backend Token
        consumer_role: bot-system-be
        secret_ref: env://ROUTER_INBOUND_TOKEN

deployments:
  - id: local-health-check
    kind: llm
    protocol: openai_chat
    routing:
      strategy: tiered_failover
    limits:
      max_concurrency: 10
      request_rate_per_second: 5
    upstreams:
      - id: local-upstream
        provider: internal_mock
        account: local
        region: local
        tier: 0
        weight: 100
        endpoint: https://example.invalid/openai/deployments/local-health-check/chat/completions
        auth:
          mode: none

shared_services: {}
""".strip(),
        encoding="utf-8",
    )
    respx.post(
        "https://example.invalid/openai/deployments/local-health-check/chat/completions"
    ).mock(return_value=httpx.Response(200, json={"id": "chatcmpl-123", "choices": []}))

    app = create_app(_settings(config_path))
    with TestClient(app) as client:
        response = client.post(
            "/v1/chat/completions/local-health-check",
            headers={"Authorization": "Bearer super-secret-token"},
            json={"messages": [{"role": "user", "content": "Hello"}]},
        )

    assert response.status_code == 200


@respx.mock
def test_chat_route_accepts_valid_entra_access_token(tmp_path: Path) -> None:
    private_pem, jwk = _private_key()
    config_path = tmp_path / "router.yaml"
    config_path.write_text(
        """
router:
  instance_name: inbound-auth-entra-success
  timeout_ms: 30000
  max_attempts: 3
  retryable_status_codes: [429, 500, 502, 503, 504]
  health:
    failure_threshold: 3
    cooldown_seconds: 30
    half_open_after_seconds: 60
  inbound_auth:
    providers:
      - kind: entra_id
        tenant_id: test-tenant
        audiences: [router-api-client-id]
        applications:
          - client_app_id: client-app-id
            display_name: Bot System Backend
            consumer_role: bot-system-be
            required_app_roles: [invoke.router]

deployments:
  - id: local-health-check
    kind: llm
    protocol: openai_chat
    routing:
      strategy: tiered_failover
    limits:
      max_concurrency: 10
      request_rate_per_second: 5
    upstreams:
      - id: local-upstream
        provider: internal_mock
        account: local
        region: local
        tier: 0
        weight: 100
        endpoint: https://example.invalid/openai/deployments/local-health-check/chat/completions
        auth:
          mode: none

shared_services: {}
""".strip(),
        encoding="utf-8",
    )
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
    respx.post(
        "https://example.invalid/openai/deployments/local-health-check/chat/completions"
    ).mock(return_value=httpx.Response(200, json={"id": "chatcmpl-123", "choices": []}))

    app = create_app(_settings(config_path))
    with TestClient(app) as client:
        token = _entra_token(private_pem, roles=["invoke.router"])
        response = client.post(
            "/v1/chat/completions/local-health-check",
            headers={"Authorization": f"Bearer {token}"},
            json={"messages": [{"role": "user", "content": "Hello"}]},
        )

    assert response.status_code == 200


@respx.mock
def test_chat_route_rejects_entra_access_token_without_required_role(tmp_path: Path) -> None:
    private_pem, jwk = _private_key()
    config_path = tmp_path / "router.yaml"
    config_path.write_text(
        """
router:
  instance_name: inbound-auth-entra-forbidden
  timeout_ms: 30000
  max_attempts: 3
  retryable_status_codes: [429, 500, 502, 503, 504]
  health:
    failure_threshold: 3
    cooldown_seconds: 30
    half_open_after_seconds: 60
  inbound_auth:
    providers:
      - kind: entra_id
        tenant_id: test-tenant
        audiences: [router-api-client-id]
        applications:
          - client_app_id: client-app-id
            display_name: Bot System Backend
            consumer_role: bot-system-be
            required_app_roles: [invoke.router]

deployments:
  - id: local-health-check
    kind: llm
    protocol: openai_chat
    routing:
      strategy: tiered_failover
    limits:
      max_concurrency: 10
      request_rate_per_second: 5
    upstreams:
      - id: local-upstream
        provider: internal_mock
        account: local
        region: local
        tier: 0
        weight: 100
        endpoint: https://example.invalid/openai/deployments/local-health-check/chat/completions
        auth:
          mode: none

shared_services: {}
""".strip(),
        encoding="utf-8",
    )
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

    app = create_app(_settings(config_path))
    with TestClient(app) as client:
        response = client.post(
            "/v1/chat/completions/local-health-check",
            headers={"Authorization": f"Bearer {_entra_token(private_pem, roles=['wrong.role'])}"},
            json={"messages": [{"role": "user", "content": "Hello"}]},
        )

    assert response.status_code == 403
