from __future__ import annotations

from typing import Protocol


class SecretProvider(Protocol):
    def get_secret(self, secret_ref: str) -> str:
        """Resolve secret material for the given reference."""
