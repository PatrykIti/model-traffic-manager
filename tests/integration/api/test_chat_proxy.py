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
