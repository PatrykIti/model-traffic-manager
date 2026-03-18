from __future__ import annotations

import os
import time
from collections import Counter
from collections.abc import Callable

import httpx
import pytest


def _require_live_load_balancing() -> str:
    if os.getenv("RUN_E2E_AKS_LIVE_LOAD_BALANCING") != "1":
        pytest.skip(
            "e2e-aks-live-load-balancing is only enabled in the dedicated live balancing runner"
        )

    base_url = os.getenv("E2E_BASE_URL")
    if not base_url:
        pytest.skip("E2E_BASE_URL is required for e2e-aks-live-load-balancing")
    return base_url


def _send_with_transport_retry(
    client: httpx.Client,
    method: str,
    url: str,
    *,
    attempts: int = 6,
    delay_seconds: int = 2,
    **kwargs: object,
) -> tuple[httpx.Response, bool]:
    had_retry = False
    last_error: httpx.TransportError | None = None

    for attempt in range(1, attempts + 1):
        try:
            return client.request(method, url, **kwargs), had_retry
        except httpx.TransportError as exc:
            had_retry = True
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


def _collect_clean_distribution_window(
    client: httpx.Client,
    url: str,
    payload: dict[str, object],
    *,
    key: str,
    attempts: int = 5,
    response_validator: Callable[[dict[str, object]], None] | None = None,
) -> Counter[str]:
    for window_attempt in range(1, attempts + 1):
        counts: Counter[str] = Counter()
        had_retry = False

        for _ in range(10):
            response, retried = _send_with_transport_retry(client, "POST", url, json=payload)
            had_retry = had_retry or retried
            assert response.status_code == 200, response.text
            body = response.json()
            if response_validator is not None:
                response_validator(body)
            counts[body[key]] += 1

        if not had_retry:
            return counts

        print(
            f"Restarting distribution window {window_attempt}/{attempts} for {url} "
            "because transport retries occurred."
        )

    return counts


def test_chat_active_active_distribution_is_observable() -> None:
    base_url = _require_live_load_balancing()

    with httpx.Client(base_url=base_url, timeout=30.0) as client:
        counts = _collect_clean_distribution_window(
            client,
            "/v1/chat/completions/chat-active-active-80-20",
            {"messages": [{"role": "user", "content": "hello"}]},
            key="selected",
        )

    assert counts["chat-a"] == 8
    assert counts["chat-b"] == 2


def test_chat_active_standby_prefers_active_upstream() -> None:
    base_url = _require_live_load_balancing()

    with httpx.Client(base_url=base_url, timeout=30.0) as client:
        responses = [
            _send_with_transport_retry(
                client,
                "POST",
                "/v1/chat/completions/chat-active-standby",
                json={"messages": [{"role": "user", "content": "hello"}]},
            )[0]
            for _ in range(3)
        ]

    for response in responses:
        assert response.status_code == 200, response.text
        assert response.json()["selected"] == "chat-primary"


def test_chat_active_standby_fails_over_to_standby_after_failure() -> None:
    base_url = _require_live_load_balancing()

    with httpx.Client(base_url=base_url, timeout=30.0) as client:
        response, _ = _send_with_transport_retry(
            client,
            "POST",
            "/v1/chat/completions/chat-active-standby-failover",
            json={"messages": [{"role": "user", "content": "hello"}]},
        )

    assert response.status_code == 200, response.text
    assert response.json()["selected"] == "chat-standby"


def test_embeddings_active_active_distribution_is_observable() -> None:
    base_url = _require_live_load_balancing()

    def _validate_embedding_payload(body: dict[str, object]) -> None:
        data = body.get("data")
        assert isinstance(data, list) and data
        first_item = data[0]
        assert isinstance(first_item, dict)
        embedding = first_item.get("embedding")
        assert isinstance(embedding, list) and embedding

    with httpx.Client(base_url=base_url, timeout=30.0) as client:
        counts = _collect_clean_distribution_window(
            client,
            "/v1/embeddings/embeddings-active-active-80-20",
            {"input": "hello"},
            key="selected",
            response_validator=_validate_embedding_payload,
        )

    assert counts["emb-a"] == 8
    assert counts["emb-b"] == 2
