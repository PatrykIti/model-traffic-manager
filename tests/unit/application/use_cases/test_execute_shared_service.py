from __future__ import annotations

from dataclasses import dataclass

import pytest

from app.application.deployment_limit_guard import DeploymentLimitGuard
from app.application.dto.outbound_response import OutboundResponse
from app.application.dto.shared_service_request import SharedServiceRequest
from app.application.use_cases.route_shared_service import RouteSharedService
from app.domain.entities.shared_service import (
    SharedService,
    SharedServiceAccessMode,
    SharedServiceRoutingStrategy,
    SharedServiceTransport,
)
from app.domain.entities.upstream import Upstream
from app.domain.errors import SharedServiceExecutionDisabledError, SharedServiceNotFound
from app.domain.services.health_state_policy import HealthStatePolicy
from app.domain.services.tiered_failover_selector import TieredFailoverSelector
from app.domain.services.upstream_failure_classifier import UpstreamFailureClassifier
from app.domain.value_objects.auth_policy import AuthMode, AuthPolicy
from app.infrastructure.health.in_memory_health_state_repository import (
    InMemoryHealthStateRepository,
)
from app.infrastructure.limits.in_memory_concurrency_limiter import InMemoryConcurrencyLimiter
from app.infrastructure.limits.in_memory_request_rate_limiter import InMemoryRequestRateLimiter


@dataclass
class FakeSharedServiceRepository:
    shared_services: tuple[SharedService, ...]

    def list_shared_services(self) -> tuple[SharedService, ...]:
        return self.shared_services

    def get_shared_service(self, name: str) -> SharedService | None:
        for shared_service in self.shared_services:
            if shared_service.name == name:
                return shared_service
        return None


class FakeAuthHeaderBuilder:
    def build(self, auth_policy: AuthPolicy) -> dict[str, str]:
        if auth_policy.mode is AuthMode.API_KEY:
            return {"api-key": "resolved-secret"}
        return {}


class FakeOutboundInvoker:
    def __init__(self, responses: dict[str, list[OutboundResponse]] | None = None) -> None:
        self._responses = responses or {}
        self.calls: list[dict[str, object]] = []

    def post_json(
        self,
        endpoint: str,
        body: object,
        headers: dict[str, str],
        timeout_ms: int,
    ) -> OutboundResponse:
        self.calls.append(
            {
                "endpoint": endpoint,
                "body": body,
                "headers": headers,
                "timeout_ms": timeout_ms,
            }
        )
        queued_responses = self._responses.get(endpoint)
        if queued_responses:
            return queued_responses.pop(0)
        return OutboundResponse(status_code=200, headers={}, json_body={"ok": True})


def build_limit_guard() -> DeploymentLimitGuard:
    return DeploymentLimitGuard(
        request_rate_limiter=InMemoryRequestRateLimiter(now_provider=lambda: 100),
        concurrency_limiter=InMemoryConcurrencyLimiter(),
    )


def build_tiered_service() -> SharedService:
    return SharedService(
        name="transcript-search",
        transport=SharedServiceTransport.HTTP_JSON,
        access_mode=SharedServiceAccessMode.ROUTER_PROXY,
        provider_managed_availability=False,
        routing_strategy=SharedServiceRoutingStrategy.TIERED_FAILOVER,
        max_concurrency=10,
        request_rate_per_second=5,
        upstreams=(
            Upstream(
                id="primary",
                provider="internal_api",
                account="platform",
                region="westeurope",
                tier=0,
                weight=100,
                endpoint="https://example.invalid/shared-primary",
                auth=AuthPolicy(mode=AuthMode.NONE),
            ),
            Upstream(
                id="secondary",
                provider="internal_api",
                account="platform",
                region="northeurope",
                tier=1,
                weight=100,
                endpoint="https://example.invalid/shared-secondary",
                auth=AuthPolicy(mode=AuthMode.NONE),
            ),
        ),
    )


def build_single_endpoint_service() -> SharedService:
    return SharedService(
        name="transcript-registry",
        transport=SharedServiceTransport.HTTP_JSON,
        access_mode=SharedServiceAccessMode.ROUTER_PROXY,
        provider_managed_availability=True,
        routing_strategy=SharedServiceRoutingStrategy.SINGLE_ENDPOINT,
        max_concurrency=10,
        request_rate_per_second=5,
        upstreams=(
            Upstream(
                id="primary",
                provider="internal_api",
                account="platform",
                region="local",
                tier=0,
                weight=100,
                endpoint="https://example.invalid/shared-registry",
                auth=AuthPolicy(mode=AuthMode.NONE),
            ),
        ),
    )


def build_direct_service() -> SharedService:
    return SharedService(
        name="conversation-archive",
        transport=SharedServiceTransport.HTTP_JSON,
        access_mode=SharedServiceAccessMode.DIRECT_BACKEND_ACCESS,
        provider_managed_availability=True,
        provider="azure_storage",
        account="archive",
        region="westeurope",
        endpoint="https://archive.example.invalid",
        auth=AuthPolicy(
            mode=AuthMode.MANAGED_IDENTITY,
            scope="https://storage.azure.com/.default",
        ),
    )


