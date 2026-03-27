from __future__ import annotations

import pytest

from app.domain.entities.upstream import CapacityMode, Upstream
from app.domain.errors import DomainInvariantError
from app.domain.value_objects.auth_policy import AuthMode, AuthPolicy


def test_upstream_accepts_valid_data() -> None:
    upstream = Upstream(
        id="primary",
        provider="azure_openai",
        account="aoai-prod-01",
        region="westeurope",
        tier=0,
        weight=100,
        endpoint="https://example.com/upstream",
        auth=AuthPolicy(mode=AuthMode.NONE),
        capacity_mode="ptu",
    )

    assert upstream.id == "primary"
    assert upstream.tier == 0
    assert upstream.capacity_mode is CapacityMode.PTU


def test_upstream_exposes_target_share_as_effective_weight() -> None:
    upstream = Upstream(
        id="primary",
        provider="azure_openai",
        account="aoai-prod-01",
        region="westeurope",
        tier=0,
        weight=100,
        endpoint="https://example.com/upstream",
        auth=AuthPolicy(mode=AuthMode.NONE),
        target_share_percent=40,
    )

    assert upstream.effective_weight == 40


def test_upstream_rejects_invalid_share_targets() -> None:
    with pytest.raises(DomainInvariantError):
        Upstream(
            id="primary",
            provider="azure_openai",
            account="aoai-prod-01",
            region="westeurope",
            tier=0,
            weight=100,
            endpoint="https://example.com/upstream",
            auth=AuthPolicy(mode=AuthMode.NONE),
            target_share_percent=60,
            max_share_percent=50,
        )


@pytest.mark.parametrize(
    ("tier", "weight"),
    [
        (-1, 100),
        (0, 0),
    ],
)
def test_upstream_rejects_invalid_tier_or_weight(tier: int, weight: int) -> None:
    with pytest.raises(DomainInvariantError):
        Upstream(
            id="primary",
            provider="azure_openai",
            account="aoai-prod-01",
            region="westeurope",
            tier=tier,
            weight=weight,
            endpoint="https://example.com/upstream",
            auth=AuthPolicy(mode=AuthMode.NONE),
        )
