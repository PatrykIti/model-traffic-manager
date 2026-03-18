from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: render_live_shared_services_router_config.py <terraform-outputs-json>"
        )

    outputs_path = Path(sys.argv[1])
    outputs = json.loads(outputs_path.read_text(encoding="utf-8"))

    archive_endpoint = outputs["conversation_archive_blob_endpoint"]["value"].rstrip("/")
    timeout_ms = int(os.getenv("E2E_ROUTER_TIMEOUT_MS", "30000"))
    max_attempts = int(os.getenv("E2E_ROUTER_MAX_ATTEMPTS", "3"))
    namespace = os.getenv("E2E_NAMESPACE", "e2e-router")
    mock_base_url = f"http://router-shared-service-mock.{namespace}.svc.cluster.local:8080"

    lines = [
        "router:",
        "  instance_name: e2e-aks-live-shared-services",
        f"  timeout_ms: {timeout_ms}",
        f"  max_attempts: {max_attempts}",
        "  retryable_status_codes: [429, 500, 502, 503, 504]",
        "  health:",
        "    failure_threshold: 1",
        "    cooldown_seconds: 30",
        "    half_open_after_seconds: 60",
        "",
        "deployments:",
        "  - id: local-health-check",
        "    kind: llm",
        "    protocol: openai_chat",
        "    routing:",
        "      strategy: tiered_failover",
        "    limits:",
        "      max_concurrency: 10",
        "      request_rate_per_second: 5",
        "    upstreams:",
        "      - id: local-upstream",
        "        provider: internal_mock",
        "        account: local",
        "        region: local",
        "        tier: 0",
        "        weight: 100",
        f"        endpoint: {mock_base_url}/noop",
        "        auth:",
        "          mode: none",
        "",
        "shared_services:",
        "  conversation_archive:",
        "    transport: http_json",
        "    access_mode: direct_backend_access",
        "    provider_managed_availability: true",
        "    provider: azure_storage",
        "    account: live-archive",
        "    region: westeurope",
        f"    endpoint: {archive_endpoint}",
        "    auth:",
        "      mode: managed_identity",
        "      scope: https://storage.azure.com/.default",
        "  transcript_registry:",
        "    transport: http_json",
        "    access_mode: router_proxy",
        "    provider_managed_availability: true",
        "    routing_strategy: single_endpoint",
        "    limits:",
        "      max_concurrency: 10",
        "      request_rate_per_second: 5",
        "    upstreams:",
        "      - id: transcript-registry-primary",
        "        provider: internal_api",
        "        account: platform",
        "        region: westeurope",
        "        tier: 0",
        "        weight: 100",
        f"        endpoint: {mock_base_url}/single",
        "        auth:",
        "          mode: none",
        "  transcript_search:",
        "    transport: http_json",
        "    access_mode: router_proxy",
        "    provider_managed_availability: false",
        "    routing_strategy: tiered_failover",
        "    limits:",
        "      max_concurrency: 10",
        "      request_rate_per_second: 5",
        "    upstreams:",
        "      - id: transcript-search-primary",
        "        provider: internal_api",
        "        account: platform",
        "        region: westeurope",
        "        tier: 0",
        "        weight: 100",
        f"        endpoint: {mock_base_url}/tiered-primary",
        "        auth:",
        "          mode: none",
        "      - id: transcript-search-secondary",
        "        provider: internal_api",
        "        account: platform",
        "        region: northeurope",
        "        tier: 1",
        "        weight: 100",
        f"        endpoint: {mock_base_url}/tiered-secondary",
        "        auth:",
        "          mode: none",
    ]

    sys.stdout.write("\n".join(lines))


if __name__ == "__main__":
    main()
