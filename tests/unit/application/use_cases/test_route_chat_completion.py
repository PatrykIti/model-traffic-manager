from __future__ import annotations

import pytest

from app.application.dto.chat_completion_request import ChatCompletionRequest
from app.application.dto.outbound_response import OutboundResponse
from app.application.use_cases.route_chat_completion import RouteChatCompletion
from app.domain.entities.deployment import Deployment
from app.domain.entities.upstream import Upstream
from app.domain.errors import DeploymentNotFound
from app.domain.value_objects.auth_policy import AuthMode, AuthPolicy


class FakeDeploymentRepository:
    def __init__(self, deployments: dict[str, Deployment]) -> None:
        self._deployments = deployments

    def list_deployments(self) -> tuple[Deployment, ...]:
        return tuple(self._deployments.values())

    def get_deployment(self, deployment_id: str) -> Deployment | None:
        return self._deployments.get(deployment_id)


class FakeAuthHeaderBuilder:
    def __init__(self) -> None:
        self.last_auth_policy: AuthPolicy | None = None

    def build(self, auth_policy: AuthPolicy) -> dict[str, str]:
        self.last_auth_policy = auth_policy
        if auth_policy.mode is AuthMode.API_KEY:
            return {"api-key": "resolved-secret"}
        return {}


class FakeOutboundInvoker:
    def __init__(self) -> None:
        self.last_call: dict[str, object] | None = None

    def post_json(
        self,
        endpoint: str,
        body: object,
        headers: dict[str, str],
        timeout_ms: int,
    ) -> OutboundResponse:
        self.last_call = {
            "endpoint": endpoint,
            "body": body,
            "headers": headers,
            "timeout_ms": timeout_ms,
        }
        return OutboundResponse(status_code=200, headers={}, json_body={"ok": True})


def build_deployment(auth_policy: AuthPolicy, *, upstream_count: int = 1) -> Deployment:
    upstreams = tuple(
        Upstream(
            id=f"upstream-{index}",
            provider="internal_mock",
            account="local",
            region="local",
            tier=index,
            weight=100,
            endpoint=f"https://example.invalid/chat-{index}",
            auth=auth_policy,
        )
        for index in range(upstream_count)
    )
    return Deployment(
        id="local-health-check",
        kind="llm",
        protocol="openai_chat",
        routing_strategy="tiered_failover",
        max_concurrency=10,
        request_rate_per_second=5,
        upstreams=upstreams,
    )


def test_route_chat_completion_returns_outbound_response() -> None:
    deployment = build_deployment(AuthPolicy(mode=AuthMode.NONE))
    repository = FakeDeploymentRepository({deployment.id: deployment})
    auth_builder = FakeAuthHeaderBuilder()
    outbound_invoker = FakeOutboundInvoker()
    use_case = RouteChatCompletion(
        deployment_repository=repository,
        auth_header_builder=auth_builder,
        outbound_invoker=outbound_invoker,
        timeout_ms=30000,
    )

    response = use_case.execute(
        ChatCompletionRequest(
            deployment_id="local-health-check",
            payload={"messages": [{"role": "user", "content": "Hello"}]},
        )
    )

    assert response.status_code == 200
    assert response.json_body == {"ok": True}
    assert auth_builder.last_auth_policy == deployment.upstreams[0].auth
    assert outbound_invoker.last_call == {
        "endpoint": "https://example.invalid/chat-0",
        "body": {"messages": [{"role": "user", "content": "Hello"}]},
        "headers": {},
        "timeout_ms": 30000,
    }


def test_route_chat_completion_uses_first_upstream_deterministically() -> None:
    deployment = build_deployment(AuthPolicy(mode=AuthMode.NONE), upstream_count=2)
    repository = FakeDeploymentRepository({deployment.id: deployment})
    auth_builder = FakeAuthHeaderBuilder()
    outbound_invoker = FakeOutboundInvoker()
    use_case = RouteChatCompletion(
        deployment_repository=repository,
        auth_header_builder=auth_builder,
        outbound_invoker=outbound_invoker,
        timeout_ms=30000,
    )

    use_case.execute(
        ChatCompletionRequest(
            deployment_id="local-health-check",
            payload={"messages": []},
        )
    )

    assert outbound_invoker.last_call is not None
    assert outbound_invoker.last_call["endpoint"] == "https://example.invalid/chat-0"


def test_route_chat_completion_supports_api_key_auth() -> None:
    deployment = build_deployment(
        AuthPolicy(
            mode=AuthMode.API_KEY,
            header_name="api-key",
            secret_ref="env://UPSTREAM_API_KEY",
        )
    )
    repository = FakeDeploymentRepository({deployment.id: deployment})
    auth_builder = FakeAuthHeaderBuilder()
    outbound_invoker = FakeOutboundInvoker()
    use_case = RouteChatCompletion(
        deployment_repository=repository,
        auth_header_builder=auth_builder,
        outbound_invoker=outbound_invoker,
        timeout_ms=30000,
    )

    use_case.execute(
        ChatCompletionRequest(
            deployment_id="local-health-check",
            payload={"messages": []},
        )
    )

    assert outbound_invoker.last_call is not None
    assert outbound_invoker.last_call["headers"] == {"api-key": "resolved-secret"}


def test_route_chat_completion_raises_when_deployment_is_missing() -> None:
    use_case = RouteChatCompletion(
        deployment_repository=FakeDeploymentRepository({}),
        auth_header_builder=FakeAuthHeaderBuilder(),
        outbound_invoker=FakeOutboundInvoker(),
        timeout_ms=30000,
    )

    with pytest.raises(DeploymentNotFound):
        use_case.execute(
            ChatCompletionRequest(
                deployment_id="missing-deployment",
                payload={"messages": []},
            )
        )
