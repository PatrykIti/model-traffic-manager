from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DeploymentSummary:
    id: str
    kind: str
    protocol: str
    consumer_role: str | None
    routing_strategy: str
    upstream_count: int
    providers: tuple[str, ...]
    regions: tuple[str, ...]
