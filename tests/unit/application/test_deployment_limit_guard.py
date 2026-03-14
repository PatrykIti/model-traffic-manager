from __future__ import annotations

import pytest

from app.application.deployment_limit_guard import DeploymentLimitGuard
from app.application.dto.runtime_event import RuntimeEvent
from app.domain.entities.deployment import Deployment
from app.domain.entities.upstream import Upstream
from app.domain.errors import ConcurrencyLimitExceededError, RequestRateLimitExceededError
from app.domain.value_objects.auth_policy import AuthMode, AuthPolicy


class FakeRequestRateLimiter:
    def __init__(self, retry_after_seconds: int | None = None) -> None:
        self._retry_after_seconds = retry_after_seconds

    def allow_request(self, deployment_id: str, requests_per_second: int) -> int | None:
        return self._retry_after_seconds


class FakeConcurrencyLimiter:
    def __init__(self, lease_id: str | None = "lease-1") -> None:
        self._lease_id = lease_id
        self.released: list[tuple[str, str]] = []

    def acquire(self, deployment_id: str, max_concurrency: int) -> str | None:
        return self._lease_id

    def release(self, deployment_id: str, lease_id: str) -> None:
        self.released.append((deployment_id, lease_id))


class FakeRuntimeEventRecorder:
    def __init__(self) -> None:
        self.events: list[RuntimeEvent] = []

    def record(self, event: RuntimeEvent) -> None:
        self.events.append(event)


def build_deployment() -> Deployment:
    return Deployment(
        id="deployment-a",
        kind="llm",
        protocol="openai_chat",
        routing_strategy="tiered_failover",
        max_concurrency=2,
        request_rate_per_second=1,
        upstreams=(
            Upstream(
                id="upstream-a",
                provider="internal_mock",
                account="local",
                region="local",
                tier=0,
                weight=100,
                endpoint="https://example.invalid/chat",
                auth=AuthPolicy(mode=AuthMode.NONE),
            ),
        ),
    )


def test_limit_guard_acquires_and_releases_concurrency_slot() -> None:
    concurrency_limiter = FakeConcurrencyLimiter()
    guard = DeploymentLimitGuard(
        request_rate_limiter=FakeRequestRateLimiter(),
        concurrency_limiter=concurrency_limiter,
    )

    lease_id = guard.acquire(
        build_deployment(),
        request_id="req-0",
        endpoint_kind="chat_completions",
    )
    guard.release("deployment-a", lease_id)

    assert lease_id == "lease-1"
    assert concurrency_limiter.released == [("deployment-a", "lease-1")]


def test_limit_guard_raises_rate_limit_error() -> None:
    event_recorder = FakeRuntimeEventRecorder()
    guard = DeploymentLimitGuard(
        request_rate_limiter=FakeRequestRateLimiter(retry_after_seconds=1),
        concurrency_limiter=FakeConcurrencyLimiter(),
        runtime_event_recorder=event_recorder,
    )

    with pytest.raises(RequestRateLimitExceededError):
        guard.acquire(build_deployment(), request_id="req-1", endpoint_kind="chat_completions")

    assert event_recorder.events[0].event_type == "limiter_rejected"
    assert event_recorder.events[0].limiter_reason == "request_rate"


def test_limit_guard_raises_concurrency_error() -> None:
    event_recorder = FakeRuntimeEventRecorder()
    guard = DeploymentLimitGuard(
        request_rate_limiter=FakeRequestRateLimiter(),
        concurrency_limiter=FakeConcurrencyLimiter(lease_id=None),
        runtime_event_recorder=event_recorder,
    )

    with pytest.raises(ConcurrencyLimitExceededError):
        guard.acquire(build_deployment(), request_id="req-2", endpoint_kind="embeddings")

    assert event_recorder.events[0].event_type == "limiter_rejected"
    assert event_recorder.events[0].limiter_reason == "concurrency"
