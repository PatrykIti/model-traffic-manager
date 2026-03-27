from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, cast

from redis import Redis

from app.application.deployment_limit_guard import DeploymentLimitGuard
from app.application.ports.concurrency_limiter import ConcurrencyLimiter
from app.application.ports.health_state_repository import HealthStateRepository
from app.application.ports.request_rate_limiter import RequestRateLimiter
from app.application.ports.runtime_event_recorder import RuntimeEventRecorder
from app.application.use_cases.list_deployments import ListDeployments
from app.application.use_cases.list_shared_services import ListSharedServices
from app.application.use_cases.route_chat_completion import RouteChatCompletion
from app.application.use_cases.route_embeddings import RouteEmbeddings
from app.application.use_cases.route_shared_service import RouteSharedService
from app.domain.services.health_state_policy import HealthStatePolicy
from app.domain.services.tiered_failover_selector import TieredFailoverSelector
from app.domain.services.upstream_failure_classifier import UpstreamFailureClassifier
from app.infrastructure.auth.auth_header_builder import AuthHeaderBuilder
from app.infrastructure.auth.env_secret_provider import EnvSecretProvider
from app.infrastructure.auth.inbound_auth import InboundAuthenticator
from app.infrastructure.auth.managed_identity_token_provider import ManagedIdentityTokenProvider
from app.infrastructure.config.deployment_repository import ConfigDeploymentRepository
from app.infrastructure.config.models import RouterConfigModel
from app.infrastructure.config.settings import AppSettings
from app.infrastructure.config.shared_service_repository import ConfigSharedServiceRepository
from app.infrastructure.config.yaml_loader import load_router_config
from app.infrastructure.health.in_memory_health_state_repository import (
    InMemoryHealthStateRepository,
)
from app.infrastructure.health.redis_health_state_repository import RedisHealthStateRepository
from app.infrastructure.http.httpx_outbound_invoker import HttpxOutboundInvoker
from app.infrastructure.limits.in_memory_concurrency_limiter import InMemoryConcurrencyLimiter
from app.infrastructure.limits.in_memory_request_rate_limiter import InMemoryRequestRateLimiter
from app.infrastructure.limits.redis_concurrency_limiter import RedisConcurrencyLimiter
from app.infrastructure.limits.redis_request_rate_limiter import RedisRequestRateLimiter
from app.infrastructure.observability.runtime_event_recorder import StructuredRuntimeEventRecorder


class RuntimeRedisClient(Protocol):
    def get(self, key: str) -> str | bytes | None:
        """Return the stored payload for a key."""

    def set(
        self,
        key: str,
        value: str,
        *,
        nx: bool = False,
        ex: int | None = None,
    ) -> bool | None:
        """Persist a string payload."""

    def delete(self, key: str) -> int:
        """Delete a key."""

    def close(self) -> None:
        """Close the client."""


@dataclass(slots=True)
class BootstrapContainer:
    settings: AppSettings
    router_config: RouterConfigModel
    redis_client: RuntimeRedisClient | None
    deployment_repository: ConfigDeploymentRepository
    list_deployments_use_case: ListDeployments
    shared_service_repository: ConfigSharedServiceRepository
    list_shared_services_use_case: ListSharedServices
    secret_provider: EnvSecretProvider
    inbound_authenticator: InboundAuthenticator
    token_provider: ManagedIdentityTokenProvider
    health_state_repository: HealthStateRepository
    request_rate_limiter: RequestRateLimiter
    concurrency_limiter: ConcurrencyLimiter
    deployment_limit_guard: DeploymentLimitGuard
    runtime_event_recorder: RuntimeEventRecorder
    auth_header_builder: AuthHeaderBuilder
    outbound_invoker: HttpxOutboundInvoker
    failure_classifier: UpstreamFailureClassifier
    health_state_policy: HealthStatePolicy
    routing_selector: TieredFailoverSelector
    route_chat_completion_use_case: RouteChatCompletion
    route_embeddings_use_case: RouteEmbeddings
    route_shared_service_use_case: RouteSharedService


