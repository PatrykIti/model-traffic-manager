from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from math import gcd

from app.domain.entities.upstream import BalancingPolicy, Upstream
from app.domain.value_objects.health_state import HealthState, HealthStatus
from app.domain.value_objects.route_candidate_rejection import RouteCandidateRejection


@dataclass(frozen=True, slots=True)
class RouteSelection:
    upstream: Upstream
    selected_tier: int
    reason: str
    failover_reason: str | None = None
    rejected_candidates: tuple[RouteCandidateRejection, ...] = ()


class TieredFailoverSelector:
    def __init__(self) -> None:
        self._cursors: dict[tuple[str, int], int] = {}

    def select(
        self,
        deployment_id: str,
        upstreams: tuple[Upstream, ...],
        states: Mapping[str, HealthState] | None = None,
        excluded_upstream_ids: frozenset[str] = frozenset(),
        temporarily_blocked_upstream_ids: frozenset[str] = frozenset(),
    ) -> RouteSelection | None:
        states = states or {}
        active_healthy: list[Upstream] = []
        active_half_open: list[Upstream] = []
        standby_healthy: list[Upstream] = []
        standby_half_open: list[Upstream] = []
        rejected_candidates: list[RouteCandidateRejection] = []

        for upstream in upstreams:
            state = states.get(upstream.id, HealthState())
            if upstream.id in excluded_upstream_ids:
                rejected_candidates.append(self._build_rejection(upstream, "already_attempted"))
                continue
            if upstream.id in temporarily_blocked_upstream_ids:
                rejected_candidates.append(
                    self._build_rejection(upstream, "half_open_probe_in_progress")
                )
                continue
            if upstream.drain:
                rejected_candidates.append(self._build_rejection(upstream, "drain"))
                continue
            if state.status is HealthStatus.HEALTHY:
                if upstream.warm_standby:
                    standby_healthy.append(upstream)
                else:
                    active_healthy.append(upstream)
                continue
            if state.status is HealthStatus.HALF_OPEN:
                if upstream.warm_standby:
                    standby_half_open.append(upstream)
                else:
                    active_half_open.append(upstream)
                continue

            rejected_candidates.append(
                self._build_rejection(upstream, self._reason_for_state(state))
            )

        available = tuple(active_healthy)
        if not available:
            available = tuple(active_half_open)
        if available:
            rejected_candidates.extend(
                self._build_rejection(upstream, "warm_standby_waiting")
                for upstream in (*standby_healthy, *standby_half_open)
            )
        else:
            available = tuple(standby_healthy)
            if not available:
                available = tuple(standby_half_open)

        if active_healthy or active_half_open:
            rejected_candidates.extend(
                self._build_rejection(upstream, "half_open_waiting_probe")
                for upstream in (*active_half_open, *standby_half_open)
            )

        if not available:
            return None

        selected_tier = min(upstream.tier for upstream in available)
        tier_upstreams = tuple(
            upstream for upstream in available if upstream.tier == selected_tier
        )
        policy = tier_upstreams[0].balancing_policy
        if policy is BalancingPolicy.ACTIVE_STANDBY:
            selected_upstream = self._pick_active_standby(tier_upstreams)
        else:
            selected_upstream = self._pick_weighted_round_robin(
                deployment_id=deployment_id,
                tier=selected_tier,
                upstreams=tier_upstreams,
                excluded_upstream_ids=excluded_upstream_ids,
            )
        if selected_upstream is None:
            return None

        return RouteSelection(
            upstream=selected_upstream,
            selected_tier=selected_tier,
            reason=self._build_reason(
                selected_tier=selected_tier,
                excluded_upstream_ids=excluded_upstream_ids,
                selected_state=states.get(selected_upstream.id, HealthState()).status,
            ),
            failover_reason=self._build_failover_reason(
                selected_tier=selected_tier,
                excluded_upstream_ids=excluded_upstream_ids,
                rejected_candidates=tuple(rejected_candidates),
                selected_state=states.get(selected_upstream.id, HealthState()).status,
            ),
            rejected_candidates=tuple(rejected_candidates),
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
            tuple(upstream.effective_weight for upstream in upstreams)
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
    def _pick_active_standby(upstreams: tuple[Upstream, ...]) -> Upstream | None:
        if not upstreams:
            return None
        active = [upstream for upstream in upstreams if not upstream.warm_standby]
        if active:
            return sorted(active, key=lambda upstream: upstream.id)[0]
        return sorted(upstreams, key=lambda upstream: upstream.id)[0]

    @staticmethod
    def _build_reason(
        selected_tier: int,
        excluded_upstream_ids: frozenset[str],
        selected_state: HealthStatus,
    ) -> str:
        if selected_state is HealthStatus.HALF_OPEN:
            return "selected_half_open_probe"
        if not excluded_upstream_ids:
            if selected_tier == 0:
                return "selected_primary_healthy"
            return "selected_failover_tier"

        if selected_tier == 0:
            return "selected_same_tier_retry"
        return "selected_higher_tier_retry"

    @staticmethod
    def _build_failover_reason(
        selected_tier: int,
        excluded_upstream_ids: frozenset[str],
        rejected_candidates: tuple[RouteCandidateRejection, ...],
        selected_state: HealthStatus,
    ) -> str | None:
        if selected_state is HealthStatus.HALF_OPEN:
            return "circuit_recovery_probe"
        if excluded_upstream_ids:
            return "previous_attempt_failed"
        if selected_tier == 0:
            return None

        lower_tier_reasons = {
            rejected.reason
            for rejected in rejected_candidates
            if rejected.tier < selected_tier and rejected.reason != "already_attempted"
        }
        if not lower_tier_reasons:
            return None
        if len(lower_tier_reasons) == 1:
            return f"lower_tier_{next(iter(lower_tier_reasons))}"
        return "lower_tier_mixed_rejections"

    @staticmethod
    def _reason_for_state(state: HealthState) -> str:
        if state.status is HealthStatus.COOLDOWN:
            if state.last_failure_reason is not None:
                return f"cooldown_{state.last_failure_reason.value}"
            return "cooldown"
        return {
            HealthStatus.RATE_LIMITED: "rate_limited",
            HealthStatus.QUOTA_EXHAUSTED: "quota_exhausted",
            HealthStatus.UNHEALTHY: "unhealthy",
            HealthStatus.CIRCUIT_OPEN: "circuit_open",
            HealthStatus.HALF_OPEN: "half_open",
            HealthStatus.HEALTHY: "healthy",
        }[state.status]

    @staticmethod
    def _build_rejection(upstream: Upstream, reason: str) -> RouteCandidateRejection:
        return RouteCandidateRejection(
            upstream_id=upstream.id,
            provider=upstream.provider,
            account=upstream.account,
            region=upstream.region,
            tier=upstream.tier,
            reason=reason,
        )
