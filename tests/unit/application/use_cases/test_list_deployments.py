from __future__ import annotations

from dataclasses import dataclass

from app.application.dto.deployment_summary import DeploymentSummary
from app.application.use_cases.list_deployments import ListDeployments
from app.domain.entities.deployment import Deployment
from app.domain.entities.upstream import Upstream
from app.domain.value_objects.auth_policy import AuthMode, AuthPolicy


@dataclass
class FakeDeploymentRepository:
    deployments: tuple[Deployment, ...]

    def list_deployments(self) -> tuple[Deployment, ...]:
        return self.deployments

    def get_deployment(self, deployment_id: str) -> Deployment | None:
        for deployment in self.deployments:
            if deployment.id == deployment_id:
                return deployment
        return None


def build_upstream(region: str) -> Upstream:
    return Upstream(
        id=f"upstream-{region}",
        provider="azure_openai",
        account="aoai-prod-01",
        region=region,
        tier=0,
        weight=100,
        endpoint=f"https://example.com/{region}",
        auth=AuthPolicy(mode=AuthMode.NONE),
    )


def test_list_deployments_returns_summaries() -> None:
    deployment = Deployment(
        id="gpt-4o-chat",
        kind="llm",
        protocol="openai_chat",
        routing_strategy="tiered_failover",
        max_concurrency=50,
        request_rate_per_second=20,
        upstreams=(build_upstream("westeurope"), build_upstream("northeurope")),
    )
    repository = FakeDeploymentRepository(deployments=(deployment,))

    summaries = ListDeployments(repository).execute()

    assert summaries == (
        DeploymentSummary(
            id="gpt-4o-chat",
            kind="llm",
            protocol="openai_chat",
            routing_strategy="tiered_failover",
            upstream_count=2,
            providers=("azure_openai",),
            regions=("northeurope", "westeurope"),
        ),
    )
