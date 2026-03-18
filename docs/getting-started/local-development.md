[Repository README](../../README.md) | [docs](../README.md) | [Getting Started](./README.md)

# Local Development

Use the canonical local command path:

```text
make bootstrap
make check
make run
```

What each command does:

- `make bootstrap` syncs the locked environment with `uv`
- `make check` runs lint, type-check, and tests
- `make release-check` runs the local quality gate plus shell, workflow, and Terraform validation
- `make integration-azure-local` runs `apply -> integration tests -> destroy` against Azure using the active Azure CLI context
- `make integration-azure-chat-local` runs `apply -> direct chat provider probe -> destroy` against Azure OpenAI using repository auth and outbound adapters
- `make integration-azure-embeddings-local` runs `apply -> direct embeddings provider probe -> destroy` against Azure OpenAI using repository auth and outbound adapters
- `make e2e-aks-local` runs `apply -> deploy -> e2e smoke -> destroy` against AKS using the active Azure CLI context
- `make e2e-aks-live-model-local` runs a wider AKS suite with Azure OpenAI infrastructure and a real model-response validation
- `make e2e-aks-live-embeddings-local` runs a dedicated AKS suite for real embeddings responses through the router
- `make e2e-aks-live-load-balancing-local` runs a dedicated AKS suite for model-aware load-balancing behavior
- `make e2e-aks-live-shared-services-local` runs a dedicated AKS suite for shared-service execution modes
- `make e2e-aks-redis-local` runs a dedicated AKS suite for Redis-backed multi-replica runtime-state behavior
- `make run` starts the bootstrap FastAPI app

All `make` targets that execute `pytest` now use verbose reporting, so the console shows each test name as it runs and prints a full final status summary.

The live Azure OpenAI validation scopes generate randomized account and subdomain suffixes by default so repeated local runs do not collide with recently deleted Cognitive Services custom subdomains.

Environment defaults are documented in [`.env.example`](../../.env.example).

Config references:

- [`configs/example.router.yaml`](../../configs/example.router.yaml)
  minimal bootstrap config for quick local startup
- [`configs/full-capabilities.router.yaml`](../../configs/full-capabilities.router.yaml)
  full commented reference for the complete currently supported config contract

Useful first endpoints after startup:

- `GET /health/live`
- `GET /health/ready`
- `GET /deployments`
- `GET /shared-services`
- `POST /v1/shared-services/{service_id}`
- `POST /v1/chat/completions/{deployment_id}`
- `POST /v1/embeddings/{deployment_id}`

If you test the `api_key` path locally, expose secret material through environment variables referenced by `env://...` secret refs.

If you test the `managed_identity` path locally, rely on the Azure credential chain available to the router process. The default repository config still uses `none`, so local startup does not require Azure auth by default.

If you want to exercise shared runtime state locally, set:

- `MODEL_TRAFFIC_MANAGER_RUNTIME_STATE_BACKEND=redis`
- `MODEL_TRAFFIC_MANAGER_REDIS_URL=redis://...`
- optional `MODEL_TRAFFIC_MANAGER_REDIS_KEY_PREFIX=router`

For higher-level local Azure-backed runs:

- the active Azure subscription is resolved from `az account show`
- Terraform inputs come from the shared baseline under `infra/_shared/env/`
- `destroy` is attempted under shell traps even when the selected higher-level suite fails
- the default profile is `ENVIRONMENT=dev1`
- `integration-azure-chat-local` and `integration-azure-embeddings-local` are intentionally separate so chat and embeddings provider probes can be exercised independently

Live-model notes:

- `make e2e-aks-local` stays the cheaper AKS smoke path without a real model account
- `make e2e-aks-live-model-local` provisions extra Azure OpenAI infrastructure and consumes real model quota
- `make e2e-aks-live-embeddings-local` provisions a dedicated Azure OpenAI embeddings deployment and validates live vectors through AKS
- `make e2e-aks-live-load-balancing-local` provisions a dedicated AKS validation scope and verifies active-active / active-standby balancing against live in-cluster mocks
- `make e2e-aks-live-shared-services-local` provisions a dedicated AKS validation scope and verifies direct-access plus router-proxy shared-service behavior
- `make e2e-aks-redis-local` provisions a dedicated AKS validation scope and verifies shared cooldown, circuit, request-rate, and concurrency behavior across router replicas
- the current live-model profile targets `swedencentral` and validates `gpt-5` plus `gpt-5.1`
- the current live-model suite also exercises router failover against an in-cluster mock primary for rate-limit and unhealthy scenarios
- the current live embeddings profile targets `germanywestcentral` and validates `text-embedding-3-small`
- the current live load-balancing profile validates same-tier chat and embeddings distribution plus active-standby behavior
- this suite is intentionally separate because model quota and regional model availability can change independently of the smoke AKS path
- the next meaningful higher-level addition is the final workflow rollout for the expanded live matrix
