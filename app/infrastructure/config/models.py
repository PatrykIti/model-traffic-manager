from __future__ import annotations

from typing import Annotated, Literal

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field, model_validator

from app.domain.entities.deployment import Deployment, DeploymentKind, DeploymentProtocol
from app.domain.entities.shared_service import (
    SharedService,
    SharedServiceAccessMode,
    SharedServiceRoutingStrategy,
    SharedServiceTransport,
)
from app.domain.entities.upstream import BalancingPolicy, CapacityMode, Upstream
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
    inbound_auth: InboundAuthConfigModel | None = None


class RoutingConfigModel(BaseModel):
    strategy: Literal["tiered_failover"]


class LimitsConfigModel(BaseModel):
    max_concurrency: int = Field(gt=0)
    request_rate_per_second: int = Field(gt=0)


class ApiBearerTokenConfigModel(BaseModel):
    kind: Literal["api_bearer_token"]
    token_id: str = Field(min_length=1)
    display_name: str | None = Field(default=None, min_length=1)
    consumer_role: str | None = Field(default=None, min_length=1)
    secret_ref: str = Field(min_length=1)


class EntraApplicationConfigModel(BaseModel):
    client_app_id: str = Field(min_length=1)
    display_name: str | None = Field(default=None, min_length=1)
    consumer_role: str | None = Field(default=None, min_length=1)
    required_app_roles: list[str] = Field(min_length=1)


class EntraIdInboundAuthConfigModel(BaseModel):
    kind: Literal["entra_id"]
    tenant_id: str = Field(min_length=1)
    audiences: list[str] = Field(min_length=1)
    authority_host: str = "https://login.microsoftonline.com"
    applications: list[EntraApplicationConfigModel] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_unique_client_apps(self) -> EntraIdInboundAuthConfigModel:
        client_app_ids = [application.client_app_id for application in self.applications]
        if len(client_app_ids) != len(set(client_app_ids)):
            raise ValueError(
                "entra_id applications must not contain duplicate client_app_id values"
            )
        return self


InboundAuthProviderConfigModel = Annotated[
    ApiBearerTokenConfigModel | EntraIdInboundAuthConfigModel,
    Field(discriminator="kind"),
]


class InboundAuthConfigModel(BaseModel):
    providers: list[InboundAuthProviderConfigModel] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_provider_mix(self) -> InboundAuthConfigModel:
        entra_provider_count = sum(
            1
            for provider in self.providers
            if isinstance(provider, EntraIdInboundAuthConfigModel)
        )
        if entra_provider_count > 1:
            raise ValueError("inbound_auth must not define more than one entra_id provider")
        return self


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
    model_name: str | None = None
    model_version: str | None = None
    deployment_name: str | None = None
    capacity_mode: CapacityMode | None = None
    compatibility_group: str | None = None
    balancing_policy: BalancingPolicy = BalancingPolicy.WEIGHTED_ROUND_ROBIN
    warm_standby: bool = False
    drain: bool = False
    target_share_percent: int | None = Field(default=None, gt=0, le=100)
    max_share_percent: int | None = Field(default=None, gt=0, le=100)

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
            model_name=self.model_name,
            model_version=self.model_version,
            deployment_name=self.deployment_name,
            capacity_mode=self.capacity_mode,
            compatibility_group=self.compatibility_group,
            balancing_policy=self.balancing_policy,
            warm_standby=self.warm_standby,
            drain=self.drain,
            target_share_percent=self.target_share_percent,
            max_share_percent=self.max_share_percent,
        )


