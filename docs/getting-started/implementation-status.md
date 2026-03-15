[Repository README](../../README.md) | [docs](../README.md) | [Getting Started](./README.md)

# Implementation Status

Current repository status:

- project bootstrap is in place
- dependency lock and quality tools are configured
- a typed domain and config foundation is implemented
- startup validates YAML config and builds deployment and shared-service registries
- proxy paths for chat completions and embeddings are implemented
- only MVP deployment contracts are accepted at startup: `llm` with `openai_chat` and `embeddings` with `openai_embeddings`
- chat and embeddings routes reject incompatible deployment contracts explicitly at request time
- outbound auth supports `none`, `api_key`, and `managed_identity`
- tiered multi-upstream selection and request-level failover are implemented
- cooldown after `429`, quota classification, circuit-open behavior, and half-open recovery probes are implemented
- in-memory and Redis-backed health-state persistence are both wired into the active runtime
- deployment-level request-rate limiting and concurrency limiting are implemented
- Redis-backed limiter adapters are available in the active runtime when `runtime_state_backend=redis`
- request correlation, structured runtime events, `/metrics`, and trace foundations are implemented
- routing events record rejected candidates and explicit failover reasons
- `GET /shared-services` exposes the configured shared-service registry
- `POST /v1/shared-services/{service_id}` executes router-proxy shared services while direct-backend-access services remain metadata-only
- opt-in `integration-azure` and `e2e-aks` workflows plus repo-local higher-level test artifacts are implemented
- outbound HTTP connection-pool tuning and explicit timeout policy are implemented
- `make release-check` validates the current release gate locally
- health endpoints, `GET /deployments`, `GET /shared-services`, `POST /v1/chat/completions/{deployment_id}`, `POST /v1/embeddings/{deployment_id}`, and `POST /v1/shared-services/{service_id}` are covered by tests
- public documentation and internal delivery documentation are split
