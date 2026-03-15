from __future__ import annotations

from typing import Literal

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field, model_validator

from app.domain.entities.deployment import Deployment, DeploymentKind, DeploymentProtocol
from app.domain.entities.shared_service import (
    SharedService,
    SharedServiceAccessMode,
    SharedServiceRoutingStrategy,
    SharedServiceTransport,
)
from app.domain.entities.upstream import Upstream
from app.domain.errors import ConfigValidationError
from app.domain.value_objects.auth_policy import AuthMode, AuthPolicy


class RouterHealthConfigModel(BaseModel):
    failure_threshold: int = Field(gt=0)
    cooldown_seconds: int = Field(ge=0)
    half_open_after_seconds: int = Field(ge=0)


class RouterRuntimeConfigModel(BaseModel):
    instance_name: str = Field(min_length=1)
    timeout_ms: int = Field(gt=0)
    max_attempts: int = Field(gt=0)
    retryable_status_codes: list[int]
    health: RouterHealthConfigModel


class RoutingConfigModel(BaseModel):
    strategy: Literal["tiered_failover"]


class LimitsConfigModel(BaseModel):
    max_concurrency: int = Field(gt=0)
    request_rate_per_second: int = Field(gt=0)


class AuthConfigModel(BaseModel):
    mode: AuthMode
    scope: str | None = None
    client_id: str | None = None
    header_name: str | None = None
    secret_ref: str | None = None

    model_config = ConfigDict(use_enum_values=False)

    @model_validator(mode="after")
    def validate_auth(self) -> AuthConfigModel:
        if self.mode is AuthMode.MANAGED_IDENTITY and not self.scope:
            raise ValueError("managed_identity auth requires 'scope'")

        if self.mode is AuthMode.API_KEY and (not self.header_name or not self.secret_ref):
            raise ValueError("api_key auth requires both 'header_name' and 'secret_ref'")

        if self.mode is AuthMode.NONE and any(
            value is not None
            for value in (self.scope, self.client_id, self.header_name, self.secret_ref)
        ):
            raise ValueError("auth mode 'none' must not define extra auth fields")

        return self

    def to_domain(self) -> AuthPolicy:
        return AuthPolicy(
            mode=self.mode,
            scope=self.scope,
            client_id=self.client_id,
            header_name=self.header_name,
            secret_ref=self.secret_ref,
        )


class UpstreamConfigModel(BaseModel):
    id: str = Field(min_length=1)
    provider: str = Field(min_length=1)
    account: str = Field(min_length=1)
    region: str = Field(min_length=1)
    tier: int = Field(ge=0)
    weight: int = Field(gt=0)
    endpoint: AnyHttpUrl
    auth: AuthConfigModel

    def to_domain(self) -> Upstream:
        return Upstream(
            id=self.id,
            provider=self.provider,
            account=self.account,
            region=self.region,
            tier=self.tier,
            weight=self.weight,
            endpoint=str(self.endpoint),
            auth=self.auth.to_domain(),
        )


class DeploymentConfigModel(BaseModel):
    id: str = Field(min_length=1)
    kind: DeploymentKind
    protocol: DeploymentProtocol
    routing: RoutingConfigModel
    limits: LimitsConfigModel
    upstreams: list[UpstreamConfigModel] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_unique_upstream_ids(self) -> DeploymentConfigModel:
        upstream_ids = [upstream.id for upstream in self.upstreams]
        if len(upstream_ids) != len(set(upstream_ids)):
            raise ValueError(f"deployment '{self.id}' contains duplicate upstream IDs")
        return self

    def to_domain(self) -> Deployment:
        return Deployment(
            id=self.id,
            kind=self.kind,
            protocol=self.protocol,
            routing_strategy=self.routing.strategy,
            max_concurrency=self.limits.max_concurrency,
            request_rate_per_second=self.limits.request_rate_per_second,
            upstreams=tuple(upstream.to_domain() for upstream in self.upstreams),
        )


