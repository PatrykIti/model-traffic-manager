[Repository README](../../README.md) | [docs](../README.md) | [Getting Started](./README.md)

# Implementation Status

Current repository status:

- project bootstrap is in place
- dependency lock and quality tools are configured
- a typed domain and config foundation is implemented
- startup validates YAML config and builds a deployment repository
- the first proxy path for chat completions is implemented
- health endpoints, `GET /deployments`, and `POST /v1/chat/completions/{deployment_id}` are covered by tests
- public documentation and internal delivery documentation are split

Still ahead:

- routing policies
- health/failover state management
- `managed_identity`
- embeddings
- multi-upstream failover
