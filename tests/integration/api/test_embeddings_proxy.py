from __future__ import annotations

from pathlib import Path

import httpx
import pytest
import respx
from fastapi.testclient import TestClient

from app.entrypoints.api.main import create_app
from app.infrastructure.config.settings import AppSettings


def build_settings(config_path: Path) -> AppSettings:
    return AppSettings(config_path=config_path, environment="test", log_level="WARNING")


@respx.mock
def test_embeddings_proxy_success_passthrough() -> None:
    respx.post(
        "https://example.invalid/openai/deployments/local-embeddings-check/embeddings"
    ).mock(
        return_value=httpx.Response(
            200,
            json={"data": [{"embedding": [0.1, 0.2, 0.3], "index": 0}]},
        )
    )

    app = create_app()
    with TestClient(app) as client:
        response = client.post(
            "/v1/embeddings/local-embeddings-check",
            json={"input": "Hello"},
        )

    assert response.status_code == 200
    assert response.json() == {"data": [{"embedding": [0.1, 0.2, 0.3], "index": 0}]}


def test_embeddings_proxy_returns_404_when_deployment_is_missing() -> None:
    app = create_app()
    with TestClient(app) as client:
        response = client.post(
            "/v1/embeddings/missing-deployment",
            json={"input": "Hello"},
        )

    assert response.status_code == 404
    assert "missing-deployment" in response.json()["detail"]


@respx.mock
def test_embeddings_proxy_maps_connection_error_to_502() -> None:
    request = httpx.Request(
        "POST",
        "https://example.invalid/openai/deployments/local-embeddings-check/embeddings",
    )
    respx.post(
        "https://example.invalid/openai/deployments/local-embeddings-check/embeddings"
    ).mock(side_effect=httpx.ConnectError("connect failed", request=request))

    app = create_app()
    with TestClient(app) as client:
        response = client.post(
            "/v1/embeddings/local-embeddings-check",
            json={"input": "Hello"},
        )

    assert response.status_code == 502


@respx.mock
def test_embeddings_proxy_supports_api_key_from_env(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("UPSTREAM_API_KEY", "phase-2-secret")

    config_path = tmp_path / "router.yaml"
    config_path.write_text(
        """
router:
  instance_name: api-key-test
  timeout_ms: 30000
  max_attempts: 3
  retryable_status_codes: [429, 500, 502, 503, 504]
  health:
    failure_threshold: 3
    cooldown_seconds: 30
    half_open_after_seconds: 60

deployments:
  - id: api-key-embeddings
    kind: embeddings
    protocol: openai_embeddings
    routing:
      strategy: tiered_failover
    limits:
      max_concurrency: 10
      request_rate_per_second: 5
    upstreams:
      - id: upstream-api-key
        provider: external_openai
        account: local
        region: local
        tier: 0
        weight: 100
        endpoint: https://example.invalid/embeddings
        auth:
          mode: api_key
          header_name: api-key
          secret_ref: env://UPSTREAM_API_KEY

shared_services: {}
""".strip(),
        encoding="utf-8",
    )

    route = respx.post("https://example.invalid/embeddings").mock(
        return_value=httpx.Response(200, json={"data": [{"embedding": [0.4, 0.5]}]})
    )

    app = create_app(build_settings(config_path))
    with TestClient(app) as client:
        response = client.post(
            "/v1/embeddings/api-key-embeddings",
            json={"input": "Hello"},
        )

    assert response.status_code == 200
    assert response.json() == {"data": [{"embedding": [0.4, 0.5]}]}
    assert route.calls[0].request.headers["api-key"] == "phase-2-secret"


@respx.mock
def test_embeddings_proxy_supports_managed_identity_with_stub_token_provider(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeTokenProvider:
        def get_token(self, scope: str, client_id: str | None = None) -> str:
            assert scope == "https://cognitiveservices.azure.com/.default"
            assert client_id == "user-assigned-client-id"
            return "managed-identity-token"

    config_path = tmp_path / "router.yaml"
    config_path.write_text(
        """
router:
  instance_name: managed-identity-test
  timeout_ms: 30000
  max_attempts: 3
  retryable_status_codes: [429, 500, 502, 503, 504]
  health:
    failure_threshold: 3
    cooldown_seconds: 30
    half_open_after_seconds: 60

deployments:
  - id: managed-identity-embeddings
    kind: embeddings
    protocol: openai_embeddings
    routing:
      strategy: tiered_failover
    limits:
      max_concurrency: 10
      request_rate_per_second: 5
    upstreams:
      - id: upstream-managed-identity
        provider: azure_openai
        account: local
        region: local
        tier: 0
        weight: 100
        endpoint: https://example.invalid/embeddings
        auth:
          mode: managed_identity
          scope: https://cognitiveservices.azure.com/.default
          client_id: user-assigned-client-id

shared_services: {}
""".strip(),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "app.infrastructure.bootstrap.container.ManagedIdentityTokenProvider",
        lambda: FakeTokenProvider(),
    )
    route = respx.post("https://example.invalid/embeddings").mock(
        return_value=httpx.Response(200, json={"data": [{"embedding": [0.6, 0.7]}]})
    )

    app = create_app(build_settings(config_path))
    with TestClient(app) as client:
        response = client.post(
            "/v1/embeddings/managed-identity-embeddings",
            json={"input": "Hello"},
        )

    assert response.status_code == 200
    assert response.json() == {"data": [{"embedding": [0.6, 0.7]}]}
    assert route.calls[0].request.headers["authorization"] == "Bearer managed-identity-token"


@respx.mock
def test_embeddings_proxy_retries_within_primary_tier_before_succeeding(tmp_path: Path) -> None:
    config_path = tmp_path / "router.yaml"
    config_path.write_text(
        """
router:
  instance_name: failover-test
  timeout_ms: 30000
  max_attempts: 3
  retryable_status_codes: [429, 500, 502, 503, 504]
  health:
    failure_threshold: 3
    cooldown_seconds: 30
    half_open_after_seconds: 60

deployments:
  - id: failover-embeddings
    kind: embeddings
    protocol: openai_embeddings
    routing:
      strategy: tiered_failover
    limits:
      max_concurrency: 10
      request_rate_per_second: 5
    upstreams:
      - id: upstream-primary-a
        provider: internal_mock
        account: local
        region: local
        tier: 0
        weight: 100
        endpoint: https://example.invalid/embeddings-primary-a
        auth:
          mode: none
      - id: upstream-primary-b
        provider: internal_mock
        account: local
        region: local
        tier: 0
        weight: 100
        endpoint: https://example.invalid/embeddings-primary-b
        auth:
          mode: none

shared_services: {}
""".strip(),
        encoding="utf-8",
    )

    respx.post("https://example.invalid/embeddings-primary-a").mock(
        return_value=httpx.Response(503, json={"error": "retry"})
    )
    fallback_route = respx.post("https://example.invalid/embeddings-primary-b").mock(
        return_value=httpx.Response(200, json={"data": [{"embedding": [0.8, 0.9]}]})
    )

    app = create_app(build_settings(config_path))
    with TestClient(app) as client:
        response = client.post(
            "/v1/embeddings/failover-embeddings",
            json={"input": "Hello"},
        )

    assert response.status_code == 200
    assert response.json() == {"data": [{"embedding": [0.8, 0.9]}]}
    assert len(fallback_route.calls) == 1
