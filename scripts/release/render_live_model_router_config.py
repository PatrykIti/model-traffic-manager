from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: render_live_model_router_config.py <terraform-outputs-json>")

    outputs_path = Path(sys.argv[1])
    outputs = json.loads(outputs_path.read_text(encoding="utf-8"))

    endpoint = outputs["openai_account_endpoint"]["value"].rstrip("/")
    deployments = outputs["router_deployments"]["value"]
    timeout_ms = int(os.getenv("E2E_ROUTER_TIMEOUT_MS", "30000"))
    max_attempts = int(os.getenv("E2E_ROUTER_MAX_ATTEMPTS", "3"))
    failure_threshold = int(os.getenv("E2E_ROUTER_FAILURE_THRESHOLD", "1"))
    cooldown_seconds = int(os.getenv("E2E_ROUTER_COOLDOWN_SECONDS", "30"))
    half_open_after_seconds = int(os.getenv("E2E_ROUTER_HALF_OPEN_AFTER_SECONDS", "60"))
    namespace = os.getenv("E2E_NAMESPACE", "e2e-router")
    mock_base_url = f"http://router-failover-mock.{namespace}.svc.cluster.local:8080"

    lines = [
        "router:",
        "  instance_name: e2e-aks-live-model",
        f"  timeout_ms: {timeout_ms}",
        f"  max_attempts: {max_attempts}",
        "  retryable_status_codes: [429, 500, 502, 503, 504]",
        "  health:",
        f"    failure_threshold: {failure_threshold}",
        f"    cooldown_seconds: {cooldown_seconds}",
        f"    half_open_after_seconds: {half_open_after_seconds}",
        "",
        "deployments:",
    ]

    for router_deployment_id, _deployment in deployments.items():
        lines.extend(
            [
                f"  - id: {router_deployment_id}",
                "    kind: llm",
                "    protocol: openai_chat",
                "    routing:",
                "      strategy: tiered_failover",
                "    limits:",
                "      max_concurrency: 1",
                "      request_rate_per_second: 1",
                "    upstreams:",
                "      - id: primary",
                "        provider: azure_openai",
                "        account: live-model",
                "        region: swedencentral",
                "        tier: 0",
                "        weight: 100",
                f"        endpoint: {endpoint}/openai/v1/chat/completions",
                "        auth:",
                "          mode: managed_identity",
                "          scope: https://cognitiveservices.azure.com/.default",
            ]
        )
        lines.append("")
        lines.extend(
            [
                f"  - id: {router_deployment_id}-failover-rate-limit",
                "    kind: llm",
                "    protocol: openai_chat",
                "    routing:",
                "      strategy: tiered_failover",
                "    limits:",
                "      max_concurrency: 1",
                "      request_rate_per_second: 1",
                "    upstreams:",
                "      - id: mock-rate-limit-primary",
                "        provider: internal_mock",
                "        account: failover-test",
                "        region: local",
                "        tier: 0",
                "        weight: 100",
                f"        endpoint: {mock_base_url}/rate-limit",
                "        auth:",
                "          mode: none",
                "      - id: aoai-secondary",
                "        provider: azure_openai",
                "        account: live-model",
                "        region: swedencentral",
                "        tier: 1",
                "        weight: 100",
                f"        endpoint: {endpoint}/openai/v1/chat/completions",
                "        auth:",
                "          mode: managed_identity",
                "          scope: https://cognitiveservices.azure.com/.default",
                "",
                f"  - id: {router_deployment_id}-failover-unhealthy",
                "    kind: llm",
                "    protocol: openai_chat",
                "    routing:",
                "      strategy: tiered_failover",
                "    limits:",
                "      max_concurrency: 1",
                "      request_rate_per_second: 1",
                "    upstreams:",
                "      - id: mock-unhealthy-primary",
                "        provider: internal_mock",
                "        account: failover-test",
                "        region: local",
                "        tier: 0",
                "        weight: 100",
                f"        endpoint: {mock_base_url}/unhealthy",
                "        auth:",
                "          mode: none",
                "      - id: aoai-secondary",
                "        provider: azure_openai",
                "        account: live-model",
                "        region: swedencentral",
                "        tier: 1",
                "        weight: 100",
                f"        endpoint: {endpoint}/openai/v1/chat/completions",
                "        auth:",
                "          mode: managed_identity",
                "          scope: https://cognitiveservices.azure.com/.default",
            ]
        )
        lines.append("")

    lines.extend(
        [
            "shared_services: {}",
        ]
    )

    sys.stdout.write("\n".join(lines))


if __name__ == "__main__":
    main()
