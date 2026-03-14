[Repository README](../../README.md) | [docs](../README.md) | [Getting Started](./README.md)

# Implementation Status

Current repository status:

- project bootstrap is in place
- dependency lock and quality tools are configured
- a typed domain and config foundation is implemented
- startup validates YAML config and builds a deployment repository
- proxy paths for chat completions and embeddings are implemented
- outbound auth supports `none`, `api_key`, and `managed_identity`
- tiered multi-upstream selection and request-level failover are implemented
- in-memory health-state persistence, cooldown after `429`, and circuit-open behavior are implemented
- a Redis-backed health-state adapter exists behind the repository port
- deployment-level request-rate limiting and concurrency limiting are implemented
- Redis-backed limiter adapters exist behind application ports
- health endpoints, `GET /deployments`, `POST /v1/chat/completions/{deployment_id}`, and `POST /v1/embeddings/{deployment_id}` are covered by tests
- public documentation and internal delivery documentation are split

Still ahead:

- metrics, traces, and richer decision observability
