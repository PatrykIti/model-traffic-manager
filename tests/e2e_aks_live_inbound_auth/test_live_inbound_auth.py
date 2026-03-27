from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import httpx
import pytest


def _require_live_inbound_auth() -> tuple[str, dict[str, object], str]:
    if os.getenv("RUN_E2E_AKS_LIVE_INBOUND_AUTH") != "1":
        pytest.skip("e2e-aks-live-inbound-auth is only enabled in the dedicated auth runner")

    base_url = os.getenv("E2E_BASE_URL")
    outputs_path = os.getenv("E2E_LIVE_INBOUND_AUTH_OUTPUTS_JSON")
    api_token = os.getenv("E2E_INBOUND_API_TOKEN")
    if not base_url or not outputs_path or not api_token:
        pytest.skip(
            "E2E_BASE_URL, E2E_LIVE_INBOUND_AUTH_OUTPUTS_JSON, "
            "and E2E_INBOUND_API_TOKEN are required"
        )

    outputs = json.loads(Path(outputs_path).read_text(encoding="utf-8"))
    deployments = outputs["router_auth_deployments"]["value"]
    if not deployments:
        pytest.skip("No auth deployments are enabled in the Terraform outputs")
    return base_url, deployments, api_token


def _build_payload(deployment: dict[str, object]) -> dict[str, object]:
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


def _caller_pod_name(namespace: str) -> str:
    completed = subprocess.run(
        [
            "kubectl",
            "get",
            "pods",
            "-n",
            namespace,
            "-l",
            "app=router-caller",
            "-o",
            "jsonpath={.items[0].metadata.name}",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    pod_name = completed.stdout.strip()
    assert pod_name
    return pod_name


def test_router_requires_and_accepts_api_bearer_token() -> None:
    base_url, deployments, api_token = _require_live_inbound_auth()
    router_deployment_id, deployment = next(iter(deployments.items()))

    with httpx.Client(base_url=base_url, timeout=60.0) as client:
        unauthorized = client.post(
            f"/v1/chat/completions/{router_deployment_id}",
            json=_build_payload(deployment),
        )
        authorized = client.post(
            f"/v1/chat/completions/{router_deployment_id}",
            headers={"Authorization": f"Bearer {api_token}"},
            json=_build_payload(deployment),
        )

    assert unauthorized.status_code == 401
    assert authorized.status_code == 200, authorized.text


def test_router_accepts_entra_token_from_federated_workload_identity() -> None:
    _base_url, deployments, _api_token = _require_live_inbound_auth()
    namespace = os.getenv("E2E_NAMESPACE", "e2e-router")
    audience = os.environ["E2E_ROUTER_API_AUDIENCE"]
    router_deployment_id, deployment = next(iter(deployments.items()))
    pod_name = _caller_pod_name(namespace)
    payload = json.dumps(_build_payload(deployment))

    script = f"""
import httpx
from azure.identity import DefaultAzureCredential

token = DefaultAzureCredential().get_token("{audience}/.default").token
response = httpx.post(
    "http://router-app.{namespace}.svc.cluster.local:8000/v1/chat/completions/{router_deployment_id}",
    headers={{"Authorization": f"Bearer {{token}}"}},
    json={payload},
    timeout=60.0,
)
print(response.status_code)
print(response.text)
""".strip()

    completed = subprocess.run(
        [
            "kubectl",
            "exec",
            "-n",
            namespace,
            f"pod/{pod_name}",
            "--",
            "/app/.venv/bin/python",
            "-c",
            script,
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "\n200\n" in f"\n{completed.stdout}"
