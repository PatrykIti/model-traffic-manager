from __future__ import annotations

from typing import Protocol

from app.domain.value_objects.auth_policy import AuthPolicy


class AuthHeaderBuilderPort(Protocol):
    def build(self, auth_policy: AuthPolicy) -> dict[str, str]:
        """Build outbound auth headers for the given auth policy."""
