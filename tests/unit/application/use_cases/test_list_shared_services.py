from __future__ import annotations

from dataclasses import dataclass

from app.application.dto.shared_service_summary import SharedServiceSummary
from app.application.use_cases.list_shared_services import ListSharedServices
from app.domain.entities.shared_service import (
    SharedService,
    SharedServiceAccessMode,
    SharedServiceRoutingStrategy,
    SharedServiceTransport,
)
from app.domain.entities.upstream import Upstream
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
                transport=SharedServiceTransport.HTTP_JSON,
                access_mode=SharedServiceAccessMode.DIRECT_BACKEND_ACCESS,
                provider_managed_availability=True,
                provider="azure_storage",
                account="archive",
                region="westeurope",
                endpoint="https://storage.example.invalid",
                auth=AuthPolicy(
                    mode=AuthMode.MANAGED_IDENTITY,
                    scope="https://storage.azure.com/.default",
                ),
            ),
            SharedService(
                name="transcript_registry",
                transport=SharedServiceTransport.HTTP_JSON,
                access_mode=SharedServiceAccessMode.ROUTER_PROXY,
                provider_managed_availability=True,
                routing_strategy=SharedServiceRoutingStrategy.SINGLE_ENDPOINT,
                max_concurrency=10,
                request_rate_per_second=5,
                upstreams=(
                    Upstream(
                        id="primary",
                        provider="internal_api",
                        account="platform",
                        region="local",
                        tier=0,
                        weight=100,
                        endpoint="https://example.invalid/shared/transcript-registry",
                        auth=AuthPolicy(mode=AuthMode.NONE),
                    ),
                ),
            ),
        )
    )

    summaries = ListSharedServices(repository).execute()

    assert summaries == (
        SharedServiceSummary(
            name="blob_storage",
            transport="http_json",
            access_mode="direct_backend_access",
            routing_strategy=None,
            provider_managed_availability=True,
            router_callable=False,
            upstream_count=0,
            providers=("azure_storage",),
            regions=("westeurope",),
            endpoint="https://storage.example.invalid",
            auth_mode="managed_identity",
        ),
        SharedServiceSummary(
            name="transcript_registry",
            transport="http_json",
            access_mode="router_proxy",
            routing_strategy="single_endpoint",
            provider_managed_availability=True,
            router_callable=True,
            upstream_count=1,
            providers=("internal_api",),
            regions=("local",),
            endpoint="https://example.invalid/shared/transcript-registry",
            auth_mode="none",
        ),
    )
