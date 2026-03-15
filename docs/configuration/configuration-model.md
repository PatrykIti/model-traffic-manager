[Repository README](../../README.md) | [docs](../README.md) | [Configuration](./README.md)

# Configuration Model

The router uses YAML configuration validated at startup.

The main sections are:

- `router`
- `deployments`
- `shared_services`

The example bootstrap file is [`configs/example.router.yaml`](../../configs/example.router.yaml). It is intentionally small, but it already follows the semantic configuration model described in `_docs/_MVP/`.

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
- shared-service summaries expose the configured service name, endpoint, and auth mode

The current deployment-level `limits` fields are:

- `max_concurrency`
- `request_rate_per_second`

For AKS deployment patterns and the trade-offs between Secret-, env-, and ConfigMap-based delivery, see [../operations/aks-configuration-delivery.md](../operations/aks-configuration-delivery.md).
