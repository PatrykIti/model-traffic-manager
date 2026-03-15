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

    def try_acquire_half_open_probe(
        self,
        deployment_id: str,
        upstream_id: str,
        probe_ttl_seconds: int,
    ) -> bool:
        """Reserve the single half-open probe slot for an upstream when available."""

    def clear_half_open_probe(self, deployment_id: str, upstream_id: str) -> None:
        """Release any half-open probe reservation for an upstream."""
