from __future__ import annotations

from pathlib import Path

import httpx
import pytest
import respx
from fastapi.testclient import TestClient

from app.entrypoints.api.main import create_app
from app.infrastructure.config.settings import AppSettings
from app.infrastructure.limits.in_memory_request_rate_limiter import InMemoryRequestRateLimiter


def build_settings(config_path: Path) -> AppSettings:
    return AppSettings(config_path=config_path, environment="test", log_level="WARNING")


@respx.mock
def test_chat_proxy_success_passthrough() -> None:
    respx.post(
        "https://example.invalid/openai/deployments/local-health-check/chat/completions"
    ).mock(return_value=httpx.Response(200, json={"id": "chatcmpl-123", "choices": []}))

    app = create_app()
    with TestClient(app) as client:
        response = client.post(
            "/v1/chat/completions/local-health-check",
            json={"messages": [{"role": "user", "content": "Hello"}]},
        )

    assert response.status_code == 200
    assert response.json() == {"id": "chatcmpl-123", "choices": []}


def test_chat_proxy_returns_404_when_deployment_is_missing() -> None:
    app = create_app()
    with TestClient(app) as client:
        response = client.post(
            "/v1/chat/completions/missing-deployment",
            json={"messages": [{"role": "user", "content": "Hello"}]},
        )

    assert response.status_code == 404
    assert "missing-deployment" in response.json()["detail"]


@respx.mock
def test_chat_proxy_maps_connection_error_to_502() -> None:
    request = httpx.Request(
        "POST",
        "https://example.invalid/openai/deployments/local-health-check/chat/completions",
    )
    respx.post(
        "https://example.invalid/openai/deployments/local-health-check/chat/completions"
    ).mock(side_effect=httpx.ConnectError("connect failed", request=request))

    app = create_app()
    with TestClient(app) as client:
        response = client.post(
            "/v1/chat/completions/local-health-check",
            json={"messages": [{"role": "user", "content": "Hello"}]},
        )

    assert response.status_code == 502


@respx.mock
def test_chat_proxy_supports_api_key_from_env(
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
  - id: api-key-chat
    kind: llm
    protocol: openai_chat
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
        endpoint: https://example.invalid/chat/completions
        auth:
          mode: api_key
          header_name: api-key
          secret_ref: env://UPSTREAM_API_KEY

shared_services: {}
""".strip(),
        encoding="utf-8",
    )

    route = respx.post("https://example.invalid/chat/completions").mock(
        return_value=httpx.Response(200, json={"id": "chatcmpl-456", "choices": []})
    )

    app = create_app(build_settings(config_path))
    with TestClient(app) as client:
        response = client.post(
            "/v1/chat/completions/api-key-chat",
            json={"messages": [{"role": "user", "content": "Hello"}]},
        )

    assert response.status_code == 200
    assert response.json() == {"id": "chatcmpl-456", "choices": []}
    assert route.calls[0].request.headers["api-key"] == "phase-2-secret"


@respx.mock
def test_chat_proxy_supports_managed_identity_with_stub_token_provider(
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
  - id: managed-identity-chat
    kind: llm
    protocol: openai_chat
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
        endpoint: https://example.invalid/chat/completions
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
    route = respx.post("https://example.invalid/chat/completions").mock(
        return_value=httpx.Response(200, json={"id": "chatcmpl-789", "choices": []})
    )

    app = create_app(build_settings(config_path))
    with TestClient(app) as client:
        response = client.post(
            "/v1/chat/completions/managed-identity-chat",
            json={"messages": [{"role": "user", "content": "Hello"}]},
        )

    assert response.status_code == 200
    assert response.json() == {"id": "chatcmpl-789", "choices": []}
    assert route.calls[0].request.headers["authorization"] == "Bearer managed-identity-token"


@respx.mock
def test_chat_proxy_fails_over_to_next_upstream_on_retryable_status(tmp_path: Path) -> None:
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
  - id: failover-chat
    kind: llm
    protocol: openai_chat
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
        endpoint: https://example.invalid/chat-primary
        auth:
          mode: none
      - id: upstream-secondary
        provider: internal_mock
        account: local
        region: local
        tier: 1
        weight: 100
        endpoint: https://example.invalid/chat-secondary
        auth:
          mode: none

shared_services: {}
""".strip(),
        encoding="utf-8",
    )

    respx.post("https://example.invalid/chat-primary").mock(
        return_value=httpx.Response(503, json={"error": "retry"})
    )
    fallback_route = respx.post("https://example.invalid/chat-secondary").mock(
        return_value=httpx.Response(200, json={"id": "chatcmpl-failover", "choices": []})
    )

    app = create_app(build_settings(config_path))
    with TestClient(app) as client:
        response = client.post(
            "/v1/chat/completions/failover-chat",
            json={"messages": [{"role": "user", "content": "Hello"}]},
        )

    assert response.status_code == 200
    assert response.json() == {"id": "chatcmpl-failover", "choices": []}
    assert len(fallback_route.calls) == 1


