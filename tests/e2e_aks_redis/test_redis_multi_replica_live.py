from __future__ import annotations

import os
import time
from concurrent.futures import ThreadPoolExecutor

import httpx
import pytest


def _require_e2e_aks_redis() -> tuple[str, str]:
    if os.getenv("RUN_E2E_AKS_REDIS") != "1":
        pytest.skip("e2e-aks-redis is only enabled in the dedicated Redis-backed AKS runner")

    base_url_a = os.getenv("E2E_BASE_URL_REPLICA_A")
    base_url_b = os.getenv("E2E_BASE_URL_REPLICA_B")
    if not base_url_a or not base_url_b:
        pytest.skip("E2E_BASE_URL_REPLICA_A and E2E_BASE_URL_REPLICA_B are required")
    return base_url_a, base_url_b


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


def _chat_payload() -> dict[str, object]:
    return {"messages": [{"role": "user", "content": "hello"}]}


def test_request_rate_limit_is_shared_across_replicas() -> None:
    base_url_a, base_url_b = _require_e2e_aks_redis()

    with (
        httpx.Client(base_url=base_url_a, timeout=60.0) as client_a,
        httpx.Client(base_url=base_url_b, timeout=60.0) as client_b,
    ):
        response_a = None
        response_b = None
        before_metrics = _send_with_transport_retry(client_b, "GET", "/metrics").text

        for _window in range(1, 4):
            response_a = _send_with_transport_retry(
                client_a,
                "POST",
                "/v1/chat/completions/chat-shared-request-rate",
                json=_chat_payload(),
            )
            response_b = _send_with_transport_retry(
                client_b,
                "POST",
                "/v1/chat/completions/chat-shared-request-rate",
                json=_chat_payload(),
            )
            if response_b.status_code == 429:
                break
            time.sleep(1.2)

        after_metrics = _send_with_transport_retry(client_b, "GET", "/metrics").text

    assert response_a is not None
    assert response_b is not None
    assert response_a.status_code == 200, response_a.text
    assert response_b.status_code == 429, response_b.text
    assert response_b.headers.get("Retry-After") == "1"
    rejections_before = _metric_value(
        before_metrics,
        "router_limiter_rejections_total",
        {
            "endpoint_kind": "chat_completions",
            "deployment_id": "chat-shared-request-rate",
            "reason": "request_rate",
        },
    )
    rejections_after = _metric_value(
        after_metrics,
        "router_limiter_rejections_total",
        {
            "endpoint_kind": "chat_completions",
            "deployment_id": "chat-shared-request-rate",
            "reason": "request_rate",
        },
    )
    assert rejections_after - rejections_before >= 1


def test_concurrency_limit_is_shared_across_replicas() -> None:
    base_url_a, base_url_b = _require_e2e_aks_redis()

    def _invoke_replica_a() -> httpx.Response:
        with httpx.Client(base_url=base_url_a, timeout=60.0) as client_a:
            return _send_with_transport_retry(
                client_a,
                "POST",
                "/v1/chat/completions/chat-shared-concurrency",
                json=_chat_payload(),
            )

    with httpx.Client(base_url=base_url_b, timeout=60.0) as client_b:
        before_metrics = _send_with_transport_retry(client_b, "GET", "/metrics").text
        with ThreadPoolExecutor(max_workers=1) as executor:
            future_a = executor.submit(_invoke_replica_a)
            time.sleep(1)
            response_b = _send_with_transport_retry(
                client_b,
                "POST",
                "/v1/chat/completions/chat-shared-concurrency",
                json=_chat_payload(),
            )
            response_a = future_a.result()
        after_metrics = _send_with_transport_retry(client_b, "GET", "/metrics").text

    assert response_a.status_code == 200, response_a.text
    assert response_b.status_code == 503, response_b.text
    assert "concurrency limit" in response_b.json()["detail"].lower()
    rejections_before = _metric_value(
        before_metrics,
        "router_limiter_rejections_total",
        {
            "endpoint_kind": "chat_completions",
            "deployment_id": "chat-shared-concurrency",
            "reason": "concurrency",
        },
    )
    rejections_after = _metric_value(
        after_metrics,
        "router_limiter_rejections_total",
        {
            "endpoint_kind": "chat_completions",
            "deployment_id": "chat-shared-concurrency",
            "reason": "concurrency",
        },
    )
    assert rejections_after - rejections_before >= 1


