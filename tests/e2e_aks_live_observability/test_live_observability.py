from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path
from uuid import uuid4

import httpx
import pytest


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


def _run_app_insights_query(
    *,
    outputs: dict[str, object],
    query: str,
    artifacts_dir: Path,
    suffix: str,
) -> dict[str, object]:
    app_id = outputs["application_insights_app_id"]["value"]
    completed = subprocess.run(
        [
            "az",
            "monitor",
            "app-insights",
            "query",
            "--app",
            str(app_id),
            "--analytics-query",
            query,
            "--offset",
            "30m",
            "-o",
            "json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    output_path = artifacts_dir / f"app-insights-query-{suffix}.json"
    output_path.write_text(completed.stdout, encoding="utf-8")
    return json.loads(completed.stdout)


def _extract_first_row(payload: dict[str, object]) -> dict[str, object] | None:
    tables = payload.get("tables")
    if not isinstance(tables, list) or not tables:
        return None
    first_table = tables[0]
    if not isinstance(first_table, dict):
        return None
    columns = first_table.get("columns")
    rows = first_table.get("rows")
    if not isinstance(columns, list) or not isinstance(rows, list) or not rows:
        return None

    names: list[str] = []
    for column in columns:
        if not isinstance(column, dict):
            return None
        name = column.get("name")
        if not isinstance(name, str):
            return None
        names.append(name)

    first_row = rows[0]
    if not isinstance(first_row, list):
        return None
    return dict(zip(names, first_row, strict=False))


def _poll_request_trace(
    *,
    outputs: dict[str, object],
    request_id: str,
    expected_consumer_role: str,
    artifacts_dir: Path,
    attempts: int = 24,
    delay_seconds: int = 10,
) -> dict[str, object]:
    requests_query = f"""
requests
| where timestamp > ago(30m)
| extend request_id = tostring(customDimensions["router.request_id"])
| extend final_upstream_id = tostring(customDimensions["router.final_upstream_id"])
| extend consumer_role = tostring(customDimensions["router.consumer_role"])
| extend final_consumer_role = tostring(customDimensions["router.final_consumer_role"])
| where request_id == "{request_id}"
| project
    timestamp,
    name,
    resultCode,
    duration,
    request_id,
    final_upstream_id,
    consumer_role,
    final_consumer_role
| top 1 by timestamp desc
""".strip()
    traces_query = f"""
traces
| where timestamp > ago(30m)
| extend request_id = tostring(customDimensions["router.request_id"])
| extend final_upstream_id = tostring(customDimensions["router.final_upstream_id"])
| extend consumer_role = tostring(customDimensions["router.consumer_role"])
| extend final_consumer_role = tostring(customDimensions["router.final_consumer_role"])
| where request_id == "{request_id}"
| project
    timestamp,
    name = operation_Name,
    resultCode = tostring(""),
    duration = todouble(0),
    request_id,
    final_upstream_id,
    consumer_role,
    final_consumer_role
| top 1 by timestamp desc
""".strip()

    last_payload: dict[str, object] | None = None
    for attempt in range(1, attempts + 1):
        payload = _run_app_insights_query(
            outputs=outputs,
            query=requests_query,
            artifacts_dir=artifacts_dir,
            suffix=f"request-requests-{attempt}",
        )
        last_payload = payload
        row = _extract_first_row(payload)
        if row is not None and row.get("consumer_role") == expected_consumer_role:
            return row

        payload = _run_app_insights_query(
            outputs=outputs,
            query=traces_query,
            artifacts_dir=artifacts_dir,
            suffix=f"request-traces-{attempt}",
        )
        last_payload = payload
        row = _extract_first_row(payload)
        if row is not None and row.get("consumer_role") == expected_consumer_role:
            return row
        if attempt < attempts:
            time.sleep(delay_seconds)

    assert last_payload is not None
    raise AssertionError(
        f"Did not find Application Insights request row for request_id={request_id}. "
        f"Last payload saved under {artifacts_dir}."
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


def test_router_emits_request_flow_to_application_insights() -> None:
    base_url, deployments, artifacts_dir = _require_live_observability()
    outputs = json.loads(
        Path(os.environ["E2E_LIVE_OBSERVABILITY_OUTPUTS_JSON"]).read_text(encoding="utf-8")
    )
    router_deployment_id, deployment = next(iter(deployments.items()))
    request_id = f"obs-{uuid4().hex}"

    with httpx.Client(base_url=base_url, timeout=60.0) as client:
        response = client.post(
            f"/v1/chat/completions/{router_deployment_id}",
            headers={"x-request-id": request_id},
            json=_build_payload(deployment),
        )

    assert response.status_code == 200, response.text
    row = _poll_request_trace(
        outputs=outputs,
        request_id=request_id,
        expected_consumer_role=str(deployment["consumer_role"]),
        artifacts_dir=artifacts_dir,
    )

    assert row["request_id"] == request_id
    assert row["consumer_role"] == deployment["consumer_role"]
    assert row["final_consumer_role"] == deployment["consumer_role"]
    assert row["final_upstream_id"] == "primary"
    assert str(row["resultCode"]) == "200"


def test_router_startup_logs_expose_observability_snapshot() -> None:
    _base_url, deployments, artifacts_dir = _require_live_observability()
    namespace = os.getenv("E2E_NAMESPACE", "e2e-router")
    logs = _kubectl_logs(namespace)
    (artifacts_dir / "router-startup-logs.txt").write_text(logs, encoding="utf-8")

    assert "router_topology_snapshot" in logs
    assert "e2e-aks-live-observability" in logs
    assert next(iter(deployments.values()))["consumer_role"] in logs
