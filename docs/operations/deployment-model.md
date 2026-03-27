[Repository README](../../README.md) | [docs](../README.md) | [Operations](./README.md)

# Deployment Model

The current repository supports:

- local execution through `make run`
- quality validation through `make check`
- container build through `make docker-build`

Current outbound auth posture:

- `managed_identity` is the preferred secretless mode for Azure-native upstreams
- `api_key` remains available as a fallback where needed
- Managed Identity tokens are cached in-memory per router instance

Current runtime-state deployment options:

- `MODEL_TRAFFIC_MANAGER_RUNTIME_STATE_BACKEND=in_memory` keeps health and limiter state local to one process
- `MODEL_TRAFFIC_MANAGER_RUNTIME_STATE_BACKEND=redis` activates shared health and limiter coordination across instances
- `MODEL_TRAFFIC_MANAGER_REDIS_URL` configures the Redis connection string for shared runtime state
- `MODEL_TRAFFIC_MANAGER_REDIS_KEY_PREFIX` scopes Redis keys used by the router

Shared-service deployment options:

- `direct_backend_access` keeps the router as a semantic registry while the backend talks to the service directly
- `router_proxy` with `single_endpoint` keeps auth and observability in the router without adding router-managed failover
- `router_proxy` with `tiered_failover` is reserved for shared HTTP services that genuinely need explicit multi-upstream failover

Operational default:

- do not assume that every shared service should inherit the LLM routing model
- services with provider-managed availability, especially storage-style workloads, should not automatically become router-failover targets

As implementation grows further, this section should expand into AKS deployment guidance, workload identity expectations, and production runtime operations.

For AKS-specific configuration delivery options, see [aks-configuration-delivery.md](./aks-configuration-delivery.md).
