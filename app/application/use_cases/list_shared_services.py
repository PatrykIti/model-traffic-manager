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
                endpoint=shared_service.endpoint,
                auth_mode=shared_service.auth.mode.value,
            )
            for shared_service in shared_services
        )
