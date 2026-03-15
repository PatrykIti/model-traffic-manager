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
- `make integration-azure-local` runs `apply -> integration tests -> destroy` against Azure using the active Azure CLI context
- `make e2e-aks-local` runs `apply -> deploy -> e2e smoke -> destroy` against AKS using the active Azure CLI context
- `make e2e-aks-live-model-local` runs a wider AKS suite with Azure OpenAI infrastructure and a real model-response validation
- `make run` starts the bootstrap FastAPI app

Environment defaults are documented in [`.env.example`](../../.env.example), and the example runtime config lives in [`configs/example.router.yaml`](../../configs/example.router.yaml).

Useful first endpoints after startup:

- `GET /health/live`
- `GET /health/ready`
- `GET /deployments`
- `GET /shared-services`
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

Live-model notes:

- `make e2e-aks-local` stays the cheaper AKS smoke path without a real model account
- `make e2e-aks-live-model-local` provisions extra Azure OpenAI infrastructure and consumes real model quota
- the current live-model profile targets `swedencentral` and validates `gpt-5` plus `gpt-5.1`
- this suite is intentionally separate because model quota and regional model availability can change independently of the smoke AKS path
- the next meaningful higher-level additions are a Redis-backed AKS profile and a live-model embeddings path once the infra profile provisions an embeddings deployment
