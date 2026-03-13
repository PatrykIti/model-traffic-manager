from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class OutboundResponse:
    status_code: int
    headers: dict[str, str]
    json_body: Any | None = None
    text_body: str | None = None

    @property
    def content_type(self) -> str | None:
        return self.headers.get("content-type")
