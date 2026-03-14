from __future__ import annotations

from app.application.dto.runtime_event import RuntimeEvent
from app.application.ports.concurrency_limiter import ConcurrencyLimiter
from app.application.ports.request_rate_limiter import RequestRateLimiter
from app.application.ports.runtime_event_recorder import RuntimeEventRecorder
from app.domain.entities.deployment import Deployment
from app.domain.errors import ConcurrencyLimitExceededError, RequestRateLimitExceededError


class DeploymentLimitGuard:
    def __init__(
        self,
        request_rate_limiter: RequestRateLimiter,
        concurrency_limiter: ConcurrencyLimiter,
        runtime_event_recorder: RuntimeEventRecorder | None = None,
    ) -> None:
        self._request_rate_limiter = request_rate_limiter
        self._concurrency_limiter = concurrency_limiter
        self._runtime_event_recorder = runtime_event_recorder

    def acquire(
        self,
        deployment: Deployment,
        *,
        request_id: str | None = None,
        endpoint_kind: str,
    ) -> str:
        retry_after_seconds = self._request_rate_limiter.allow_request(
            deployment_id=deployment.id,
            requests_per_second=deployment.request_rate_per_second,
        )
        if retry_after_seconds is not None:
            self._record_event(
                RuntimeEvent(
                    event_type="limiter_rejected",
                    endpoint_kind=endpoint_kind,
                    deployment_id=deployment.id,
                    request_id=request_id,
                    limiter_reason="request_rate",
                    retry_after_seconds=retry_after_seconds,
                    outcome="rejected",
                )
            )
            raise RequestRateLimitExceededError(
                deployment_id=deployment.id,
                retry_after_seconds=retry_after_seconds,
            )

        lease_id = self._concurrency_limiter.acquire(
            deployment_id=deployment.id,
            max_concurrency=deployment.max_concurrency,
        )
        if lease_id is None:
            self._record_event(
                RuntimeEvent(
                    event_type="limiter_rejected",
                    endpoint_kind=endpoint_kind,
                    deployment_id=deployment.id,
                    request_id=request_id,
                    limiter_reason="concurrency",
                    outcome="rejected",
                )
            )
            raise ConcurrencyLimitExceededError(deployment.id)

        return lease_id

    def release(self, deployment_id: str, lease_id: str) -> None:
        self._concurrency_limiter.release(deployment_id, lease_id)

    def _record_event(self, event: RuntimeEvent) -> None:
        if self._runtime_event_recorder is not None:
            self._runtime_event_recorder.record(event)
