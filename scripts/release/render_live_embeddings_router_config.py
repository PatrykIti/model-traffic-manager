from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: render_live_embeddings_router_config.py <terraform-outputs-json>")

    outputs_path = Path(sys.argv[1])
    outputs = json.loads(outputs_path.read_text(encoding="utf-8"))

    endpoint = outputs["openai_account_endpoint"]["value"].rstrip("/")
    deployments = outputs["router_embeddings_deployments"]["value"]
    timeout_ms = int(os.getenv("E2E_ROUTER_TIMEOUT_MS", "30000"))
    max_attempts = int(os.getenv("E2E_ROUTER_MAX_ATTEMPTS", "3"))

    lines = [
        "router:",
        "  instance_name: e2e-aks-live-embeddings",
        f"  timeout_ms: {timeout_ms}",
        f"  max_attempts: {max_attempts}",
        "  retryable_status_codes: [429, 500, 502, 503, 504]",
        "  health:",
        "    failure_threshold: 3",
        "    cooldown_seconds: 30",
        "    half_open_after_seconds: 60",
        "",
        "deployments:",
    ]

    for router_deployment_id, _deployment in deployments.items():
        lines.extend(
            [
                f"  - id: {router_deployment_id}",
                "    kind: embeddings",
                "    protocol: openai_embeddings",
                "    routing:",
                "      strategy: tiered_failover",
                "    limits:",
                "      max_concurrency: 1",
                "      request_rate_per_second: 1",
                "    upstreams:",
                "      - id: primary",
                "        provider: azure_openai",
                "        account: live-embeddings",
                "        region: germanywestcentral",
                "        tier: 0",
                "        weight: 100",
                f"        endpoint: {endpoint}/openai/v1/embeddings",
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
