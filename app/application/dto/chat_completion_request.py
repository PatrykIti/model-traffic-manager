from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ChatCompletionRequest:
    deployment_id: str
    payload: Any
    request_id: str | None = None
