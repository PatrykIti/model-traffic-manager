from __future__ import annotations

import json
import os
import time
from pathlib import Path

import httpx
import pytest


def _require_live_model() -> tuple[str, dict[str, dict[str, str]]]:
    if os.getenv("RUN_E2E_AKS_LIVE_MODEL") != "1":
        pytest.skip("e2e-aks-live-model is only enabled in the dedicated live-model runner")

    base_url = os.getenv("E2E_BASE_URL")
    outputs_path = os.getenv("E2E_LIVE_MODEL_OUTPUTS_JSON")
    if not base_url or not outputs_path:
        pytest.skip("E2E_BASE_URL and E2E_LIVE_MODEL_OUTPUTS_JSON are required")

    outputs = json.loads(Path(outputs_path).read_text(encoding="utf-8"))
    deployments = outputs["router_deployments"]["value"]
    if not deployments:
        pytest.skip("No live-model deployments are enabled in the Terraform outputs")
    return base_url, deployments


def _build_payload(deployment: dict[str, str]) -> dict[str, object]:
    payload: dict[str, object] = {
        "model": deployment["azure_deployment_name"],
        "messages": [
            {
                "role": "developer",
                "content": (
                    "Return a visible answer with no explanations. "
                    "Reply with exactly one short word: ok."
                ),
            },
            {
                "role": "user",
                "content": "Reply with exactly one short word: ok",
            },
        ],
        "max_completion_tokens": 64,
    }

    model_name = deployment.get("model_name")
    if model_name == "gpt-5":
        payload["reasoning_effort"] = "minimal"
    elif model_name == "gpt-5.1":
        payload["reasoning_effort"] = "none"

    return payload


def _message_content(body: dict[str, object]) -> str:
    choices = body.get("choices")
    if not isinstance(choices, list) or not choices:
        return ""

    first_choice = choices[0]
    if not isinstance(first_choice, dict):
        return ""

    message = first_choice.get("message")
    if not isinstance(message, dict):
        return ""

    content = message.get("content")
    return content if isinstance(content, str) else ""


def test_router_returns_live_model_response() -> None:
    base_url, deployments = _require_live_model()

    with httpx.Client(base_url=base_url, timeout=60.0) as client:
        for router_deployment_id, deployment in deployments.items():
            payload = _build_payload(deployment)

            response = None
            for _attempt in range(1, 13):
                response = client.post(f"/v1/chat/completions/{router_deployment_id}", json=payload)
                if response.status_code == 200:
                    body = response.json()
                    if _message_content(body).strip():
                        break
                    payload["max_completion_tokens"] = int(payload["max_completion_tokens"]) * 2
                    time.sleep(2)
                    continue
                if response.status_code in {401, 403, 429, 500, 502, 503, 504}:
                    time.sleep(10)
                    continue
                break

            assert response is not None
            assert response.status_code == 200, response.text
            body = response.json()
            assert body["choices"]
            assert _message_content(body).strip(), response.text
