from __future__ import annotations

from app.application.dto.shared_service_summary import SharedServiceSummary
from app.application.ports.shared_service_repository import SharedServiceRepository


class ListSharedServices:
    def __init__(self, shared_service_repository: SharedServiceRepository) -> None:
        self._shared_service_repository = shared_service_repository

    def execute(self) -> tuple[SharedServiceSummary, ...]:
        shared_services = self._shared_service_repository.list_shared_services()
        return tuple(
            SharedServiceSummary(
                name=shared_service.name,
                transport=shared_service.transport.value,
                access_mode=shared_service.access_mode.value,
                routing_strategy=(
                    shared_service.routing_strategy.value
                    if shared_service.routing_strategy is not None
                    else None
                ),
                provider_managed_availability=shared_service.provider_managed_availability,
                router_callable=shared_service.is_router_callable,
                upstream_count=shared_service.upstream_count,
                providers=shared_service.providers,
                regions=shared_service.regions,
                endpoint=shared_service.primary_endpoint,
                auth_mode=shared_service.auth_mode,
            )
            for shared_service in shared_services
        )
