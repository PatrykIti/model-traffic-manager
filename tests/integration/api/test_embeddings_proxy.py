from __future__ import annotations

from pathlib import Path

import httpx
import pytest
import respx
from fastapi.testclient import TestClient

from app.entrypoints.api.main import create_app
from app.infrastructure.config.settings import AppSettings
from app.infrastructure.limits.in_memory_concurrency_limiter import InMemoryConcurrencyLimiter


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


@respx.mock
def test_embeddings_proxy_returns_503_when_circuit_is_open(tmp_path: Path) -> None:
    config_path = tmp_path / "router.yaml"
    config_path.write_text(
        """
router:
  instance_name: circuit-open-test
  timeout_ms: 30000
  max_attempts: 3
  retryable_status_codes: [429, 500, 502, 503, 504]
  health:
    failure_threshold: 1
    cooldown_seconds: 30
    half_open_after_seconds: 60

deployments:
  - id: circuit-open-embeddings
    kind: embeddings
    protocol: openai_embeddings
    routing:
      strategy: tiered_failover
    limits:
      max_concurrency: 10
      request_rate_per_second: 5
    upstreams:
      - id: upstream-primary
        provider: internal_mock
        account: local
        region: local
        tier: 0
        weight: 100
        endpoint: https://example.invalid/embeddings-primary
        auth:
          mode: none

shared_services: {}
""".strip(),
        encoding="utf-8",
    )

    primary_route = respx.post("https://example.invalid/embeddings-primary").mock(
        return_value=httpx.Response(503, json={"error": "retry"})
    )

    app = create_app(build_settings(config_path))
    with TestClient(app) as client:
        first_response = client.post(
            "/v1/embeddings/circuit-open-embeddings",
            json={"input": "Hello"},
        )
        second_response = client.post(
            "/v1/embeddings/circuit-open-embeddings",
            json={"input": "Hello again"},
        )

    assert first_response.status_code == 503
    assert second_response.status_code == 503
    assert "No healthy upstream" in second_response.json()["detail"]
    assert primary_route.call_count == 1


@respx.mock
def test_embeddings_proxy_returns_503_when_deployment_concurrency_limit_is_exceeded(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class SaturatedConcurrencyLimiter(InMemoryConcurrencyLimiter):
        def acquire(self, deployment_id: str, max_concurrency: int) -> str | None:
            return None

    config_path = tmp_path / "router.yaml"
    config_path.write_text(
        """
router:
  instance_name: concurrency-limit-test
  timeout_ms: 30000
  max_attempts: 3
  retryable_status_codes: [429, 500, 502, 503, 504]
  health:
    failure_threshold: 3
    cooldown_seconds: 30
    half_open_after_seconds: 60

deployments:
  - id: limited-embeddings
    kind: embeddings
    protocol: openai_embeddings
    routing:
      strategy: tiered_failover
    limits:
      max_concurrency: 1
      request_rate_per_second: 10
    upstreams:
      - id: upstream-primary
        provider: internal_mock
        account: local
        region: local
        tier: 0
        weight: 100
        endpoint: https://example.invalid/embeddings-concurrency
        auth:
          mode: none

shared_services: {}
""".strip(),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "app.infrastructure.bootstrap.container.InMemoryConcurrencyLimiter",
        lambda: SaturatedConcurrencyLimiter(),
    )
    upstream_route = respx.post("https://example.invalid/embeddings-concurrency").mock(
        return_value=httpx.Response(200, json={"data": [{"embedding": [0.9, 1.0]}]})
    )

    app = create_app(build_settings(config_path))
    with TestClient(app) as client:
        response = client.post(
            "/v1/embeddings/limited-embeddings",
            json={"input": "Hello"},
        )

    assert response.status_code == 503
    assert "concurrency limit" in response.json()["detail"]
    assert upstream_route.call_count == 0


@respx.mock
def test_metrics_endpoint_exposes_prometheus_metrics() -> None:
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
        _ = client.post("/v1/embeddings/local-embeddings-check", json={"input": "Hello"})
        response = client.get("/metrics")

    assert response.status_code == 200
    assert "router_request_duration_seconds" in response.text
    assert "router_route_attempts_total" in response.text
