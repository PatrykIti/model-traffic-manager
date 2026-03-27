from __future__ import annotations

from typing import Protocol


class TokenProvider(Protocol):
    def get_token(self, scope: str, client_id: str | None = None) -> str:
        """Return an outbound bearer token for the given scope and optional client ID."""
