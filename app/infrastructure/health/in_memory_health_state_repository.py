from __future__ import annotations

from app.application.ports.health_state_repository import HealthStateRepository
from app.domain.value_objects.health_state import HealthState


class InMemoryHealthStateRepository(HealthStateRepository):
    def __init__(self) -> None:
        self._states: dict[tuple[str, str], HealthState] = {}

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