@respx.mock
def test_chat_proxy_skips_rate_limited_upstream_during_cooldown(tmp_path: Path) -> None:
    config_path = tmp_path / "router.yaml"
    config_path.write_text(
        """
router:
  instance_name: cooldown-test
  timeout_ms: 30000
  max_attempts: 3
  retryable_status_codes: [429, 500, 502, 503, 504]
  health:
    failure_threshold: 3
    cooldown_seconds: 30
    half_open_after_seconds: 60

deployments:
  - id: cooldown-chat
    kind: llm
    protocol: openai_chat
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
        endpoint: https://example.invalid/chat-primary-a
        auth:
          mode: none
      - id: upstream-primary-b
        provider: internal_mock
        account: local
        region: local
        tier: 0
        weight: 100
        endpoint: https://example.invalid/chat-primary-b
        auth:
          mode: none

shared_services: {}
""".strip(),
        encoding="utf-8",
    )

    primary_route = respx.post("https://example.invalid/chat-primary-a").mock(
        return_value=httpx.Response(
            429,
            headers={"Retry-After": "60"},
            json={"error": {"message": "too many requests"}},
        )
    )
    secondary_route = respx.post("https://example.invalid/chat-primary-b").mock(
        return_value=httpx.Response(200, json={"id": "chatcmpl-cooldown", "choices": []})
    )

    app = create_app(build_settings(config_path))
    with TestClient(app) as client:
        first_response = client.post(
            "/v1/chat/completions/cooldown-chat",
            json={"messages": [{"role": "user", "content": "Hello"}]},
        )
        second_response = client.post(
            "/v1/chat/completions/cooldown-chat",
            json={"messages": [{"role": "user", "content": "Hello again"}]},
        )

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert primary_route.call_count == 1
    assert secondary_route.call_count == 2


@respx.mock
def test_chat_proxy_returns_429_when_deployment_request_rate_limit_is_exceeded(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config_path = tmp_path / "router.yaml"
    config_path.write_text(
        """
router:
  instance_name: request-rate-limit-test
  timeout_ms: 30000
  max_attempts: 3
  retryable_status_codes: [429, 500, 502, 503, 504]
  health:
    failure_threshold: 3
    cooldown_seconds: 30
    half_open_after_seconds: 60

deployments:
  - id: limited-chat
    kind: llm
    protocol: openai_chat
    routing:
      strategy: tiered_failover
    limits:
      max_concurrency: 10
      request_rate_per_second: 1
    upstreams:
      - id: upstream-primary
        provider: internal_mock
        account: local
        region: local
        tier: 0
        weight: 100
        endpoint: https://example.invalid/chat-rate-limit
        auth:
          mode: none

shared_services: {}
""".strip(),
        encoding="utf-8",
    )

    deterministic_limiter = InMemoryRequestRateLimiter(now_provider=lambda: 100)
    monkeypatch.setattr(
        "app.infrastructure.bootstrap.container.InMemoryRequestRateLimiter",
        lambda: deterministic_limiter,
    )
    upstream_route = respx.post("https://example.invalid/chat-rate-limit").mock(
        return_value=httpx.Response(200, json={"id": "chatcmpl-limited", "choices": []})
    )

    app = create_app(build_settings(config_path))
    with TestClient(app) as client:
        first_response = client.post(
            "/v1/chat/completions/limited-chat",
            json={"messages": [{"role": "user", "content": "Hello"}]},
        )
        second_response = client.post(
            "/v1/chat/completions/limited-chat",
            json={"messages": [{"role": "user", "content": "Hello again"}]},
        )

    assert first_response.status_code == 200
    assert second_response.status_code == 429
    assert second_response.headers["retry-after"] == "1"
    assert upstream_route.call_count == 1
