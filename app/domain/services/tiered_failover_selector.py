from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from math import gcd

from app.domain.entities.upstream import Upstream
from app.domain.value_objects.health_state import HealthState


@dataclass(frozen=True, slots=True)
class RouteSelection:
    upstream: Upstream
    selected_tier: int
    reason: str


class TieredFailoverSelector:
    def __init__(self) -> None:
        self._cursors: dict[tuple[str, int], int] = {}

    def select(
        self,
        deployment_id: str,
        upstreams: tuple[Upstream, ...],
        states: Mapping[str, HealthState] | None = None,
        excluded_upstream_ids: frozenset[str] = frozenset(),
    ) -> RouteSelection | None:
        states = states or {}
        available = tuple(
            upstream
            for upstream in upstreams
            if upstream.id not in excluded_upstream_ids
            and states.get(upstream.id, HealthState()).is_available()
        )
        if not available:
            return None

        selected_tier = min(upstream.tier for upstream in available)
        tier_upstreams = tuple(
            upstream for upstream in available if upstream.tier == selected_tier
        )
        upstream = self._pick_weighted_round_robin(
            deployment_id=deployment_id,
            tier=selected_tier,
            upstreams=tier_upstreams,
            excluded_upstream_ids=excluded_upstream_ids,
        )
        if upstream is None:
            return None

        return RouteSelection(
            upstream=upstream,
            selected_tier=selected_tier,
            reason=self._build_reason(selected_tier, excluded_upstream_ids),
        )

    def _pick_weighted_round_robin(
        self,
        deployment_id: str,
        tier: int,
        upstreams: tuple[Upstream, ...],
        excluded_upstream_ids: frozenset[str],
    ) -> Upstream | None:
        if not upstreams:
            return None

        key = (deployment_id, tier)
        cycle = self._build_cycle(upstreams)
        upstream_index = {upstream.id: upstream for upstream in upstreams}
        start = self._cursors.get(key, 0)

        for offset in range(len(cycle)):
            index = (start + offset) % len(cycle)
            upstream_id = cycle[index]
            if upstream_id in excluded_upstream_ids:
                continue
            self._cursors[key] = (index + 1) % len(cycle)
            return upstream_index[upstream_id]

        return None

    @staticmethod
    def _build_cycle(upstreams: tuple[Upstream, ...]) -> tuple[str, ...]:
        if len(upstreams) == 1:
            return (upstreams[0].id,)

        normalized_weights = TieredFailoverSelector._normalize_weights(
            tuple(upstream.weight for upstream in upstreams)
        )
        current_weights = [0] * len(upstreams)
        total_weight = sum(normalized_weights)
        sequence: list[str] = []

        for _ in range(total_weight):
            for index, weight in enumerate(normalized_weights):
                current_weights[index] += weight

            selected_index = max(range(len(upstreams)), key=current_weights.__getitem__)
            current_weights[selected_index] -= total_weight
            sequence.append(upstreams[selected_index].id)

        return tuple(sequence)

    @staticmethod
    def _normalize_weights(weights: tuple[int, ...]) -> tuple[int, ...]:
        common_divisor = weights[0]
        for weight in weights[1:]:
            common_divisor = gcd(common_divisor, weight)
        return tuple(weight // common_divisor for weight in weights)

    @staticmethod
    def _build_reason(selected_tier: int, excluded_upstream_ids: frozenset[str]) -> str:
        if not excluded_upstream_ids:
            if selected_tier == 0:
                return "selected_primary_weighted_round_robin"
            return "selected_failover_tier_weighted_round_robin"

        if selected_tier == 0:
            return "selected_same_tier_retry_candidate"
        return "selected_higher_tier_retry_candidate"
