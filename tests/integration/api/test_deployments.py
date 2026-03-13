from __future__ import annotations

from fastapi.testclient import TestClient

from app.entrypoints.api.main import app


def test_deployments_endpoint_returns_registry_from_config() -> None:
    with TestClient(app) as client:
        response = client.get("/deployments")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": "local-health-check",
            "kind": "llm",
            "protocol": "openai_chat",
            "routing_strategy": "tiered_failover",
            "upstream_count": 1,
            "providers": ["internal_mock"],
            "regions": ["local"],
        }
    ]
