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

Optional load-balancing metadata for same-tier pools:

- `model_name`
- `model_version`
- `deployment_name`
- `compatibility_group`
- `balancing_policy`
- `warm_standby`
- `drain`
- `target_share_percent`
- `max_share_percent`

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

For identity-selection examples and mixed auth-mode configurations, see [auth-and-identity.md](./auth-and-identity.md).

Shared-service notes:

- `direct_backend_access` services are metadata-only from the router perspective; execution through the router is rejected
- `single_endpoint` shared services are executed through one configured upstream without router-managed failover
- `tiered_failover` shared services reuse the upstream health and failover model
- provider-managed availability and router-managed tiered failover are intentionally distinct concerns

## Full Example Files

Ready-to-copy example router configs:

- [deployments-chat-regional-failover.router.yaml](../../configs/examples/deployments-chat-regional-failover.router.yaml)
- [deployments-chat-model-fallback.router.yaml](../../configs/examples/deployments-chat-model-fallback.router.yaml)
- [deployments-embeddings-regional-failover.router.yaml](../../configs/examples/deployments-embeddings-regional-failover.router.yaml)

These files show the full router config shape, not only the `deployments` fragment.

What each example demonstrates:

- `deployments-chat-regional-failover.router.yaml`
  same chat capability across several Azure regions with explicit tiered regional failover
- `deployments-chat-model-fallback.router.yaml`
  one logical chat deployment that falls back across different model variants across tiers
- `deployments-embeddings-regional-failover.router.yaml`
  embeddings routing with the same tiered regional failover pattern used for chat traffic

For compatibility-aware same-tier balancing and commented active-active examples, see [load-balancing.md](./load-balancing.md).
