[Repository README](../../README.md) | [docs](../README.md) | [Configuration](./README.md)

# Deployments and Upstreams

The router treats deployments and upstreams as explicit domain concepts.

Each deployment is expected to describe:

- its logical identifier
- protocol and kind
- routing settings
- limits
- upstream definitions

Each upstream should expose:

- `id`
- `provider`
- `account`
- `region`
- `tier`
- `weight`
- `endpoint`
- `auth`

Current validation rules already enforced by the application:

- deployment IDs must be unique
- upstream IDs must be unique inside a deployment
- only MVP deployment contracts are accepted:
  `llm` with `openai_chat`, or `embeddings` with `openai_embeddings`
- `managed_identity` requires `scope`
- `api_key` requires `header_name` and `secret_ref`
- `tier` must be greater than or equal to zero
- `weight` must be greater than zero

Current API surface:

- `GET /deployments` returns the validated deployment registry as deployment summaries
- `GET /shared-services` returns the validated shared-service registry
- `POST /v1/chat/completions/{deployment_id}` proxies to the selected upstream for the deployment
- `POST /v1/embeddings/{deployment_id}` proxies to the selected upstream for the deployment
- `POST /v1/shared-services/{service_id}` executes eligible shared services for backend callers

Request-path guardrails:

- chat completions requests fail with `409` if the deployment does not support the chat contract
- embeddings requests fail with `409` if the deployment does not support the embeddings contract

Current outbound auth support:

- `none`
- `api_key` with `secret_ref` resolved through `env://ENV_VAR_NAME`
- `managed_identity` with in-memory token caching keyed by `(auth_mode, client_id, scope)`

Managed Identity remains an outbound router concern. It does not imply forwarding client bearer tokens to upstreams.

Shared-service notes:

- `direct_backend_access` services are metadata-only from the router perspective; execution through the router is rejected
- `single_endpoint` shared services are executed through one configured upstream without router-managed failover
- `tiered_failover` shared services reuse the upstream health and failover model
- provider-managed availability and router-managed tiered failover are intentionally distinct concerns
