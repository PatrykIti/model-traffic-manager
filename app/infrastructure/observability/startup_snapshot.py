from __future__ import annotations

from typing import Any

from opentelemetry import trace

from app.infrastructure.bootstrap.container import BootstrapContainer
from app.infrastructure.observability.logging import get_logger
from app.infrastructure.observability.telemetry import ObservabilityRuntime


def emit_startup_topology_snapshot(
    container: BootstrapContainer,
    observability: ObservabilityRuntime,
) -> dict[str, Any]:
    snapshot = build_startup_topology_snapshot(container, observability)
    get_logger(__name__).info("router_topology_snapshot", **snapshot)
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("router_startup") as span:
        span.set_attribute("router.instance_name", snapshot["router_instance_name"])
        span.set_attribute("router.deployment_count", len(snapshot["deployments"]))
        span.set_attribute("router.shared_service_count", len(snapshot["shared_services"]))
        span.set_attribute("router.observability_backend", snapshot["observability_backend"])
        span.set_attribute("router.trace_export_enabled", snapshot["trace_export_enabled"])
        span.set_attribute("router.log_export_enabled", snapshot["log_export_enabled"])
    return snapshot


def build_startup_topology_snapshot(
    container: BootstrapContainer,
    observability: ObservabilityRuntime,
) -> dict[str, Any]:
    router_config = container.router_config
    return {
        "router_instance_name": router_config.router.instance_name,
        "runtime_state_backend": container.settings.runtime_state_backend,
        "observability_backend": observability.backend,
        "trace_export_enabled": observability.trace_export_enabled,
        "log_export_enabled": observability.log_export_enabled,
        "deployments": [
            {
                "id": deployment.id,
                "kind": deployment.kind.value,
                "protocol": deployment.protocol.value,
                "consumer_role": deployment.consumer_role,
                "upstreams": [
                    {
                        "id": upstream.id,
                        "provider": upstream.provider,
                        "account": upstream.account,
                        "region": upstream.region,
                        "tier": upstream.tier,
                        "model_name": upstream.model_name,
                        "model_version": upstream.model_version,
                        "deployment_name": upstream.deployment_name,
                        "capacity_mode": (
                            upstream.capacity_mode.value
                            if upstream.capacity_mode is not None
                            else None
                        ),
                        "balancing_policy": upstream.balancing_policy.value,
                        "warm_standby": upstream.warm_standby,
                        "drain": upstream.drain,
                    }
                    for upstream in deployment.upstreams
                ],
            }
            for deployment in router_config.deployments
        ],
        "shared_services": [
            {
                "id": name,
                "access_mode": shared_service.access_mode.value,
                "consumer_role": shared_service.consumer_role,
                "transport": shared_service.transport.value,
                "routing_strategy": (
                    shared_service.routing_strategy.value
                    if shared_service.routing_strategy is not None
                    else None
                ),
                "provider_managed_availability": shared_service.provider_managed_availability,
                "upstreams": [
                    {
                        "id": upstream.id,
                        "provider": upstream.provider,
                        "account": upstream.account,
                        "region": upstream.region,
                        "tier": upstream.tier,
                    }
                    for upstream in shared_service.upstreams
                ],
            }
            for name, shared_service in sorted(router_config.shared_services.items())
        ],
    }
