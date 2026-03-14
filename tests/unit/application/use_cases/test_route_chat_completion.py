from __future__ import annotations

import pytest

from app.application.dto.chat_completion_request import ChatCompletionRequest
from app.application.dto.outbound_response import OutboundResponse
from app.application.use_cases.route_chat_completion import RouteChatCompletion
from app.domain.entities.deployment import Deployment
from app.domain.entities.upstream import Upstream
from app.domain.errors import DeploymentNotFound
from app.domain.services.health_state_policy import HealthStatePolicy
from app.domain.services.tiered_failover_selector import TieredFailoverSelector
from app.domain.services.upstream_failure_classifier import UpstreamFailureClassifier
from app.domain.value_objects.auth_policy import AuthMode, AuthPolicy
from app.infrastructure.health.in_memory_health_state_repository import (
    InMemoryHealthStateRepository,
)


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
    def __init__(self, responses: dict[str, list[OutboundResponse]] | None = None) -> None:
        self.last_call: dict[str, object] | None = None
        self.calls: list[dict[str, object]] = []
        self._responses = responses or {}

    def post_json(
        self,
        endpoint: str,
        body: object,
        headers: dict[str, str],
        timeout_ms: int,
    ) -> OutboundResponse:
        call = {
            "endpoint": endpoint,
            "body": body,
            "headers": headers,
            "timeout_ms": timeout_ms,
        }
        self.last_call = call
        self.calls.append(call)
        queued_responses = self._responses.get(endpoint)
        if queued_responses:
            return queued_responses.pop(0)
        return OutboundResponse(status_code=200, headers={}, json_body={"ok": True})


def build_health_components() -> tuple[
    InMemoryHealthStateRepository,
    UpstreamFailureClassifier,
    HealthStatePolicy,
]:
    return (
        InMemoryHealthStateRepository(),
        UpstreamFailureClassifier(),
        HealthStatePolicy(
            failure_threshold=2,
            cooldown_seconds=30,
            half_open_after_seconds=60,
            now_provider=lambda: 100,
        ),
    )


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


def build_same_tier_deployment(auth_policy: AuthPolicy) -> Deployment:
    return Deployment(
        id="local-health-check",
        kind="llm",
        protocol="openai_chat",
        routing_strategy="tiered_failover",
        max_concurrency=10,
        request_rate_per_second=5,
        upstreams=(
            Upstream(
                id="upstream-0",
                provider="internal_mock",
                account="local",
                region="local",
                tier=0,
                weight=100,
                endpoint="https://example.invalid/chat-0",
                auth=auth_policy,
            ),
            Upstream(
                id="upstream-1",
                provider="internal_mock",
                account="local",
                region="local",
                tier=0,
                weight=100,
                endpoint="https://example.invalid/chat-1",
                auth=auth_policy,
            ),
        ),
    )


