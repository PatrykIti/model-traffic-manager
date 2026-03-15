from __future__ import annotations

from app.domain.entities.shared_service import SharedService
from app.infrastructure.config.models import RouterConfigModel


class ConfigSharedServiceRepository:
    def __init__(self, shared_services: tuple[SharedService, ...]) -> None:
        self._shared_services = shared_services
        self._shared_service_index = {
            shared_service.name: shared_service for shared_service in shared_services
        }

    @classmethod
    def from_router_config(cls, router_config: RouterConfigModel) -> ConfigSharedServiceRepository:
        return cls(shared_services=router_config.to_domain_shared_services())

    def list_shared_services(self) -> tuple[SharedService, ...]:
        return self._shared_services

    def get_shared_service(self, name: str) -> SharedService | None:
        return self._shared_service_index.get(name)
