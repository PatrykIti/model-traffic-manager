[Repository README](../../README.md) | [docs](../README.md) | [Operations](./README.md)

# Testing Levels and Environments

This repository uses a layered testing model. The layers are cumulative: introducing a higher-level test environment never removes the need for lower-level tests that cover the same behavior.

## Testing levels

### 1. `unit`

Purpose:

- prove pure logic
- keep feedback fast
- isolate domain and application behavior

Environment:

- no Azure
- no AKS
- no real external services

Typical scope:

- domain invariants
- routing policy behavior
- auth policy behavior
- use case orchestration
- failure classification

### 2. `integration-local`

Purpose:

- prove local application wiring
- prove startup/config/API behavior without cloud dependencies

Environment:

- FastAPI app
- local YAML config
- local or in-process repositories/adapters
- optionally local infra dependencies when needed later

Typical scope:

- startup loading and validation
- route registration
- config-backed repositories
- API responses backed by local runtime objects

### 3. `integration-azure`

Purpose:

- prove real Azure service integration without adding cluster deployment concerns

Environment:

- real Azure services
- no AKS deployment requirement

Typical scope:

- Azure OpenAI / AI Foundry calls
- Managed Identity token acquisition
- Key Vault integration
- later, other Azure-native dependencies that the app talks to directly

Current repository activation:

- workflow: `.github/workflows/integration-azure.yml`
- test suite: `tests/integration_azure/`
- infra scope: `infra/integration-azure/`
- shared tfvars baseline: `infra/_shared/env/dev1.tfvars` and `infra/_shared/env/prd1.tfvars`
- local command: `make integration-azure-local`

Default rule:

- this level remains opt-in and is not part of the default PR quality workflow

Minimal Azure footprint should stay intentionally small and feature-driven.

### 4. `e2e-aks`

Purpose:

- prove the application as a deployed workload
- validate cluster-specific runtime behavior

Environment:

- AKS
- workload identity / deployment model
- Helm or equivalent deployment packaging
- cluster-mounted config/secrets

Typical scope:

- deployment manifests/charts
- namespace-scoped config delivery
- pod identity behavior
- in-cluster startup and health behavior

Current repository activation:

- workflow: `.github/workflows/e2e-aks.yml`
- janitor workflow: `.github/workflows/e2e-azure-janitor.yml`
- test suite: `tests/e2e_aks/`
- Kubernetes runtime assets: `infra/e2e-aks/k8s/`
- infra scope: `infra/e2e-aks/`
- shared tfvars baseline: `infra/_shared/env/dev1.tfvars` and `infra/_shared/env/prd1.tfvars`
- scope-specific overrides: `infra/e2e-aks/env/dev1.tfvars` and `infra/e2e-aks/env/prd1.tfvars`
- local command: `make e2e-aks-local`

Current smoke coverage:

- `GET /health/live`
- `GET /health/ready`
- `GET /deployments`
- `GET /shared-services`
- `GET /metrics`

### 5. `e2e-aks-live-model`

Purpose:

- prove a real chat request through AKS, Workload Identity, router runtime config, and Azure OpenAI

Environment:

- AKS
- Azure OpenAI / AI Foundry resource and deployment
- workload identity and Azure RBAC

Current repository activation:

- local command: `make e2e-aks-live-model-local`
- test suite: `tests/e2e_aks_live_model/`
- infra scope: `infra/e2e-aks-live-model/`
- current model profile: `gpt-5` and `gpt-5.1` in `swedencentral`

Current live-model coverage:

- real `POST /v1/chat/completions/{deployment_id}` requests through AKS
- router config generated from Terraform outputs
- live response validation with a non-empty assistant message

Default rule:

- use this suite deliberately because it consumes real model quota and provisions broader temporary infrastructure

Default rule:

- this level remains opt-in and is not part of the default PR quality workflow

Recommended next additions:

- a Redis-backed AKS profile that proves shared health and limiter state in-cluster
- a live-model embeddings profile once the dedicated infrastructure provisions an embeddings deployment

## Phase mapping

### Phase 0

Required levels:

- `unit`
- `integration-local`

Reason:

- bootstrap and startup logic should be proven before any cloud dependency is introduced

### Phase 1

Required levels:

- `unit`
- `integration-local`

Reason:

- domain, config validation, and deployment registry are still local application concerns

### Phase 2

Required levels:

- `unit`
- `integration-local`

Add when real provider calls appear:

- `integration-azure`

Reason:

- single-upstream routing can be proven locally first, but real outbound integration should be validated once the provider path exists

### Phase 3

Required levels:

- `unit`
- `integration-local`
- `integration-azure`

Reason:

- Managed Identity and Azure-native outbound auth must be proven against real Azure services

### Phase 4

Required levels:

- `unit`
- `integration-local`
- selected `integration-azure` scenarios

Reason:

- multi-upstream and tier behavior remains mostly local logic, but real provider combinations may need targeted Azure-backed validation

### Phase 5

Required levels:

- `unit`
- `integration-local`
- `integration-azure` where Azure services are involved

Potential additions:

- local or dedicated integration coverage for Redis-backed behavior

Reason:

- health, cooldown, and circuit breaker behavior are still primarily logic and adapter concerns

### Later release and deployment phases

Required levels:

- all relevant lower levels
- `e2e-aks`

Reason:

- once Helm, workload identity, namespace-scoped delivery, and full cluster runtime behavior become part of the acceptance criteria, end-to-end AKS coverage is mandatory

## Repository rule

Use the smallest environment that proves the behavior honestly.

That means:

- do not jump to Azure or AKS when unit or local integration tests are enough
- do not skip Azure-backed validation once the feature depends on real Azure behavior
- do not skip AKS end-to-end validation once deployment/runtime behavior is in scope
