from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class EmbeddingsRequest:
    deployment_id: str
    payload: Any
    request_id: str | None = None