def test_route_chat_completion_returns_outbound_response() -> None:
    deployment = build_deployment(AuthPolicy(mode=AuthMode.NONE))
    repository = FakeDeploymentRepository({deployment.id: deployment})
    auth_builder = FakeAuthHeaderBuilder()
    outbound_invoker = FakeOutboundInvoker()
    health_state_repository, failure_classifier, health_state_policy = build_health_components()
    use_case = RouteChatCompletion(
        deployment_repository=repository,
        auth_header_builder=auth_builder,
        outbound_invoker=outbound_invoker,
        health_state_repository=health_state_repository,
        failure_classifier=failure_classifier,
        health_state_policy=health_state_policy,
        routing_selector=TieredFailoverSelector(),
        timeout_ms=30000,
        max_attempts=3,
        retryable_status_codes=(429, 500, 502, 503, 504),
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
    health_state_repository, failure_classifier, health_state_policy = build_health_components()
    use_case = RouteChatCompletion(
        deployment_repository=repository,
        auth_header_builder=auth_builder,
        outbound_invoker=outbound_invoker,
        health_state_repository=health_state_repository,
        failure_classifier=failure_classifier,
        health_state_policy=health_state_policy,
        routing_selector=TieredFailoverSelector(),
        timeout_ms=30000,
        max_attempts=3,
        retryable_status_codes=(429, 500, 502, 503, 504),
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
    health_state_repository, failure_classifier, health_state_policy = build_health_components()
    use_case = RouteChatCompletion(
        deployment_repository=repository,
        auth_header_builder=auth_builder,
        outbound_invoker=outbound_invoker,
        health_state_repository=health_state_repository,
        failure_classifier=failure_classifier,
        health_state_policy=health_state_policy,
        routing_selector=TieredFailoverSelector(),
        timeout_ms=30000,
        max_attempts=3,
        retryable_status_codes=(429, 500, 502, 503, 504),
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
    health_state_repository, failure_classifier, health_state_policy = build_health_components()
    use_case = RouteChatCompletion(
        deployment_repository=FakeDeploymentRepository({}),
        auth_header_builder=FakeAuthHeaderBuilder(),
        outbound_invoker=FakeOutboundInvoker(),
        health_state_repository=health_state_repository,
        failure_classifier=failure_classifier,
        health_state_policy=health_state_policy,
        routing_selector=TieredFailoverSelector(),
        timeout_ms=30000,
        max_attempts=3,
        retryable_status_codes=(429, 500, 502, 503, 504),
    )

    with pytest.raises(DeploymentNotFound):
        use_case.execute(
            ChatCompletionRequest(
                deployment_id="missing-deployment",
                payload={"messages": []},
            )
        )


def test_route_chat_completion_retries_within_same_tier_before_returning() -> None:
    deployment = build_same_tier_deployment(AuthPolicy(mode=AuthMode.NONE))
    repository = FakeDeploymentRepository({deployment.id: deployment})
    auth_builder = FakeAuthHeaderBuilder()
    outbound_invoker = FakeOutboundInvoker(
        responses={
            "https://example.invalid/chat-0": [
                OutboundResponse(status_code=503, headers={}, json_body={"error": "retry"}),
            ],
            "https://example.invalid/chat-1": [
                OutboundResponse(status_code=200, headers={}, json_body={"ok": True}),
            ],
        }
    )
    health_state_repository, failure_classifier, health_state_policy = build_health_components()
    use_case = RouteChatCompletion(
        deployment_repository=repository,
        auth_header_builder=auth_builder,
        outbound_invoker=outbound_invoker,
        health_state_repository=health_state_repository,
        failure_classifier=failure_classifier,
        health_state_policy=health_state_policy,
        routing_selector=TieredFailoverSelector(),
        timeout_ms=30000,
        max_attempts=3,
        retryable_status_codes=(429, 500, 502, 503, 504),
    )

    response = use_case.execute(
        ChatCompletionRequest(
            deployment_id="local-health-check",
            payload={"messages": [{"role": "user", "content": "Hello"}]},
        )
    )

    assert response.status_code == 200
    assert [call["endpoint"] for call in outbound_invoker.calls] == [
        "https://example.invalid/chat-0",
        "https://example.invalid/chat-1",
    ]


def test_route_chat_completion_does_not_retry_non_retriable_response() -> None:
    deployment = build_deployment(AuthPolicy(mode=AuthMode.NONE), upstream_count=2)
    repository = FakeDeploymentRepository({deployment.id: deployment})
    auth_builder = FakeAuthHeaderBuilder()
    outbound_invoker = FakeOutboundInvoker(
        responses={
            "https://example.invalid/chat-0": [
                OutboundResponse(status_code=400, headers={}, json_body={"error": "bad_request"}),
            ],
        }
    )
    health_state_repository, failure_classifier, health_state_policy = build_health_components()
    use_case = RouteChatCompletion(
        deployment_repository=repository,
        auth_header_builder=auth_builder,
        outbound_invoker=outbound_invoker,
        health_state_repository=health_state_repository,
        failure_classifier=failure_classifier,
        health_state_policy=health_state_policy,
        routing_selector=TieredFailoverSelector(),
        timeout_ms=30000,
        max_attempts=3,
        retryable_status_codes=(429, 500, 502, 503, 504),
    )

    response = use_case.execute(
        ChatCompletionRequest(
            deployment_id="local-health-check",
            payload={"messages": [{"role": "user", "content": "Hello"}]},
        )
    )

    assert response.status_code == 400
    assert [call["endpoint"] for call in outbound_invoker.calls] == [
        "https://example.invalid/chat-0"
    ]
