[Repository README](../../README.md) | [docs](../README.md) | [Configuration](./README.md)

# Configuration Model

The router uses YAML configuration validated at startup.

The main sections are:

- `router`
- `deployments`
- `shared_services`

Available reference configs:

- [`configs/example.router.yaml`](../../configs/example.router.yaml)
  minimal runnable baseline for local startup
- [`configs/full-capabilities.router.yaml`](../../configs/full-capabilities.router.yaml)
  commented full reference that shows the currently supported router contract in one place

Current runtime behavior:

- the config file is read during startup
- YAML is parsed and validated into typed Pydantic models
- invalid config stops application startup
- validated deployments are mapped into domain entities and exposed through the deployment repository
- validated shared services are mapped into domain entities and exposed through the shared-service registry
- deployment `limits` are enforced for request rate and concurrency on the active proxy paths

Supported MVP deployment contracts:

- `kind: llm` with `protocol: openai_chat`
- `kind: embeddings` with `protocol: openai_embeddings`

Current shared-service runtime surface:

- `GET /shared-services` returns the validated shared-service registry
- `POST /v1/shared-services/{service_id}` executes eligible shared services through the router
- shared-service summaries expose execution mode, routing strategy, endpoint visibility, and upstream metadata

Current shared-service execution model:

- `access_mode: direct_backend_access`
  the router stores semantic connection metadata, but the backend calls the service directly
- `access_mode: router_proxy` with `routing_strategy: single_endpoint`
  the router executes one HTTP/JSON downstream call without router-managed failover
- `access_mode: router_proxy` with `routing_strategy: tiered_failover`
  the router reuses the failover model already used for LLM traffic

`provider_managed_availability: true` means the operator expects the service or provider to manage availability semantics outside router-controlled multi-upstream failover.

The current deployment-level `limits` fields are:

- `max_concurrency`
- `request_rate_per_second`

For AKS deployment patterns and the trade-offs between Secret-, env-, and ConfigMap-based delivery, see [../operations/aks-configuration-delivery.md](../operations/aks-configuration-delivery.md).
