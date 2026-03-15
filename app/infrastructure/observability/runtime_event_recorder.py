from __future__ import annotations

from opentelemetry import trace
from prometheus_client import Counter, Histogram, generate_latest

from app.application.dto.runtime_event import RuntimeEvent
from app.application.ports.runtime_event_recorder import RuntimeEventRecorder
from app.infrastructure.observability.logging import get_logger

_ROUTE_ATTEMPTS = Counter(
    "router_route_attempts_total",
    "Number of upstream attempts performed by the router.",
    ["endpoint_kind", "deployment_id"],
)
_ROUTE_RESULTS = Counter(
    "router_route_results_total",
    "Number of routed request outcomes observed by the router.",
    ["endpoint_kind", "deployment_id", "outcome"],
)
_LIMITER_REJECTIONS = Counter(
    "router_limiter_rejections_total",
    "Number of limiter rejections issued by the router.",
    ["endpoint_kind", "deployment_id", "reason"],
)
_HEALTH_STATE_UPDATES = Counter(
    "router_health_state_updates_total",
    "Number of health-state updates recorded by the router.",
    ["deployment_id", "status"],
)
_REQUEST_DURATION = Histogram(
    "router_request_duration_seconds",
    "Observed request duration for router entrypoints.",
    ["endpoint_kind"],
)


class StructuredRuntimeEventRecorder(RuntimeEventRecorder):
    def __init__(self) -> None:
        self._logger = get_logger(__name__)

    def record(self, event: RuntimeEvent) -> None:
        payload = {
            "event_type": event.event_type,
            "endpoint_kind": event.endpoint_kind,
            "deployment_id": event.deployment_id,
            "request_id": event.request_id,
            "attempt": event.attempt,
            "upstream_id": event.upstream_id,
            "provider": event.provider,
            "account": event.account,
            "region": event.region,
            "selected_tier": event.selected_tier,
            "decision_reason": event.decision_reason,
            "failover_reason": event.failover_reason,
            "outcome": event.outcome,
            "failure_reason": event.failure_reason,
            "health_status": event.health_status,
            "limiter_reason": event.limiter_reason,
            "retry_after_seconds": event.retry_after_seconds,
            "status_code": event.status_code,
            "rejected_candidates": [
                {
                    "upstream_id": candidate.upstream_id,
                    "provider": candidate.provider,
                    "account": candidate.account,
                    "region": candidate.region,
                    "tier": candidate.tier,
                    "reason": candidate.reason,
                }
                for candidate in event.rejected_candidates
            ],
        }
        self._logger.info("runtime_event", **payload)
        self._record_metrics(event)
        self._record_trace_event(event)

    def _record_metrics(self, event: RuntimeEvent) -> None:
        if event.event_type == "route_selected":
            _ROUTE_ATTEMPTS.labels(event.endpoint_kind, event.deployment_id).inc()
            return
        if event.event_type == "request_completed" and event.outcome is not None:
            _ROUTE_RESULTS.labels(event.endpoint_kind, event.deployment_id, event.outcome).inc()
            return
        if event.event_type == "limiter_rejected" and event.limiter_reason is not None:
            _LIMITER_REJECTIONS.labels(
                event.endpoint_kind,
                event.deployment_id,
                event.limiter_reason,
            ).inc()
            return
        if event.event_type == "health_state_updated" and event.health_status is not None:
            _HEALTH_STATE_UPDATES.labels(event.deployment_id, event.health_status).inc()

    def _record_trace_event(self, event: RuntimeEvent) -> None:
        span = trace.get_current_span()
        if span is None or not span.is_recording():
            return
        attributes: dict[str, str | int] = {
            "router.event_type": event.event_type,
            "router.endpoint_kind": event.endpoint_kind,
            "router.deployment_id": event.deployment_id,
        }
        if event.request_id is not None:
            attributes["router.request_id"] = event.request_id
        if event.upstream_id is not None:
            attributes["router.upstream_id"] = event.upstream_id
        if event.decision_reason is not None:
            attributes["router.decision_reason"] = event.decision_reason
        if event.failover_reason is not None:
            attributes["router.failover_reason"] = event.failover_reason
        if event.failure_reason is not None:
            attributes["router.failure_reason"] = event.failure_reason
        if event.health_status is not None:
            attributes["router.health_status"] = event.health_status
        if event.limiter_reason is not None:
            attributes["router.limiter_reason"] = event.limiter_reason
        if event.status_code is not None:
            attributes["http.status_code"] = event.status_code
        span.add_event(event.event_type, attributes=attributes)


def metrics_payload() -> bytes:
    return generate_latest()


def observe_request_duration(endpoint_kind: str, duration_seconds: float) -> None:
    _REQUEST_DURATION.labels(endpoint_kind).observe(duration_seconds)
