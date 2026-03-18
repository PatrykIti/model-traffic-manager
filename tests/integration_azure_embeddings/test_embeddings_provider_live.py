from __future__ import annotations

import json
import os
import time
from pathlib import Path

import pytest

from app.domain.value_objects.auth_policy import AuthMode, AuthPolicy
from app.infrastructure.auth.auth_header_builder import AuthHeaderBuilder
from app.infrastructure.auth.managed_identity_token_provider import ManagedIdentityTokenProvider
from app.infrastructure.http.httpx_outbound_invoker import HttpxOutboundInvoker


class UnusedSecretProvider:
    def get_secret(self, secret_ref: str) -> str:  # pragma: no cover - defensive stub
        raise AssertionError("Secret provider should not be used for managed_identity")


def _require_integration_azure_embeddings() -> tuple[str, str, dict[str, dict[str, str]], str]:
    if os.getenv("RUN_INTEGRATION_AZURE_EMBEDDINGS") != "1":
        pytest.skip(
            "integration-azure-embeddings is only enabled "
            "in the dedicated Azure embeddings workflow"
        )

    outputs_path = os.getenv("INTEGRATION_AZURE_EMBEDDINGS_OUTPUTS_JSON")
    if not outputs_path:
        pytest.skip("INTEGRATION_AZURE_EMBEDDINGS_OUTPUTS_JSON is required")

    outputs = json.loads(Path(outputs_path).read_text(encoding="utf-8"))
    endpoint = outputs["openai_account_endpoint"]["value"].rstrip("/")
    scope = outputs["provider_scope"]["value"]
    deployments = outputs["provider_embeddings_deployments"]["value"]
    client_id = outputs["user_assigned_identity_client_id"]["value"]
    if not deployments:
        pytest.skip(
            "No embeddings deployments are enabled "
            "in the integration-azure-embeddings outputs"
        )
    return endpoint, scope, deployments, client_id


def test_embeddings_provider_probe_returns_real_vector_with_explicit_client_id() -> None:
    endpoint, scope, deployments, client_id = _require_integration_azure_embeddings()

    builder = AuthHeaderBuilder(
        secret_provider=UnusedSecretProvider(),
        token_provider=ManagedIdentityTokenProvider(),
    )
    invoker = HttpxOutboundInvoker()

    try:
        for deployment in deployments.values():
            headers = builder.build(
                AuthPolicy(
                    mode=AuthMode.MANAGED_IDENTITY,
                    scope=scope,
                    client_id=client_id,
                )
            )

            response = None
            for _attempt in range(1, 13):
                response = invoker.post_json(
                    endpoint=f"{endpoint}/openai/v1/embeddings",
                    body={
                        "model": deployment["azure_deployment_name"],
                        "input": "integration azure embeddings probe",
                    },
                    headers=headers,
                    timeout_ms=60000,
                )
                if response.status_code == 200:
                    body = response.json_body
                    if isinstance(body, dict):
                        data = body.get("data")
                        if isinstance(data, list) and data:
                            first = data[0]
                            if (
                                isinstance(first, dict)
                                and isinstance(first.get("embedding"), list)
                                and first["embedding"]
                            ):
                                break
                    time.sleep(2)
                    continue
                if response.status_code in {401, 403, 429, 500, 502, 503, 504}:
                    time.sleep(10)
                    continue
                break

            assert response is not None
            assert response.status_code == 200, response.text_body or str(response.json_body)
            assert isinstance(response.json_body, dict)
            data = response.json_body["data"]
            assert data
            assert data[0]["embedding"]
    finally:
        invoker.close()
