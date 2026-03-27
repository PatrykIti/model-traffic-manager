from __future__ import annotations

import json
import os
import time
from pathlib import Path

import httpx
import pytest


def _require_live_shared_services() -> tuple[str, str]:
    if os.getenv("RUN_E2E_AKS_LIVE_SHARED_SERVICES") != "1":
        pytest.skip(
            "e2e-aks-live-shared-services is only enabled "
            "in the dedicated live shared-services runner"
        )

    base_url = os.getenv("E2E_BASE_URL")
    outputs_path = os.getenv("E2E_LIVE_SHARED_SERVICES_OUTPUTS_JSON")
    if not base_url or not outputs_path:
        pytest.skip("E2E_BASE_URL and E2E_LIVE_SHARED_SERVICES_OUTPUTS_JSON are required")

    outputs = json.loads(Path(outputs_path).read_text(encoding="utf-8"))
    archive_endpoint = outputs["conversation_archive_blob_endpoint"]["value"].rstrip("/")
    return base_url, archive_endpoint


def _metric_value(metrics_text: str, metric_name: str, labels: dict[str, str]) -> float:
    for raw_line in metrics_text.splitlines():
        line = raw_line.strip()
        if not line.startswith(f"{metric_name}{{"):
            continue
        if all(f'{key}="{value}"' in line for key, value in labels.items()):
            return float(line.rsplit(" ", 1)[1])
    return 0.0


def _send_with_transport_retry(
    client: httpx.Client,
    method: str,
    url: str,
    *,
    attempts: int = 6,
    delay_seconds: int = 2,
    **kwargs: object,
) -> httpx.Response:
    last_error: httpx.TransportError | None = None

    for attempt in range(1, attempts + 1):
        try:
            return client.request(method, url, **kwargs)
        except httpx.TransportError as exc:
            last_error = exc
            if attempt == attempts:
                break
            print(
                f"Transport retry {attempt}/{attempts} for {method} {url}: "
                f"{exc.__class__.__name__}: {exc}"
            )
            time.sleep(delay_seconds)

    assert last_error is not None
    raise last_error


def test_shared_services_registry_exposes_direct_and_router_proxy_profiles() -> None:
    base_url, archive_endpoint = _require_live_shared_services()

    with httpx.Client(base_url=base_url, timeout=60.0) as client:
        response = _send_with_transport_retry(client, "GET", "/shared-services")

    assert response.status_code == 200, response.text
    summaries = {service["name"]: service for service in response.json()}

    archive = summaries["conversation_archive"]
    assert archive["access_mode"] == "direct_backend_access"
    assert archive["router_callable"] is False
    assert archive["provider_managed_availability"] is True
    assert archive["auth_mode"] == "managed_identity"
    assert archive["endpoint"].rstrip("/") == archive_endpoint

    registry = summaries["transcript_registry"]
    assert registry["access_mode"] == "router_proxy"
    assert registry["routing_strategy"] == "single_endpoint"
    assert registry["router_callable"] is True
    assert registry["upstream_count"] == 1

    search = summaries["transcript_search"]
    assert search["access_mode"] == "router_proxy"
    assert search["routing_strategy"] == "tiered_failover"
    assert search["router_callable"] is True
    assert search["upstream_count"] == 2


def test_direct_backend_access_service_fails_closed_when_executed_via_router() -> None:
    base_url, _archive_endpoint = _require_live_shared_services()

    with httpx.Client(base_url=base_url, timeout=60.0) as client:
        response = _send_with_transport_retry(
            client,
            "POST",
            "/v1/shared-services/conversation_archive",
            json={"conversation_id": "conv-1"},
        )

    assert response.status_code == 409
    assert "direct backend access" in response.json()["detail"].lower()


def test_router_proxy_single_endpoint_service_executes_successfully() -> None:
    base_url, _archive_endpoint = _require_live_shared_services()

    with httpx.Client(base_url=base_url, timeout=60.0) as client:
        response = _send_with_transport_retry(
            client,
            "POST",
            "/v1/shared-services/transcript_registry",
            json={"conversation_id": "conv-1", "event": "stored"},
        )

    assert response.status_code == 200, response.text
    assert response.json() == {"selected": "single-endpoint", "status": "stored"}


def test_router_proxy_tiered_failover_uses_secondary_and_skips_primary_after_circuit() -> None:
    base_url, _archive_endpoint = _require_live_shared_services()

    with httpx.Client(base_url=base_url, timeout=60.0) as client:
        before_metrics = _send_with_transport_retry(client, "GET", "/metrics").text
        response = _send_with_transport_retry(
            client,
            "POST",
            "/v1/shared-services/transcript_search",
            json={"conversation_id": "conv-1"},
        )
        assert response.status_code == 200, response.text
        assert response.json() == {"selected": "tiered-secondary", "status": "stored"}

        after_first_metrics = _send_with_transport_retry(client, "GET", "/metrics").text
        response_second = _send_with_transport_retry(
            client,
            "POST",
            "/v1/shared-services/transcript_search",
            json={"conversation_id": "conv-1"},
        )
        assert response_second.status_code == 200, response_second.text
        assert response_second.json() == {"selected": "tiered-secondary", "status": "stored"}
        after_second_metrics = _send_with_transport_retry(client, "GET", "/metrics").text

    attempts_before = _metric_value(
        before_metrics,
        "router_route_attempts_total",
        {"endpoint_kind": "shared_service", "deployment_id": "transcript_search"},
    )
    attempts_after_first = _metric_value(
        after_first_metrics,
        "router_route_attempts_total",
        {"endpoint_kind": "shared_service", "deployment_id": "transcript_search"},
    )
    attempts_after_second = _metric_value(
        after_second_metrics,
        "router_route_attempts_total",
        {"endpoint_kind": "shared_service", "deployment_id": "transcript_search"},
    )
    circuit_updates = _metric_value(
        after_second_metrics,
        "router_health_state_updates_total",
        {"deployment_id": "transcript_search", "status": "circuit_open"},
    )

    assert attempts_after_first - attempts_before == 2
    assert attempts_after_second - attempts_after_first == 1
    assert circuit_updates >= 1