def test_execute_shared_service_raises_when_service_is_missing() -> None:
    use_case = RouteSharedService(
        shared_service_repository=FakeSharedServiceRepository(shared_services=()),
        auth_header_builder=FakeAuthHeaderBuilder(),
        outbound_invoker=FakeOutboundInvoker(),
        deployment_limit_guard=build_limit_guard(),
        health_state_repository=InMemoryHealthStateRepository(),
        failure_classifier=UpstreamFailureClassifier(),
        health_state_policy=HealthStatePolicy(
            failure_threshold=2,
            cooldown_seconds=30,
            half_open_after_seconds=60,
            now_provider=lambda: 100,
        ),
        routing_selector=TieredFailoverSelector(),
        timeout_ms=30000,
        max_attempts=3,
        retryable_status_codes=(429, 500, 502, 503, 504),
    )

    with pytest.raises(SharedServiceNotFound):
        use_case.execute(SharedServiceRequest(service_id="missing", payload={"q": "hello"}))


def test_execute_shared_service_rejects_direct_access_services() -> None:
    service = build_direct_service()
    use_case = RouteSharedService(
        shared_service_repository=FakeSharedServiceRepository(shared_services=(service,)),
        auth_header_builder=FakeAuthHeaderBuilder(),
        outbound_invoker=FakeOutboundInvoker(),
        deployment_limit_guard=build_limit_guard(),
        health_state_repository=InMemoryHealthStateRepository(),
        failure_classifier=UpstreamFailureClassifier(),
        health_state_policy=HealthStatePolicy(
            failure_threshold=2,
            cooldown_seconds=30,
            half_open_after_seconds=60,
            now_provider=lambda: 100,
        ),
        routing_selector=TieredFailoverSelector(),
        timeout_ms=30000,
        max_attempts=3,
        retryable_status_codes=(429, 500, 502, 503, 504),
    )

    with pytest.raises(SharedServiceExecutionDisabledError):
        use_case.execute(SharedServiceRequest(service_id=service.name, payload={"q": "hello"}))


def test_execute_shared_service_routes_single_endpoint_service() -> None:
    service = build_single_endpoint_service()
    outbound_invoker = FakeOutboundInvoker(
        responses={
            "https://example.invalid/shared-registry": [
                OutboundResponse(status_code=200, headers={}, json_body={"status": "stored"}),
            ],
        }
    )
    use_case = RouteSharedService(
        shared_service_repository=FakeSharedServiceRepository(shared_services=(service,)),
        auth_header_builder=FakeAuthHeaderBuilder(),
        outbound_invoker=outbound_invoker,
        deployment_limit_guard=build_limit_guard(),
        health_state_repository=InMemoryHealthStateRepository(),
        failure_classifier=UpstreamFailureClassifier(),
        health_state_policy=HealthStatePolicy(
            failure_threshold=2,
            cooldown_seconds=30,
            half_open_after_seconds=60,
            now_provider=lambda: 100,
        ),
        routing_selector=TieredFailoverSelector(),
        timeout_ms=30000,
        max_attempts=3,
        retryable_status_codes=(429, 500, 502, 503, 504),
    )

    response = use_case.execute(
        SharedServiceRequest(service_id=service.name, payload={"event_id": "evt-1"})
    )

    assert response.status_code == 200
    assert [call["endpoint"] for call in outbound_invoker.calls] == [
        "https://example.invalid/shared-registry"
    ]


def test_execute_shared_service_fails_over_for_tiered_shared_service() -> None:
    service = build_tiered_service()
    outbound_invoker = FakeOutboundInvoker(
        responses={
            "https://example.invalid/shared-primary": [
                OutboundResponse(status_code=503, headers={}, json_body={"error": "retry"}),
            ],
            "https://example.invalid/shared-secondary": [
                OutboundResponse(status_code=200, headers={}, json_body={"ok": True}),
            ],
        }
    )
    use_case = RouteSharedService(
        shared_service_repository=FakeSharedServiceRepository(shared_services=(service,)),
        auth_header_builder=FakeAuthHeaderBuilder(),
        outbound_invoker=outbound_invoker,
        deployment_limit_guard=build_limit_guard(),
        health_state_repository=InMemoryHealthStateRepository(),
        failure_classifier=UpstreamFailureClassifier(),
        health_state_policy=HealthStatePolicy(
            failure_threshold=2,
            cooldown_seconds=30,
            half_open_after_seconds=60,
            now_provider=lambda: 100,
        ),
        routing_selector=TieredFailoverSelector(),
        timeout_ms=30000,
        max_attempts=3,
        retryable_status_codes=(429, 500, 502, 503, 504),
    )

    response = use_case.execute(
        SharedServiceRequest(service_id=service.name, payload={"event_id": "evt-1"})
    )

    assert response.status_code == 200
    assert [call["endpoint"] for call in outbound_invoker.calls] == [
        "https://example.invalid/shared-primary",
        "https://example.invalid/shared-secondary",
    ]
