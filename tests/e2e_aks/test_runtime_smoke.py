from __future__ import annotations

import os

import httpx
import pytest


def _require_e2e_aks() -> str:
    if os.getenv("RUN_E2E_AKS") != "1":
        pytest.skip("e2e-aks is only enabled in the dedicated AKS workflow")

    base_url = os.getenv("E2E_BASE_URL")
    if not base_url:
        pytest.skip("E2E_BASE_URL is required for e2e-aks")
    return base_url


def test_router_runtime_health_and_metrics_smoke() -> None:
    base_url = _require_e2e_aks()

    with httpx.Client(base_url=base_url, timeout=30.0) as client:
        live = client.get("/health/live")
        ready = client.get("/health/ready")
        deployments = client.get("/deployments")
        shared_services = client.get("/shared-services")
        metrics = client.get("/metrics")

    assert live.status_code == 200
    assert ready.status_code == 200
    assert deployments.status_code == 200
    assert shared_services.status_code == 200
    assert metrics.status_code == 200
    assert "router_request_duration_seconds" in metrics.text
