from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RuntimeEvent:
    event_type: str
    endpoint_kind: str
    deployment_id: str
    request_id: str | None = None
    attempt: int | None = None
    upstream_id: str | None = None
    provider: str | None = None
    account: str | None = None
    region: str | None = None
    selected_tier: int | None = None
    decision_reason: str | None = None
    outcome: str | None = None
    failure_reason: str | None = None
    health_status: str | None = None
    limiter_reason: str | None = None
    retry_after_seconds: int | None = None
    status_code: int | None = None
