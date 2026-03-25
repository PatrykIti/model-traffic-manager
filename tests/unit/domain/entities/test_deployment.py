from __future__ import annotations

import pytest

from app.domain.entities.deployment import Deployment
from app.domain.entities.upstream import Upstream
from app.domain.errors import DomainInvariantError
from app.domain.value_objects.auth_policy import AuthMode, AuthPolicy


def build_upstream(*, provider: str = "azure_openai", region: str = "westeurope") -> Upstream:
    return Upstream(
        id=f"{provider}-{region}",
        provider=provider,
        account="account-01",
        region=region,
        tier=0,
        weight=100,
        endpoint=f"https://example.com/{provider}/{region}",
        auth=AuthPolicy(mode=AuthMode.NONE),
    )


def test_deployment_exposes_provider_and_region_summaries() -> None:
    deployment = Deployment(
        id="gpt-4o-chat",
        kind="llm",
        protocol="openai_chat",
        consumer_role="chatbot-api",
        routing_strategy="tiered_failover",
        max_concurrency=10,
        request_rate_per_second=5,
        upstreams=(
            build_upstream(provider="azure_openai", region="westeurope"),
            build_upstream(provider="azure_openai", region="northeurope"),
            build_upstream(provider="internal_mock", region="local"),
        ),
    )

    assert deployment.upstream_count == 3
    assert deployment.consumer_role == "chatbot-api"
    assert deployment.providers == ("azure_openai", "internal_mock")
    assert deployment.regions == ("local", "northeurope", "westeurope")


def test_deployment_requires_at_least_one_upstream() -> None:
    with pytest.raises(DomainInvariantError):
        Deployment(
            id="gpt-4o-chat",
            kind="llm",
            protocol="openai_chat",
            routing_strategy="tiered_failover",
            max_concurrency=10,
            request_rate_per_second=5,
            upstreams=(),
        )
