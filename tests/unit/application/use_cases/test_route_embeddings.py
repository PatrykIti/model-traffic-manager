from __future__ import annotations

import pytest

from app.application.dto.embeddings_request import EmbeddingsRequest
from app.application.dto.outbound_response import OutboundResponse
from app.application.use_cases.route_embeddings import RouteEmbeddings
from app.domain.entities.deployment import Deployment
from app.domain.entities.upstream import Upstream
from app.domain.errors import DeploymentNotFound
from app.domain.services.tiered_failover_selector import TieredFailoverSelector
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
        return OutboundResponse(
            status_code=200,
            headers={},
            json_body={"data": [{"embedding": [0.1, 0.2, 0.3]}]},
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
            endpoint=f"https://example.invalid/embeddings-{index}",
            auth=auth_policy,
        )
        for index in range(upstream_count)
    )
    return Deployment(
        id="local-embeddings-check",
        kind="embeddings",
        protocol="openai_embeddings",
        routing_strategy="tiered_failover",
        max_concurrency=10,
        request_rate_per_second=5,
        upstreams=upstreams,
    )


def test_route_embeddings_returns_outbound_response() -> None:
    deployment = build_deployment(AuthPolicy(mode=AuthMode.NONE))
    repository = FakeDeploymentRepository({deployment.id: deployment})
    auth_builder = FakeAuthHeaderBuilder()
    outbound_invoker = FakeOutboundInvoker()
    use_case = RouteEmbeddings(
        deployment_repository=repository,
        auth_header_builder=auth_builder,
        outbound_invoker=outbound_invoker,
        routing_selector=TieredFailoverSelector(),
        timeout_ms=30000,
        max_attempts=3,
        retryable_status_codes=(429, 500, 502, 503, 504),
    )

    response = use_case.execute(
        EmbeddingsRequest(
            deployment_id="local-embeddings-check",
            payload={"input": "Hello"},
        )
    )

    assert response.status_code == 200
    assert response.json_body == {"data": [{"embedding": [0.1, 0.2, 0.3]}]}
    assert auth_builder.last_auth_policy == deployment.upstreams[0].auth
    assert outbound_invoker.last_call == {
        "endpoint": "https://example.invalid/embeddings-0",
        "body": {"input": "Hello"},
        "headers": {},
        "timeout_ms": 30000,
    }


def test_route_embeddings_uses_first_upstream_deterministically() -> None:
    deployment = build_deployment(AuthPolicy(mode=AuthMode.NONE), upstream_count=2)
    repository = FakeDeploymentRepository({deployment.id: deployment})
    auth_builder = FakeAuthHeaderBuilder()
    outbound_invoker = FakeOutboundInvoker()
    use_case = RouteEmbeddings(
        deployment_repository=repository,
        auth_header_builder=auth_builder,
        outbound_invoker=outbound_invoker,
        routing_selector=TieredFailoverSelector(),
        timeout_ms=30000,
        max_attempts=3,
        retryable_status_codes=(429, 500, 502, 503, 504),
    )

    use_case.execute(
        EmbeddingsRequest(
            deployment_id="local-embeddings-check",
            payload={"input": ["one", "two"]},
        )
    )

    assert outbound_invoker.last_call is not None
    assert outbound_invoker.last_call["endpoint"] == "https://example.invalid/embeddings-0"


def test_route_embeddings_supports_api_key_auth() -> None:
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
    use_case = RouteEmbeddings(
        deployment_repository=repository,
        auth_header_builder=auth_builder,
        outbound_invoker=outbound_invoker,
        routing_selector=TieredFailoverSelector(),
        timeout_ms=30000,
        max_attempts=3,
        retryable_status_codes=(429, 500, 502, 503, 504),
    )

    use_case.execute(
        EmbeddingsRequest(
            deployment_id="local-embeddings-check",
            payload={"input": "Hello"},
        )
    )

    assert outbound_invoker.last_call is not None
    assert outbound_invoker.last_call["headers"] == {"api-key": "resolved-secret"}


def test_route_embeddings_raises_when_deployment_is_missing() -> None:
    use_case = RouteEmbeddings(
        deployment_repository=FakeDeploymentRepository({}),
        auth_header_builder=FakeAuthHeaderBuilder(),
        outbound_invoker=FakeOutboundInvoker(),
        routing_selector=TieredFailoverSelector(),
        timeout_ms=30000,
        max_attempts=3,
        retryable_status_codes=(429, 500, 502, 503, 504),
    )

    with pytest.raises(DeploymentNotFound):
        use_case.execute(
            EmbeddingsRequest(
                deployment_id="missing-deployment",
                payload={"input": "Hello"},
            )
        )


def test_route_embeddings_retries_into_higher_tier_after_primary_failure() -> None:
    deployment = Deployment(
        id="local-embeddings-check",
        kind="embeddings",
        protocol="openai_embeddings",
        routing_strategy="tiered_failover",
        max_concurrency=10,
        request_rate_per_second=5,
        upstreams=(
            Upstream(
                id="primary-upstream",
                provider="internal_mock",
                account="local",
                region="local",
                tier=0,
                weight=100,
                endpoint="https://example.invalid/embeddings-primary",
                auth=AuthPolicy(mode=AuthMode.NONE),
            ),
            Upstream(
                id="secondary-upstream",
                provider="internal_mock",
                account="local",
                region="local",
                tier=1,
                weight=100,
                endpoint="https://example.invalid/embeddings-secondary",
                auth=AuthPolicy(mode=AuthMode.NONE),
            ),
        ),
    )
    repository = FakeDeploymentRepository({deployment.id: deployment})
    outbound_invoker = FakeOutboundInvoker(
        responses={
            "https://example.invalid/embeddings-primary": [
                OutboundResponse(status_code=503, headers={}, json_body={"error": "retry"}),
            ],
            "https://example.invalid/embeddings-secondary": [
                OutboundResponse(status_code=200, headers={}, json_body={"data": [{"index": 0}]}),
            ],
        }
    )
    use_case = RouteEmbeddings(
        deployment_repository=repository,
        auth_header_builder=FakeAuthHeaderBuilder(),
        outbound_invoker=outbound_invoker,
        routing_selector=TieredFailoverSelector(),
        timeout_ms=30000,
        max_attempts=3,
        retryable_status_codes=(429, 500, 502, 503, 504),
    )

    response = use_case.execute(
        EmbeddingsRequest(
            deployment_id="local-embeddings-check",
            payload={"input": "Hello"},
        )
    )

    assert response.status_code == 200
    assert [call["endpoint"] for call in outbound_invoker.calls] == [
        "https://example.invalid/embeddings-primary",
        "https://example.invalid/embeddings-secondary",
    ]