class DeploymentConfigModel(BaseModel):
    id: str = Field(min_length=1)
    kind: DeploymentKind
    protocol: DeploymentProtocol
    consumer_role: str | None = Field(default=None, min_length=1)
    routing: RoutingConfigModel
    limits: LimitsConfigModel
    upstreams: list[UpstreamConfigModel] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_unique_upstream_ids(self) -> DeploymentConfigModel:
        upstream_ids = [upstream.id for upstream in self.upstreams]
        if len(upstream_ids) != len(set(upstream_ids)):
            raise ValueError(f"deployment '{self.id}' contains duplicate upstream IDs")
        tier_groups = {
            tier: [upstream for upstream in self.upstreams if upstream.tier == tier]
            for tier in {upstream.tier for upstream in self.upstreams}
        }
        for tier, upstreams in tier_groups.items():
            if len(upstreams) <= 1:
                continue
            groups = {
                upstream.compatibility_group
                for upstream in upstreams
                if upstream.compatibility_group is not None
            }
            if len(groups) > 1:
                raise ValueError(
                    f"deployment '{self.id}' tier '{tier}' must not mix multiple "
                    "compatibility_group values"
                )
            policies = {upstream.balancing_policy for upstream in upstreams}
            if len(policies) != 1:
                raise ValueError(
                    f"deployment '{self.id}' tier '{tier}' must use one balancing_policy"
                )
            if self.protocol is DeploymentProtocol.OPENAI_EMBEDDINGS:
                model_names = {upstream.model_name for upstream in upstreams}
                model_versions = {upstream.model_version for upstream in upstreams}
                if (
                    None in model_names
                    or None in model_versions
                    or len(model_names) != 1
                    or len(model_versions) != 1
                ):
                    raise ValueError(
                        f"deployment '{self.id}' tier '{tier}' must keep embeddings "
                        "pools on one model_name/model_version"
                    )
            else:
                model_names = {
                    upstream.model_name
                    for upstream in upstreams
                    if upstream.model_name is not None
                }
                model_versions = {
                    upstream.model_version
                    for upstream in upstreams
                    if upstream.model_version is not None
                }
                if len(model_names) > 1 or len(model_versions) > 1:
                    raise ValueError(
                        f"deployment '{self.id}' tier '{tier}' must not mix different "
                        "model_name/model_version values"
                    )
            if next(iter(policies)) is BalancingPolicy.ACTIVE_STANDBY:
                active_upstreams = [
                    upstream
                    for upstream in upstreams
                    if not upstream.warm_standby and not upstream.drain
                ]
                if len(active_upstreams) > 1:
                    raise ValueError(
                        f"deployment '{self.id}' tier '{tier}' active_standby pool "
                        "must have at most one active upstream"
                    )
            share_defined = [
                upstream
                for upstream in upstreams
                if (
                    not upstream.warm_standby
                    and not upstream.drain
                    and upstream.target_share_percent is not None
                )
            ]
            active_non_drain = [
                upstream
                for upstream in upstreams
                if not upstream.warm_standby and not upstream.drain
            ]
            if share_defined and len(share_defined) != len(active_non_drain):
                raise ValueError(
                    f"deployment '{self.id}' tier '{tier}' must define "
                    "target_share_percent on every active upstream or on none"
                )
            if (
                share_defined
                and sum(upstream.target_share_percent or 0 for upstream in share_defined) != 100
            ):
                raise ValueError(
                    f"deployment '{self.id}' tier '{tier}' target_share_percent "
                    "values must sum to 100"
                )
            effective_share_denominator = sum(
                upstream.target_share_percent or upstream.weight
                for upstream in active_non_drain
            )
            for upstream in active_non_drain:
                if upstream.max_share_percent is None:
                    continue
                effective_share_percent = (
                    (upstream.target_share_percent or upstream.weight)
                    / effective_share_denominator
                ) * 100
                if effective_share_percent > upstream.max_share_percent:
                    raise ValueError(
                        f"deployment '{self.id}' tier '{tier}' upstream '{upstream.id}' "
                        "would exceed max_share_percent under the configured distribution"
                    )
        return self

    def to_domain(self) -> Deployment:
        return Deployment(
            id=self.id,
            kind=self.kind,
            protocol=self.protocol,
            routing_strategy=self.routing.strategy,
            max_concurrency=self.limits.max_concurrency,
            request_rate_per_second=self.limits.request_rate_per_second,
            consumer_role=self.consumer_role,
            upstreams=tuple(upstream.to_domain() for upstream in self.upstreams),
        )


class SharedServiceConfigModel(BaseModel):
    transport: SharedServiceTransport = SharedServiceTransport.HTTP_JSON
    access_mode: SharedServiceAccessMode
    provider_managed_availability: bool = False
    consumer_role: str | None = Field(default=None, min_length=1)
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
            consumer_role=self.consumer_role,
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