def build_container(settings: AppSettings) -> BootstrapContainer:
    router_config = load_router_config(settings.config_path)
    redis_client = _build_redis_client(settings)
    deployment_repository = ConfigDeploymentRepository.from_router_config(router_config)
    shared_service_repository = ConfigSharedServiceRepository.from_router_config(router_config)
    list_deployments_use_case = ListDeployments(deployment_repository=deployment_repository)
    list_shared_services_use_case = ListSharedServices(
        shared_service_repository=shared_service_repository
    )
    secret_provider = EnvSecretProvider()
    inbound_authenticator = InboundAuthenticator.from_config(
        router_config.router.inbound_auth,
        secret_provider=secret_provider,
    )
    token_provider = ManagedIdentityTokenProvider()
    health_state_repository = _build_health_state_repository(settings, redis_client)
    request_rate_limiter = _build_request_rate_limiter(settings, redis_client)
    concurrency_limiter = _build_concurrency_limiter(settings, redis_client)
    runtime_event_recorder = StructuredRuntimeEventRecorder()
    deployment_limit_guard = DeploymentLimitGuard(
        request_rate_limiter=request_rate_limiter,
        concurrency_limiter=concurrency_limiter,
        runtime_event_recorder=runtime_event_recorder,
    )
    auth_header_builder = AuthHeaderBuilder(
        secret_provider=secret_provider,
        token_provider=token_provider,
    )
    outbound_invoker = HttpxOutboundInvoker(
        connect_timeout_ms=settings.outbound_connect_timeout_ms,
        write_timeout_ms=settings.outbound_write_timeout_ms,
        pool_timeout_ms=settings.outbound_pool_timeout_ms,
        max_connections=settings.outbound_max_connections,
        max_keepalive_connections=settings.outbound_max_keepalive_connections,
    )
    failure_classifier = UpstreamFailureClassifier()
    health_state_policy = HealthStatePolicy(
        failure_threshold=router_config.router.health.failure_threshold,
        cooldown_seconds=router_config.router.health.cooldown_seconds,
        half_open_after_seconds=router_config.router.health.half_open_after_seconds,
    )
    routing_selector = TieredFailoverSelector()
    route_chat_completion_use_case = RouteChatCompletion(
        deployment_repository=deployment_repository,
        auth_header_builder=auth_header_builder,
        outbound_invoker=outbound_invoker,
        deployment_limit_guard=deployment_limit_guard,
        health_state_repository=health_state_repository,
        failure_classifier=failure_classifier,
        health_state_policy=health_state_policy,
        routing_selector=routing_selector,
        runtime_event_recorder=runtime_event_recorder,
        timeout_ms=router_config.router.timeout_ms,
        max_attempts=router_config.router.max_attempts,
        retryable_status_codes=tuple(router_config.router.retryable_status_codes),
    )
    route_embeddings_use_case = RouteEmbeddings(
        deployment_repository=deployment_repository,
        auth_header_builder=auth_header_builder,
        outbound_invoker=outbound_invoker,
        deployment_limit_guard=deployment_limit_guard,
        health_state_repository=health_state_repository,
        failure_classifier=failure_classifier,
        health_state_policy=health_state_policy,
        routing_selector=routing_selector,
        runtime_event_recorder=runtime_event_recorder,
        timeout_ms=router_config.router.timeout_ms,
        max_attempts=router_config.router.max_attempts,
        retryable_status_codes=tuple(router_config.router.retryable_status_codes),
    )
    route_shared_service_use_case = RouteSharedService(
        shared_service_repository=shared_service_repository,
        auth_header_builder=auth_header_builder,
        outbound_invoker=outbound_invoker,
        deployment_limit_guard=deployment_limit_guard,
        health_state_repository=health_state_repository,
        failure_classifier=failure_classifier,
        health_state_policy=health_state_policy,
        routing_selector=routing_selector,
        runtime_event_recorder=runtime_event_recorder,
        timeout_ms=router_config.router.timeout_ms,
        max_attempts=router_config.router.max_attempts,
        retryable_status_codes=tuple(router_config.router.retryable_status_codes),
    )
    return BootstrapContainer(
        settings=settings,
        router_config=router_config,
        redis_client=redis_client,
        deployment_repository=deployment_repository,
        list_deployments_use_case=list_deployments_use_case,
        shared_service_repository=shared_service_repository,
        list_shared_services_use_case=list_shared_services_use_case,
        secret_provider=secret_provider,
        inbound_authenticator=inbound_authenticator,
        token_provider=token_provider,
        health_state_repository=health_state_repository,
        request_rate_limiter=request_rate_limiter,
        concurrency_limiter=concurrency_limiter,
        deployment_limit_guard=deployment_limit_guard,
        runtime_event_recorder=runtime_event_recorder,
        auth_header_builder=auth_header_builder,
        outbound_invoker=outbound_invoker,
        failure_classifier=failure_classifier,
        health_state_policy=health_state_policy,
        routing_selector=routing_selector,
        route_chat_completion_use_case=route_chat_completion_use_case,
        route_embeddings_use_case=route_embeddings_use_case,
        route_shared_service_use_case=route_shared_service_use_case,
    )


def _build_redis_client(settings: AppSettings) -> RuntimeRedisClient | None:
    if settings.runtime_state_backend != "redis":
        return None
    return cast(
        RuntimeRedisClient,
        Redis.from_url(settings.redis_url or "", decode_responses=True),
    )


def _build_health_state_repository(
    settings: AppSettings,
    redis_client: RuntimeRedisClient | None,
) -> HealthStateRepository:
    if settings.runtime_state_backend == "redis" and redis_client is not None:
        return RedisHealthStateRepository(
            redis_client=redis_client,
            key_prefix=f"{settings.redis_key_prefix}:health",
            probe_key_prefix=f"{settings.redis_key_prefix}:half-open-probe",
        )
    return InMemoryHealthStateRepository()


def _build_request_rate_limiter(
    settings: AppSettings,
    redis_client: RuntimeRedisClient | None,
) -> RequestRateLimiter:
    if settings.runtime_state_backend == "redis" and redis_client is not None:
        return RedisRequestRateLimiter(
            redis_client=redis_client,
            key_prefix=f"{settings.redis_key_prefix}:rate-limit",
        )
    return InMemoryRequestRateLimiter()


def _build_concurrency_limiter(
    settings: AppSettings,
    redis_client: RuntimeRedisClient | None,
) -> ConcurrencyLimiter:
    if settings.runtime_state_backend == "redis" and redis_client is not None:
        return RedisConcurrencyLimiter(
            redis_client=redis_client,
            key_prefix=f"{settings.redis_key_prefix}:concurrency",
        )
    return InMemoryConcurrencyLimiter()
