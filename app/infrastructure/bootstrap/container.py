from __future__ import annotations

from dataclasses import dataclass

from app.application.use_cases.list_deployments import ListDeployments
from app.infrastructure.config.deployment_repository import ConfigDeploymentRepository
from app.infrastructure.config.models import RouterConfigModel
from app.infrastructure.config.settings import AppSettings
from app.infrastructure.config.yaml_loader import load_router_config


@dataclass(slots=True)
class BootstrapContainer:
    settings: AppSettings
    router_config: RouterConfigModel
    deployment_repository: ConfigDeploymentRepository
    list_deployments_use_case: ListDeployments


def build_container(settings: AppSettings) -> BootstrapContainer:
    router_config = load_router_config(settings.config_path)
    deployment_repository = ConfigDeploymentRepository.from_router_config(router_config)
    list_deployments_use_case = ListDeployments(deployment_repository=deployment_repository)
    return BootstrapContainer(
        settings=settings,
        router_config=router_config,
        deployment_repository=deployment_repository,
        list_deployments_use_case=list_deployments_use_case,
    )
