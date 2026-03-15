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


def test_router_returns_live_model_response() -> None:
    base_url, deployments = _require_live_model()

    with httpx.Client(base_url=base_url, timeout=60.0) as client:
        for router_deployment_id, deployment in deployments.items():
            payload = {
                "model": deployment["azure_deployment_name"],
                "messages": [
                    {
                        "role": "user",
                        "content": "Reply with exactly one short word: ok",
                    }
                ],
                "max_completion_tokens": 8,
            }

            response = None
            for _attempt in range(1, 13):
                response = client.post(f"/v1/chat/completions/{router_deployment_id}", json=payload)
                if response.status_code == 200:
                    break
                if response.status_code in {401, 403, 429, 500, 502, 503, 504}:
                    time.sleep(10)
                    continue
                break

            assert response is not None
            assert response.status_code == 200, response.text
            body = response.json()
            assert body["choices"]
            assert body["choices"][0]["message"]["content"].strip()
