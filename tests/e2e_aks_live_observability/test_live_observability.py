from __future__ import annotations

import json
import os
import re
import subprocess
import time
from pathlib import Path
from uuid import uuid4

import httpx
import pytest

_ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-9;]*m")


def _require_live_observability() -> tuple[str, dict[str, object], Path]:
    if os.getenv("RUN_E2E_AKS_LIVE_OBSERVABILITY") != "1":
        pytest.skip(
            "e2e-aks-live-observability is only enabled in the dedicated observability runner"
        )

    base_url = os.getenv("E2E_BASE_URL")
    outputs_path = os.getenv("E2E_LIVE_OBSERVABILITY_OUTPUTS_JSON")
    artifacts_dir = os.getenv("VALIDATION_ARTIFACTS_DIR")
    if not base_url or not outputs_path:
        pytest.skip("E2E_BASE_URL and E2E_LIVE_OBSERVABILITY_OUTPUTS_JSON are required")
    if not artifacts_dir:
        pytest.skip("VALIDATION_ARTIFACTS_DIR is required")

    outputs = json.loads(Path(outputs_path).read_text(encoding="utf-8"))
    deployments = outputs["router_observability_deployments"]["value"]
    if not deployments:
        pytest.skip("No observability deployments were enabled in the Terraform outputs")

    return base_url, deployments, Path(artifacts_dir)


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


def _poll_request_export_logs(
    *,
    namespace: str,
    request_id: str,
    expected_consumer_role: str,
    artifacts_dir: Path,
    attempts: int = 18,
    delay_seconds: int = 5,
) -> str:
    last_logs = ""
    for attempt in range(1, attempts + 1):
        logs = _kubectl_logs(namespace)
        last_logs = logs
        (artifacts_dir / f"router-export-logs-{attempt}.txt").write_text(logs, encoding="utf-8")
        if (
            request_id in logs
            and expected_consumer_role in logs
            and "upstream_id=primary" in logs
            and "applicationinsights.azure.com//v2.1/track" in logs
            and "Response status: 200" in logs
            and "Transmission succeeded" in logs
        ):
            return logs
        if attempt < attempts:
            time.sleep(delay_seconds)

    raise AssertionError(
        f"Did not find router request plus successful Application Insights export logs "
        f"for request_id={request_id}. Last logs saved under {artifacts_dir}. "
        f"Last log excerpt:\n{last_logs[-4000:]}"
    )


def _kubectl_logs(namespace: str) -> str:
    completed = subprocess.run(
        [
            "kubectl",
            "logs",
            "-n",
            namespace,
            "deployment/router-app",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout


def _normalize_logs(raw_logs: str) -> str:
    return _ANSI_ESCAPE_RE.sub("", raw_logs)


def _poll_successful_export_logs(
    *,
    namespace: str,
    artifacts_dir: Path,
    attempts: int = 18,
    delay_seconds: int = 5,
) -> str:
    last_logs = ""
    for attempt in range(1, attempts + 1):
        logs = _kubectl_logs(namespace)
        last_logs = logs
        (artifacts_dir / f"router-export-success-{attempt}.txt").write_text(
            logs,
            encoding="utf-8",
        )
        if (
            "applicationinsights.azure.com//v2.1/track" in logs
            and "Response status: 200" in logs
            and "Transmission succeeded" in logs
        ):
            return logs
        if attempt < attempts:
            time.sleep(delay_seconds)

    raise AssertionError(
        "Did not find a successful Application Insights export in pod logs. "
        f"Last logs saved under {artifacts_dir}. "
        f"Last log excerpt:\n{last_logs[-4000:]}"
    )


def test_router_emits_request_flow_to_application_insights() -> None:
    base_url, deployments, artifacts_dir = _require_live_observability()
    router_deployment_id, deployment = next(iter(deployments.items()))
    request_id = f"obs-{uuid4().hex}"
    namespace = os.getenv("E2E_NAMESPACE", "e2e-router")

    with httpx.Client(base_url=base_url, timeout=60.0) as client:
        response = client.post(
            f"/v1/chat/completions/{router_deployment_id}",
            headers={"x-request-id": request_id},
            json=_build_payload(deployment),
        )

    assert response.status_code == 200, response.text

    request_logs = _kubectl_logs(namespace)
    normalized_request_logs = _normalize_logs(request_logs)
    (artifacts_dir / "router-request-flow.log").write_text(
        normalized_request_logs,
        encoding="utf-8",
    )
    assert request_id in normalized_request_logs
    assert deployment["consumer_role"] in normalized_request_logs
    assert "event_type=request_completed" in normalized_request_logs
    assert "upstream_id=primary" in normalized_request_logs

    export_logs = _poll_successful_export_logs(
        namespace=namespace,
        artifacts_dir=artifacts_dir,
    )

    normalized_export_logs = _normalize_logs(export_logs)
    assert "applicationinsights.azure.com//v2.1/track" in normalized_export_logs
    assert "Transmission succeeded" in normalized_export_logs


def test_router_startup_logs_expose_observability_snapshot() -> None:
    _base_url, deployments, artifacts_dir = _require_live_observability()
    namespace = os.getenv("E2E_NAMESPACE", "e2e-router")
    logs = _normalize_logs(_kubectl_logs(namespace))
    (artifacts_dir / "router-startup-logs.txt").write_text(logs, encoding="utf-8")

    assert "router_topology_snapshot" in logs
    assert "e2e-aks-live-observability" in logs
    assert next(iter(deployments.values()))["consumer_role"] in logs