def test_cooldown_state_is_shared_across_replicas() -> None:
    base_url_a, base_url_b = _require_e2e_aks_redis()

    with (
        httpx.Client(base_url=base_url_a, timeout=60.0) as client_a,
        httpx.Client(base_url=base_url_b, timeout=60.0) as client_b,
    ):
        before_metrics_a = _send_with_transport_retry(client_a, "GET", "/metrics").text
        before_metrics_b = _send_with_transport_retry(client_b, "GET", "/metrics").text
        first_response = _send_with_transport_retry(
            client_a,
            "POST",
            "/v1/chat/completions/chat-failover-rate-limit",
            json=_chat_payload(),
        )
        assert first_response.status_code == 200, first_response.text
        assert first_response.json()["selected"] == "secondary"

        after_first_metrics_a = _send_with_transport_retry(client_a, "GET", "/metrics").text
        after_first_metrics_b = _send_with_transport_retry(client_b, "GET", "/metrics").text
        second_response = _send_with_transport_retry(
            client_b,
            "POST",
            "/v1/chat/completions/chat-failover-rate-limit",
            json=_chat_payload(),
        )
        assert second_response.status_code == 200, second_response.text
        assert second_response.json()["selected"] == "secondary"
        after_second_metrics_b = _send_with_transport_retry(client_b, "GET", "/metrics").text

    cooldown_updates_before = _metric_value(
        before_metrics_a,
        "router_health_state_updates_total",
        {"deployment_id": "chat-failover-rate-limit", "status": "cooldown"},
    )
    cooldown_updates_after = _metric_value(
        after_first_metrics_a,
        "router_health_state_updates_total",
        {"deployment_id": "chat-failover-rate-limit", "status": "cooldown"},
    )
    attempts_before = _metric_value(
        before_metrics_b,
        "router_route_attempts_total",
        {"endpoint_kind": "chat_completions", "deployment_id": "chat-failover-rate-limit"},
    )
    attempts_after_first = _metric_value(
        after_first_metrics_b,
        "router_route_attempts_total",
        {"endpoint_kind": "chat_completions", "deployment_id": "chat-failover-rate-limit"},
    )
    attempts_after_second = _metric_value(
        after_second_metrics_b,
        "router_route_attempts_total",
        {"endpoint_kind": "chat_completions", "deployment_id": "chat-failover-rate-limit"},
    )

    assert cooldown_updates_after - cooldown_updates_before >= 1
    assert attempts_after_first - attempts_before == 0
    assert attempts_after_second - attempts_after_first == 1


def test_circuit_open_state_is_shared_across_replicas() -> None:
    base_url_a, base_url_b = _require_e2e_aks_redis()

    with (
        httpx.Client(base_url=base_url_a, timeout=60.0) as client_a,
        httpx.Client(base_url=base_url_b, timeout=60.0) as client_b,
    ):
        before_metrics_a = _send_with_transport_retry(client_a, "GET", "/metrics").text
        before_metrics_b = _send_with_transport_retry(client_b, "GET", "/metrics").text
        first_response = _send_with_transport_retry(
            client_a,
            "POST",
            "/v1/chat/completions/chat-failover-unhealthy",
            json=_chat_payload(),
        )
        assert first_response.status_code == 200, first_response.text
        assert first_response.json()["selected"] == "secondary"

        after_first_metrics_a = _send_with_transport_retry(client_a, "GET", "/metrics").text
        after_first_metrics_b = _send_with_transport_retry(client_b, "GET", "/metrics").text
        second_response = _send_with_transport_retry(
            client_b,
            "POST",
            "/v1/chat/completions/chat-failover-unhealthy",
            json=_chat_payload(),
        )
        assert second_response.status_code == 200, second_response.text
        assert second_response.json()["selected"] == "secondary"
        after_second_metrics_b = _send_with_transport_retry(client_b, "GET", "/metrics").text

    circuit_updates_before = _metric_value(
        before_metrics_a,
        "router_health_state_updates_total",
        {"deployment_id": "chat-failover-unhealthy", "status": "circuit_open"},
    )
    circuit_updates_after = _metric_value(
        after_first_metrics_a,
        "router_health_state_updates_total",
        {"deployment_id": "chat-failover-unhealthy", "status": "circuit_open"},
    )
    attempts_before = _metric_value(
        before_metrics_b,
        "router_route_attempts_total",
        {"endpoint_kind": "chat_completions", "deployment_id": "chat-failover-unhealthy"},
    )
    attempts_after_first = _metric_value(
        after_first_metrics_b,
        "router_route_attempts_total",
        {"endpoint_kind": "chat_completions", "deployment_id": "chat-failover-unhealthy"},
    )
    attempts_after_second = _metric_value(
        after_second_metrics_b,
        "router_route_attempts_total",
        {"endpoint_kind": "chat_completions", "deployment_id": "chat-failover-unhealthy"},
    )

    assert circuit_updates_after - circuit_updates_before >= 1
    assert attempts_after_first - attempts_before == 0
    assert attempts_after_second - attempts_after_first == 1
