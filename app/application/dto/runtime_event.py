from __future__ import annotations

from dataclasses import dataclass
from typing import TypedDict

from app.domain.entities.upstream import Upstream
from app.domain.value_objects.route_candidate_rejection import RouteCandidateRejection


@dataclass(frozen=True, slots=True)
class RuntimeEvent:
    event_type: str
    endpoint_kind: str
    deployment_id: str
    consumer_role: str | None = None
    request_id: str | None = None
    attempt: int | None = None
    upstream_id: str | None = None
    provider: str | None = None
    account: str | None = None
    region: str | None = None
    model_name: str | None = None
    model_version: str | None = None
    deployment_name: str | None = None
    capacity_mode: str | None = None
    auth_mode: str | None = None
    selected_tier: int | None = None
    decision_reason: str | None = None
    failover_reason: str | None = None
    outcome: str | None = None
    failure_reason: str | None = None
    health_status: str | None = None
    limiter_reason: str | None = None
    retry_after_seconds: int | None = None
    status_code: int | None = None
    rejected_candidates: tuple[RouteCandidateRejection, ...] = ()


class UpstreamRuntimeMetadata(TypedDict):
    consumer_role: str | None
    upstream_id: str
    provider: str
    account: str
    region: str
    model_name: str | None
    model_version: str | None
    deployment_name: str | None
    capacity_mode: str | None
    auth_mode: str | None


def upstream_runtime_metadata(
    upstream: Upstream,
    *,
    consumer_role: str | None,
) -> UpstreamRuntimeMetadata:
    return {
        "consumer_role": consumer_role,
        "upstream_id": upstream.id,
        "provider": upstream.provider,
        "account": upstream.account,
        "region": upstream.region,
        "model_name": upstream.model_name,
        "model_version": upstream.model_version,
        "deployment_name": upstream.deployment_name,
        "capacity_mode": (
            upstream.capacity_mode.value if upstream.capacity_mode is not None else None
        ),
        "auth_mode": upstream.auth.mode.value,
    }
