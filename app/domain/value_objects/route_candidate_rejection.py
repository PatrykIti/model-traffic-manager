from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RouteCandidateRejection:
    upstream_id: str
    provider: str
    account: str
    region: str
    tier: int
    reason: str
