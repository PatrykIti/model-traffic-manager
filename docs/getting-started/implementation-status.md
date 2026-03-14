[Repository README](../../README.md) | [docs](../README.md) | [Getting Started](./README.md)

# Implementation Status

Current repository status:

- project bootstrap is in place
- dependency lock and quality tools are configured
- a typed domain and config foundation is implemented
- startup validates YAML config and builds a deployment repository
- proxy paths for chat completions and embeddings are implemented
- health endpoints, `GET /deployments`, `POST /v1/chat/completions/{deployment_id}`, and `POST /v1/embeddings/{deployment_id}` are covered by tests
- public documentation and internal delivery documentation are split

Still ahead:

- routing policies
- health/failover state management
- `managed_identity`
- multi-upstream failover
