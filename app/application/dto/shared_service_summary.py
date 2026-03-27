from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SharedServiceSummary:
    name: str
    transport: str
    access_mode: str
    consumer_role: str | None
    routing_strategy: str | None
    provider_managed_availability: bool
    router_callable: bool
    upstream_count: int
    providers: tuple[str, ...]
    regions: tuple[str, ...]
    endpoint: str | None
    auth_mode: str | None
