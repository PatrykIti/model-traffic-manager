from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from app.entrypoints.api.main import create_app
from app.infrastructure.config.settings import AppSettings


def build_settings(config_path: Path) -> AppSettings:
    return AppSettings(config_path=config_path, environment="test", log_level="WARNING")


def test_shared_services_endpoint_returns_configured_registry(tmp_path: Path) -> None:
    config_path = tmp_path / "router.yaml"
    config_path.write_text(
        """
router:
  instance_name: shared-services-test
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
  blob_storage:
    endpoint: https://storage.example.invalid
    auth:
      mode: managed_identity
      scope: https://storage.azure.com/.default
  key_vault:
    endpoint: https://vault.example.invalid
    auth:
      mode: none
""".strip(),
        encoding="utf-8",
    )

    app = create_app(build_settings(config_path))
    with TestClient(app) as client:
        response = client.get("/shared-services")

    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "blob_storage",
            "endpoint": "https://storage.example.invalid/",
            "auth_mode": "managed_identity",
        },
        {
            "name": "key_vault",
            "endpoint": "https://vault.example.invalid/",
            "auth_mode": "none",
        },
    ]
