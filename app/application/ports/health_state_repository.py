from __future__ import annotations

from typing import Protocol

from app.domain.value_objects.health_state import HealthState


class HealthStateRepository(Protocol):
    def get_states(
        self,
        deployment_id: str,
        upstream_ids: tuple[str, ...],
    ) -> dict[str, HealthState]:
        """Return the stored health state for the given deployment upstreams."""

    def set_state(self, deployment_id: str, upstream_id: str, state: HealthState) -> None:
        """Persist the current health state for a deployment upstream."""