class SharedServiceConfigModel(BaseModel):
    transport: SharedServiceTransport = SharedServiceTransport.HTTP_JSON
    access_mode: SharedServiceAccessMode
    provider_managed_availability: bool = False
    routing_strategy: SharedServiceRoutingStrategy | None = None
    provider: str | None = None
    account: str | None = None
    region: str | None = None
    endpoint: AnyHttpUrl | None = None
    auth: AuthConfigModel | None = None
    limits: LimitsConfigModel | None = None
    upstreams: list[UpstreamConfigModel] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_shared_service(self) -> SharedServiceConfigModel:
        if self.access_mode is SharedServiceAccessMode.DIRECT_BACKEND_ACCESS:
            if self.routing_strategy is not None:
                raise ValueError(
                    "direct_backend_access shared services must not define routing_strategy"
                )
            if self.limits is not None:
                raise ValueError("direct_backend_access shared services must not define limits")
            if self.upstreams:
                raise ValueError(
                    "direct_backend_access shared services must not define upstreams"
                )
            if self.endpoint is None or self.auth is None:
                raise ValueError(
                    "direct_backend_access shared services must define endpoint and auth"
                )
            if not self.provider or not self.account or not self.region:
                raise ValueError(
                    "direct_backend_access shared services must define "
                    "provider, account, and region"
                )
            return self

        if self.routing_strategy is None:
            raise ValueError("router_proxy shared services must define routing_strategy")
        if self.limits is None:
            raise ValueError("router_proxy shared services must define limits")
        if not self.upstreams:
            raise ValueError("router_proxy shared services must define upstreams")
        if self.endpoint is not None or self.auth is not None:
            raise ValueError(
                "router_proxy shared services must not define top-level endpoint or auth"
            )

        upstream_ids = [upstream.id for upstream in self.upstreams]
        if len(upstream_ids) != len(set(upstream_ids)):
            raise ValueError("router_proxy shared services contain duplicate upstream IDs")
        if (
            self.routing_strategy is SharedServiceRoutingStrategy.SINGLE_ENDPOINT
            and len(self.upstreams) != 1
        ):
            raise ValueError(
                "shared services with routing_strategy=single_endpoint must define one upstream"
            )
        if (
            self.routing_strategy is SharedServiceRoutingStrategy.TIERED_FAILOVER
            and self.provider_managed_availability
        ):
            raise ValueError(
                "provider_managed_availability cannot be combined with "
                "routing_strategy=tiered_failover"
            )
        return self

    def to_domain(self, name: str) -> SharedService:
        return SharedService(
            name=name,
            transport=self.transport,
            access_mode=self.access_mode,
            provider_managed_availability=self.provider_managed_availability,
            routing_strategy=self.routing_strategy,
            provider=self.provider,
            account=self.account,
            region=self.region,
            endpoint=(str(self.endpoint) if self.endpoint is not None else None),
            auth=(self.auth.to_domain() if self.auth is not None else None),
            max_concurrency=(self.limits.max_concurrency if self.limits is not None else None),
            request_rate_per_second=(
                self.limits.request_rate_per_second if self.limits is not None else None
            ),
            upstreams=tuple(upstream.to_domain() for upstream in self.upstreams),
        )


class RouterConfigModel(BaseModel):
    router: RouterRuntimeConfigModel
    deployments: list[DeploymentConfigModel]
    shared_services: dict[str, SharedServiceConfigModel] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_unique_deployment_ids(self) -> RouterConfigModel:
        deployment_ids = [deployment.id for deployment in self.deployments]
        if len(deployment_ids) != len(set(deployment_ids)):
            raise ValueError("router config contains duplicate deployment IDs")
        return self

    def to_domain_deployments(self) -> tuple[Deployment, ...]:
        return tuple(deployment.to_domain() for deployment in self.deployments)

    def to_domain_shared_services(self) -> tuple[SharedService, ...]:
        return tuple(
            shared_service.to_domain(name)
            for name, shared_service in sorted(self.shared_services.items())
        )


def validate_router_config(raw_config: object) -> RouterConfigModel:
    try:
        return RouterConfigModel.model_validate(raw_config)
    except Exception as exc:  # pragma: no cover - wrapped for domain-facing error surface
        raise ConfigValidationError(f"Invalid router configuration: {exc}") from exc
