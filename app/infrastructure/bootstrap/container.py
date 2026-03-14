from __future__ import annotations

from dataclasses import dataclass

from app.application.deployment_limit_guard import DeploymentLimitGuard
from app.application.ports.concurrency_limiter import ConcurrencyLimiter
from app.application.ports.health_state_repository import HealthStateRepository
from app.application.ports.request_rate_limiter import RequestRateLimiter
from app.application.use_cases.list_deployments import ListDeployments
from app.application.use_cases.route_chat_completion import RouteChatCompletion
from app.application.use_cases.route_embeddings import RouteEmbeddings
from app.domain.services.health_state_policy import HealthStatePolicy
from app.domain.services.tiered_failover_selector import TieredFailoverSelector
from app.domain.services.upstream_failure_classifier import UpstreamFailureClassifier
from app.infrastructure.auth.auth_header_builder import AuthHeaderBuilder
from app.infrastructure.auth.env_secret_provider import EnvSecretProvider
from app.infrastructure.auth.managed_identity_token_provider import ManagedIdentityTokenProvider
from app.infrastructure.config.deployment_repository import ConfigDeploymentRepository
from app.infrastructure.config.models import RouterConfigModel
from app.infrastructure.config.settings import AppSettings
from app.infrastructure.config.yaml_loader import load_router_config
from app.infrastructure.health.in_memory_health_state_repository import (
    InMemoryHealthStateRepository,
)
from app.infrastructure.http.httpx_outbound_invoker import HttpxOutboundInvoker
from app.infrastructure.limits.in_memory_concurrency_limiter import InMemoryConcurrencyLimiter
from app.infrastructure.limits.in_memory_request_rate_limiter import InMemoryRequestRateLimiter


@dataclass(slots=True)
class BootstrapContainer:
    settings: AppSettings
    router_config: RouterConfigModel
    deployment_repository: ConfigDeploymentRepository
    list_deployments_use_case: ListDeployments
    secret_provider: EnvSecretProvider
    token_provider: ManagedIdentityTokenProvider
    health_state_repository: HealthStateRepository
    request_rate_limiter: RequestRateLimiter
    concurrency_limiter: ConcurrencyLimiter
    deployment_limit_guard: DeploymentLimitGuard
    auth_header_builder: AuthHeaderBuilder
    outbound_invoker: HttpxOutboundInvoker
    failure_classifier: UpstreamFailureClassifier
    health_state_policy: HealthStatePolicy
    routing_selector: TieredFailoverSelector
    route_chat_completion_use_case: RouteChatCompletion
    route_embeddings_use_case: RouteEmbeddings


def build_container(settings: AppSettings) -> BootstrapContainer:
    router_config = load_router_config(settings.config_path)
    deployment_repository = ConfigDeploymentRepository.from_router_config(router_config)
    list_deployments_use_case = ListDeployments(deployment_repository=deployment_repository)
    secret_provider = EnvSecretProvider()
    token_provider = ManagedIdentityTokenProvider()
    health_state_repository = InMemoryHealthStateRepository()
    request_rate_limiter = InMemoryRequestRateLimiter()
    concurrency_limiter = InMemoryConcurrencyLimiter()
    deployment_limit_guard = DeploymentLimitGuard(
        request_rate_limiter=request_rate_limiter,
        concurrency_limiter=concurrency_limiter,
    )
    auth_header_builder = AuthHeaderBuilder(
        secret_provider=secret_provider,
        token_provider=token_provider,
    )
    outbound_invoker = HttpxOutboundInvoker()
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
        timeout_ms=router_config.router.timeout_ms,
        max_attempts=router_config.router.max_attempts,
        retryable_status_codes=tuple(router_config.router.retryable_status_codes),
    )
    return BootstrapContainer(
        settings=settings,
        router_config=router_config,
        deployment_repository=deployment_repository,
        list_deployments_use_case=list_deployments_use_case,
        secret_provider=secret_provider,
        token_provider=token_provider,
        health_state_repository=health_state_repository,
        request_rate_limiter=request_rate_limiter,
        concurrency_limiter=concurrency_limiter,
        deployment_limit_guard=deployment_limit_guard,
        auth_header_builder=auth_header_builder,
        outbound_invoker=outbound_invoker,
        failure_classifier=failure_classifier,
        health_state_policy=health_state_policy,
        routing_selector=routing_selector,
        route_chat_completion_use_case=route_chat_completion_use_case,
        route_embeddings_use_case=route_embeddings_use_case,
    )
