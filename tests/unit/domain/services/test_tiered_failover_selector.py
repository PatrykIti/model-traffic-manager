from __future__ import annotations

from app.domain.entities.upstream import Upstream
from app.domain.services.tiered_failover_selector import TieredFailoverSelector
from app.domain.value_objects.auth_policy import AuthMode, AuthPolicy
from app.domain.value_objects.health_state import HealthState, HealthStatus


def build_upstream(upstream_id: str, *, tier: int, weight: int) -> Upstream:
    return Upstream(
        id=upstream_id,
        provider="azure_openai",
        account="aoai-prod-01",
        region="westeurope",
        tier=tier,
        weight=weight,
        endpoint=f"https://example.invalid/{upstream_id}",
        auth=AuthPolicy(mode=AuthMode.NONE),
    )


def test_selector_picks_lowest_available_tier() -> None:
    selector = TieredFailoverSelector()
    upstreams = (
        build_upstream("tier-1", tier=1, weight=100),
        build_upstream("tier-0", tier=0, weight=100),
    )

    selection = selector.select("deployment-a", upstreams)

    assert selection is not None
    assert selection.upstream.id == "tier-0"
    assert selection.selected_tier == 0
    assert selection.reason == "selected_primary_healthy"


def test_selector_uses_weighted_round_robin_within_tier() -> None:
    selector = TieredFailoverSelector()
    upstreams = (
        build_upstream("primary-a", tier=0, weight=200),
        build_upstream("primary-b", tier=0, weight=100),
    )

    first = selector.select("deployment-a", upstreams)
    second = selector.select("deployment-a", upstreams)
    third = selector.select("deployment-a", upstreams)

    assert first is not None
    assert second is not None
    assert third is not None
    assert [first.upstream.id, second.upstream.id, third.upstream.id] == [
        "primary-a",
        "primary-b",
        "primary-a",
    ]


def test_selector_moves_to_next_candidate_when_excluded() -> None:
    selector = TieredFailoverSelector()
    upstreams = (
        build_upstream("primary-a", tier=0, weight=100),
        build_upstream("primary-b", tier=0, weight=100),
        build_upstream("secondary-a", tier=1, weight=100),
    )

    initial = selector.select("deployment-a", upstreams)
    retry = selector.select(
        "deployment-a",
        upstreams,
        excluded_upstream_ids=frozenset({"primary-a"}),
    )
    higher_tier = selector.select(
        "deployment-a",
        upstreams,
        excluded_upstream_ids=frozenset({"primary-a", "primary-b"}),
    )

    assert initial is not None
    assert retry is not None
    assert higher_tier is not None
    assert initial.upstream.id == "primary-a"
    assert retry.upstream.id == "primary-b"
    assert retry.reason == "selected_same_tier_retry"
    assert retry.failover_reason == "previous_attempt_failed"
    assert higher_tier.upstream.id == "secondary-a"
    assert higher_tier.reason == "selected_higher_tier_retry"
    assert higher_tier.failover_reason == "previous_attempt_failed"


def test_selector_skips_unavailable_primary_tier_states() -> None:
    selector = TieredFailoverSelector()
    upstreams = (
        build_upstream("primary-a", tier=0, weight=100),
        build_upstream("secondary-a", tier=1, weight=100),
    )

    selection = selector.select(
        "deployment-a",
        upstreams,
        states={"primary-a": HealthState(status=HealthStatus.CIRCUIT_OPEN)},
    )

    assert selection is not None
    assert selection.upstream.id == "secondary-a"
    assert selection.selected_tier == 1
    assert selection.reason == "selected_failover_tier"
    assert selection.failover_reason == "lower_tier_circuit_open"
    assert selection.rejected_candidates[0].reason == "circuit_open"


def test_selector_prefers_healthy_candidates_over_half_open_candidates() -> None:
    selector = TieredFailoverSelector()
    upstreams = (
        build_upstream("primary-healthy", tier=0, weight=100),
        build_upstream("primary-half-open", tier=0, weight=100),
    )

    selection = selector.select(
        "deployment-a",
        upstreams,
        states={"primary-half-open": HealthState(status=HealthStatus.HALF_OPEN)},
    )

    assert selection is not None
    assert selection.upstream.id == "primary-healthy"
    assert selection.rejected_candidates[0].reason == "half_open_waiting_probe"


def test_selector_marks_temporarily_blocked_half_open_candidates() -> None:
    selector = TieredFailoverSelector()
    upstreams = (build_upstream("primary-half-open", tier=0, weight=100),)

    selection = selector.select(
        "deployment-a",
        upstreams,
        states={"primary-half-open": HealthState(status=HealthStatus.HALF_OPEN)},
        temporarily_blocked_upstream_ids=frozenset({"primary-half-open"}),
    )

    assert selection is None
