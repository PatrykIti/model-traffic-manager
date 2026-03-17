from __future__ import annotations

import os
from collections import Counter

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


def test_chat_active_active_distribution_is_observable() -> None:
    base_url = _require_live_load_balancing()

    counts: Counter[str] = Counter()
    with httpx.Client(base_url=base_url, timeout=30.0) as client:
        for _ in range(10):
            response = client.post(
                "/v1/chat/completions/chat-active-active-80-20",
                json={"messages": [{"role": "user", "content": "hello"}]},
            )
            assert response.status_code == 200, response.text
            counts[response.json()["selected"]] += 1

    assert counts["chat-a"] == 8
    assert counts["chat-b"] == 2


def test_chat_active_standby_prefers_active_upstream() -> None:
    base_url = _require_live_load_balancing()

    with httpx.Client(base_url=base_url, timeout=30.0) as client:
        responses = [
            client.post(
                "/v1/chat/completions/chat-active-standby",
                json={"messages": [{"role": "user", "content": "hello"}]},
            )
            for _ in range(3)
        ]

    for response in responses:
        assert response.status_code == 200, response.text
        assert response.json()["selected"] == "chat-primary"


def test_chat_active_standby_fails_over_to_standby_after_failure() -> None:
    base_url = _require_live_load_balancing()

    with httpx.Client(base_url=base_url, timeout=30.0) as client:
        response = client.post(
            "/v1/chat/completions/chat-active-standby-failover",
            json={"messages": [{"role": "user", "content": "hello"}]},
        )

    assert response.status_code == 200, response.text
    assert response.json()["selected"] == "chat-standby"


def test_embeddings_active_active_distribution_is_observable() -> None:
    base_url = _require_live_load_balancing()

    counts: Counter[str] = Counter()
    with httpx.Client(base_url=base_url, timeout=30.0) as client:
        for _ in range(10):
            response = client.post(
                "/v1/embeddings/embeddings-active-active-80-20",
                json={"input": "hello"},
            )
            assert response.status_code == 200, response.text
            body = response.json()
            counts[body["selected"]] += 1
            assert body["data"][0]["embedding"]

    assert counts["emb-a"] == 8
    assert counts["emb-b"] == 2
