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


def _require_integration_azure_chat() -> tuple[str, str, dict[str, dict[str, str]], str]:
    if os.getenv("RUN_INTEGRATION_AZURE_CHAT") != "1":
        pytest.skip(
            "integration-azure-chat is only enabled in the dedicated Azure chat workflow"
        )

    outputs_path = os.getenv("INTEGRATION_AZURE_CHAT_OUTPUTS_JSON")
    if not outputs_path:
        pytest.skip("INTEGRATION_AZURE_CHAT_OUTPUTS_JSON is required")

    outputs = json.loads(Path(outputs_path).read_text(encoding="utf-8"))
    endpoint = outputs["openai_account_endpoint"]["value"].rstrip("/")
    scope = outputs["provider_scope"]["value"]
    deployments = outputs["provider_chat_deployments"]["value"]
    client_id = outputs["user_assigned_identity_client_id"]["value"]
    if not deployments:
        pytest.skip("No chat deployments are enabled in the integration-azure-chat outputs")
    return endpoint, scope, deployments, client_id


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


def test_chat_provider_probe_returns_real_response_with_explicit_client_id() -> None:
    endpoint, scope, deployments, client_id = _require_integration_azure_chat()

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
                    endpoint=f"{endpoint}/openai/v1/chat/completions",
                    body=_build_payload(deployment),
                    headers=headers,
                    timeout_ms=60000,
                )
                if response.status_code == 200:
                    body = response.json_body
                    if isinstance(body, dict) and _message_content(body).strip():
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
            assert _message_content(response.json_body).strip()
    finally:
        invoker.close()
