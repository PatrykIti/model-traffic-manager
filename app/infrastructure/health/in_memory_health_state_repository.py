from __future__ import annotations

import time

from app.application.ports.health_state_repository import HealthStateRepository
from app.domain.value_objects.health_state import HealthState, HealthStatus


class InMemoryHealthStateRepository(HealthStateRepository):
    def __init__(self) -> None:
        self._states: dict[tuple[str, str], HealthState] = {}
        self._half_open_probes: dict[tuple[str, str], int] = {}

    def get_states(
        self,
        deployment_id: str,
        upstream_ids: tuple[str, ...],
    ) -> dict[str, HealthState]:
        states: dict[str, HealthState] = {}
        for upstream_id in upstream_ids:
            state = self._states.get((deployment_id, upstream_id))
            if state is not None:
                states[upstream_id] = state
        return states

    def set_state(self, deployment_id: str, upstream_id: str, state: HealthState) -> None:
        self._states[(deployment_id, upstream_id)] = state
        if state.status is not HealthStatus.HALF_OPEN:
            self.clear_half_open_probe(deployment_id, upstream_id)

    def try_acquire_half_open_probe(
        self,
        deployment_id: str,
        upstream_id: str,
        probe_ttl_seconds: int,
    ) -> bool:
        key = (deployment_id, upstream_id)
        now = int(time.time())
        expires_at = self._half_open_probes.get(key)
        if expires_at is not None and expires_at > now:
            return False
        self._half_open_probes[key] = now + probe_ttl_seconds
        return True

    def clear_half_open_probe(self, deployment_id: str, upstream_id: str) -> None:
        self._half_open_probes.pop((deployment_id, upstream_id), None)
