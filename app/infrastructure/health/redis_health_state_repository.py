from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Protocol

from app.application.ports.health_state_repository import HealthStateRepository
from app.domain.value_objects.failure_classification import FailureReason
from app.domain.value_objects.health_state import HealthState, HealthStatus


class RedisLike(Protocol):
    def get(self, key: str) -> str | bytes | None:
        """Return the stored payload for a key."""

    def set(
        self,
        key: str,
        value: str,
        *,
        nx: bool = False,
        ex: int | None = None,
    ) -> bool | None:
        """Persist the payload for a key."""

    def delete(self, key: str) -> int:
        """Delete a stored key."""


class RedisHealthStateRepository(HealthStateRepository):
    def __init__(
        self,
        redis_client: RedisLike,
        key_prefix: str = "router:health",
        probe_key_prefix: str = "router:half-open-probe",
    ) -> None:
        self._redis_client = redis_client
        self._key_prefix = key_prefix
        self._probe_key_prefix = probe_key_prefix

    def get_states(
        self,
        deployment_id: str,
        upstream_ids: tuple[str, ...],
    ) -> dict[str, HealthState]:
        states: dict[str, HealthState] = {}
        for upstream_id in upstream_ids:
            payload = self._redis_client.get(self._build_key(deployment_id, upstream_id))
            if payload is None:
                continue
            states[upstream_id] = self._deserialize(payload)
        return states

    def set_state(self, deployment_id: str, upstream_id: str, state: HealthState) -> None:
        self._redis_client.set(
            self._build_key(deployment_id, upstream_id),
            self._serialize(state),
        )
        if state.status is not HealthStatus.HALF_OPEN:
            self.clear_half_open_probe(deployment_id, upstream_id)

    def try_acquire_half_open_probe(
        self,
        deployment_id: str,
        upstream_id: str,
        probe_ttl_seconds: int,
    ) -> bool:
        return bool(
            self._redis_client.set(
                self._build_probe_key(deployment_id, upstream_id),
                "1",
                nx=True,
                ex=probe_ttl_seconds,
            )
        )

    def clear_half_open_probe(self, deployment_id: str, upstream_id: str) -> None:
        self._redis_client.delete(self._build_probe_key(deployment_id, upstream_id))

    def _build_key(self, deployment_id: str, upstream_id: str) -> str:
        return f"{self._key_prefix}:{deployment_id}:{upstream_id}"

    def _build_probe_key(self, deployment_id: str, upstream_id: str) -> str:
        return f"{self._probe_key_prefix}:{deployment_id}:{upstream_id}"

    @staticmethod
    def _serialize(state: HealthState) -> str:
        payload = {
            "status": state.status.value,
            "consecutive_failures": state.consecutive_failures,
            "cooldown_until": state.cooldown_until,
            "circuit_open_until": state.circuit_open_until,
            "last_failure_reason": (
                state.last_failure_reason.value if state.last_failure_reason is not None else None
            ),
        }
        return json.dumps(payload, separators=(",", ":"))

    @staticmethod
    def _deserialize(payload: str | bytes) -> HealthState:
        if isinstance(payload, bytes):
            payload = payload.decode("utf-8")

        data = json.loads(payload)
        return HealthState(
            status=HealthStatus(data["status"]),
            consecutive_failures=int(data["consecutive_failures"]),
            cooldown_until=_optional_int(data, "cooldown_until"),
            circuit_open_until=_optional_int(data, "circuit_open_until"),
            last_failure_reason=(
                FailureReason(data["last_failure_reason"])
                if data.get("last_failure_reason") is not None
                else None
            ),
        )


def _optional_int(payload: Mapping[str, object], key: str) -> int | None:
    value = payload.get(key)
    if value is None:
        return None
    if isinstance(value, (int, str)):
        return int(value)
    raise TypeError(f"Field '{key}' must be serialized as an integer-compatible value.")
