from __future__ import annotations

from app.application.dto.deployment_summary import DeploymentSummary
from app.application.ports.deployment_repository import DeploymentRepository


class ListDeployments:
    def __init__(self, deployment_repository: DeploymentRepository) -> None:
        self._deployment_repository = deployment_repository

    def execute(self) -> tuple[DeploymentSummary, ...]:
        deployments = self._deployment_repository.list_deployments()
        return tuple(
            DeploymentSummary(
                id=deployment.id,
                kind=deployment.kind.value,
                protocol=deployment.protocol.value,
                routing_strategy=deployment.routing_strategy,
                upstream_count=deployment.upstream_count,
                providers=deployment.providers,
                regions=deployment.regions,
            )
            for deployment in deployments
        )
