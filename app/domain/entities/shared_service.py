from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from app.domain.entities.upstream import Upstream
from app.domain.errors import DomainInvariantError
from app.domain.value_objects.auth_policy import AuthPolicy


class SharedServiceTransport(StrEnum):
    HTTP_JSON = "http_json"


class SharedServiceAccessMode(StrEnum):
    DIRECT_BACKEND_ACCESS = "direct_backend_access"
    ROUTER_PROXY = "router_proxy"


class SharedServiceRoutingStrategy(StrEnum):
    SINGLE_ENDPOINT = "single_endpoint"
    TIERED_FAILOVER = "tiered_failover"


@dataclass(frozen=True, slots=True)
class SharedService:
    name: str
    transport: SharedServiceTransport
    access_mode: SharedServiceAccessMode
    provider_managed_availability: bool
    consumer_role: str | None = None
    routing_strategy: SharedServiceRoutingStrategy | None = None
    endpoint: str | None = None
    auth: AuthPolicy | None = None
    provider: str | None = None
    account: str | None = None
    region: str | None = None
    max_concurrency: int | None = None
    request_rate_per_second: int | None = None
    upstreams: tuple[Upstream, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "transport", SharedServiceTransport(self.transport))
        object.__setattr__(self, "access_mode", SharedServiceAccessMode(self.access_mode))
        if self.routing_strategy is not None:
            object.__setattr__(
                self,
                "routing_strategy",
                SharedServiceRoutingStrategy(self.routing_strategy),
            )
        if not self.name:
            raise DomainInvariantError("Shared-service name must not be empty.")
        if self.consumer_role is not None and not self.consumer_role:
            raise DomainInvariantError("Shared-service consumer_role must not be empty.")
        if self.access_mode is SharedServiceAccessMode.DIRECT_BACKEND_ACCESS:
            if not self.endpoint:
                raise DomainInvariantError(
                    "Direct-access shared services must define an endpoint."
                )
            if self.auth is None:
                raise DomainInvariantError("Direct-access shared services must define auth.")
            if not self.provider or not self.account or not self.region:
                raise DomainInvariantError(
                    "Direct-access shared services must define provider, account, and region."
                )
            if self.upstreams:
                raise DomainInvariantError(
                    "Direct-access shared services must not define router upstreams."
                )
            if self.routing_strategy is not None:
                raise DomainInvariantError(
                    "Direct-access shared services must not define a routing strategy."
                )
            if self.max_concurrency is not None or self.request_rate_per_second is not None:
                raise DomainInvariantError(
                    "Direct-access shared services must not define router proxy limits."
                )
            return

        if not self.upstreams:
            raise DomainInvariantError("Router-proxy shared services must define upstreams.")
        if self.endpoint is not None or self.auth is not None:
            raise DomainInvariantError(
                "Router-proxy shared services must define endpoint and auth through upstreams."
            )
        if self.max_concurrency is None or self.max_concurrency <= 0:
            raise DomainInvariantError(
                "Router-proxy shared services must define a positive max_concurrency."
            )
        if self.request_rate_per_second is None or self.request_rate_per_second <= 0:
            raise DomainInvariantError(
                "Router-proxy shared services must define a positive request_rate_per_second."
            )
        if self.routing_strategy is None:
            raise DomainInvariantError(
                "Router-proxy shared services must define a routing strategy."
            )
        if (
            self.routing_strategy is SharedServiceRoutingStrategy.SINGLE_ENDPOINT
            and len(self.upstreams) != 1
        ):
            raise DomainInvariantError(
                "Shared services with routing strategy 'single_endpoint' "
                "must define exactly one upstream."
            )
        if (
            self.routing_strategy is SharedServiceRoutingStrategy.TIERED_FAILOVER
            and self.provider_managed_availability
        ):
            raise DomainInvariantError(
                "Provider-managed availability cannot be combined with tiered_failover."
            )

    @property
    def is_router_callable(self) -> bool:
        return self.access_mode is SharedServiceAccessMode.ROUTER_PROXY

    @property
    def id(self) -> str:
        return self.name

    @property
    def uses_failover(self) -> bool:
        return self.routing_strategy is SharedServiceRoutingStrategy.TIERED_FAILOVER

    @property
    def upstream_count(self) -> int:
        return len(self.upstreams)

    @property
    def primary_upstream(self) -> Upstream:
        if not self.upstreams:
            raise DomainInvariantError("Shared service does not define any upstreams.")
        return self.upstreams[0]

    @property
    def providers(self) -> tuple[str, ...]:
        if self.upstreams:
            return tuple(sorted({upstream.provider for upstream in self.upstreams}))
        if self.provider is None:
            return ()
        return (self.provider,)

    @property
    def regions(self) -> tuple[str, ...]:
        if self.upstreams:
            return tuple(sorted({upstream.region for upstream in self.upstreams}))
        if self.region is None:
            return ()
        return (self.region,)

    @property
    def primary_endpoint(self) -> str | None:
        if self.upstreams:
            return self.upstreams[0].endpoint
        return self.endpoint

    @property
    def auth_mode(self) -> str | None:
        if self.upstreams:
            return self.upstreams[0].auth.mode.value
        if self.auth is None:
            return None
        return self.auth.mode.value
