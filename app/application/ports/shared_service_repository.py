from __future__ import annotations

from typing import Protocol

from app.domain.entities.shared_service import SharedService


class SharedServiceRepository(Protocol):
    def list_shared_services(self) -> tuple[SharedService, ...]:
        """Return every configured shared service."""

    def get_shared_service(self, name: str) -> SharedService | None:
        """Return a configured shared service by name."""
