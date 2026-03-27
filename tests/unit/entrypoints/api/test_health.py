from __future__ import annotations

from fastapi.testclient import TestClient

from app.entrypoints.api.main import app


def test_live_health_returns_expected_payload() -> None:
    with TestClient(app) as client:
        response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "kind": "live",
        "service": "model-traffic-manager",
    }


def test_ready_health_returns_expected_payload() -> None:
    with TestClient(app) as client:
        response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "kind": "ready",
        "service": "model-traffic-manager",
    }
