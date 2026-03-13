from __future__ import annotations

from app.domain.entities.deployment import Deployment
from app.infrastructure.config.models import RouterConfigModel


class ConfigDeploymentRepository:
    def __init__(self, deployments: tuple[Deployment, ...]) -> None:
        self._deployments = deployments
        self._deployment_index = {deployment.id: deployment for deployment in deployments}

    @classmethod
    def from_router_config(cls, router_config: RouterConfigModel) -> ConfigDeploymentRepository:
        return cls(deployments=router_config.to_domain_deployments())

    def list_deployments(self) -> tuple[Deployment, ...]:
        return self._deployments

    def get_deployment(self, deployment_id: str) -> Deployment | None:
        return self._deployment_index.get(deployment_id)
