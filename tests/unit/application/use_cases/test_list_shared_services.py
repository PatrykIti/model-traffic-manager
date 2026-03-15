from __future__ import annotations

from dataclasses import dataclass

from app.application.dto.shared_service_summary import SharedServiceSummary
from app.application.use_cases.list_shared_services import ListSharedServices
from app.domain.entities.shared_service import SharedService
from app.domain.value_objects.auth_policy import AuthMode, AuthPolicy


@dataclass
class FakeSharedServiceRepository:
    shared_services: tuple[SharedService, ...]

    def list_shared_services(self) -> tuple[SharedService, ...]:
        return self.shared_services

    def get_shared_service(self, name: str) -> SharedService | None:
        for shared_service in self.shared_services:
            if shared_service.name == name:
                return shared_service
        return None


def test_list_shared_services_returns_summaries() -> None:
    repository = FakeSharedServiceRepository(
        shared_services=(
            SharedService(
                name="blob_storage",
                endpoint="https://storage.example.invalid",
                auth=AuthPolicy(
                    mode=AuthMode.MANAGED_IDENTITY,
                    scope="https://storage.azure.com/.default",
                ),
            ),
        )
    )

    summaries = ListSharedServices(repository).execute()

    assert summaries == (
        SharedServiceSummary(
            name="blob_storage",
            endpoint="https://storage.example.invalid",
            auth_mode="managed_identity",
        ),
    )
