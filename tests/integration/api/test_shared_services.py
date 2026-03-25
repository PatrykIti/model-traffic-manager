from __future__ import annotations

from pathlib import Path

import httpx
import respx
from fastapi.testclient import TestClient

from app.entrypoints.api.main import create_app
from app.infrastructure.config.settings import AppSettings


def build_settings(config_path: Path) -> AppSettings:
    return AppSettings(config_path=config_path, environment="test", log_level="WARNING")


@respx.mock
def test_shared_services_endpoint_returns_runtime_registry() -> None:
    app = create_app()
    with TestClient(app) as client:
        response = client.get("/shared-services")

    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "conversation_archive",
            "transport": "http_json",
            "access_mode": "direct_backend_access",
            "consumer_role": "archive-worker",
            "routing_strategy": None,
            "provider_managed_availability": True,
            "router_callable": False,
            "upstream_count": 0,
            "providers": ["azure_storage"],
            "regions": ["westeurope"],
            "endpoint": "https://conversation-archive.blob.core.windows.net/",
            "auth_mode": "managed_identity",
        },
        {
            "name": "transcript_registry",
            "transport": "http_json",
            "access_mode": "router_proxy",
            "consumer_role": "transcript-backend",
            "routing_strategy": "single_endpoint",
            "provider_managed_availability": True,
            "router_callable": True,
            "upstream_count": 1,
            "providers": ["internal_api"],
            "regions": ["local"],
            "endpoint": "https://example.invalid/shared/transcript-registry",
            "auth_mode": "none",
        },
    ]


def test_shared_service_proxy_rejects_direct_access_service() -> None:
    app = create_app()
    with TestClient(app) as client:
        response = client.post(
            "/v1/shared-services/conversation_archive",
            json={"conversation_id": "conv-1"},
        )

    assert response.status_code == 409
    assert "direct backend access" in response.json()["detail"]


@respx.mock
def test_shared_service_proxy_routes_single_endpoint_service() -> None:
    route = respx.post("https://example.invalid/shared/transcript-registry").mock(
        return_value=httpx.Response(200, json={"status": "stored"})
    )

    app = create_app()
    with TestClient(app) as client:
        response = client.post(
            "/v1/shared-services/transcript_registry",
            json={"conversation_id": "conv-1", "event": "stored"},
        )

    assert response.status_code == 200
    assert response.json() == {"status": "stored"}
    assert route.calls[0].request.content


@respx.mock
def test_shared_service_proxy_fails_over_for_tiered_service(tmp_path: Path) -> None:
    config_path = tmp_path / "router.yaml"
    config_path.write_text(
        """
router:
  instance_name: shared-service-failover-test
  timeout_ms: 30000
  max_attempts: 3
  retryable_status_codes: [429, 500, 502, 503, 504]
  health:
    failure_threshold: 3
    cooldown_seconds: 30
    half_open_after_seconds: 60

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
        endpoint: https://example.invalid/chat
        auth:
          mode: none

shared_services:
  transcript_search:
    consumer_role: search-backend
    transport: http_json
    access_mode: router_proxy
    provider_managed_availability: false
    routing_strategy: tiered_failover
    limits:
      max_concurrency: 10
      request_rate_per_second: 5
    upstreams:
      - id: primary
        provider: internal_api
        account: platform
        region: westeurope
        tier: 0
        weight: 100
        endpoint: https://example.invalid/shared-primary
        auth:
          mode: none
      - id: secondary
        provider: internal_api
        account: platform
        region: northeurope
        tier: 1
        weight: 100
        endpoint: https://example.invalid/shared-secondary
        auth:
          mode: none
""".strip(),
        encoding="utf-8",
    )

    respx.post("https://example.invalid/shared-primary").mock(
        return_value=httpx.Response(503, json={"error": "retry"})
    )
    fallback_route = respx.post("https://example.invalid/shared-secondary").mock(
        return_value=httpx.Response(200, json={"status": "stored"})
    )

    app = create_app(build_settings(config_path))
    with TestClient(app) as client:
        response = client.post(
            "/v1/shared-services/transcript_search",
            json={"conversation_id": "conv-1"},
        )

    assert response.status_code == 200
    assert response.json() == {"status": "stored"}
    assert fallback_route.called is True
