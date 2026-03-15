from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SharedServiceSummary:
    name: str
    endpoint: str
    auth_mode: str
