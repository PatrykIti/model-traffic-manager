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

- workflow: `.github/workflows/integration-azure.yml` with `suite` input selecting `integration-azure`, `integration-azure-chat`, or `integration-azure-embeddings`
- test suite: `tests/integration_azure/`
- infra scope: `infra/integration-azure/`
- shared tfvars baseline: `infra/_shared/env/dev1.tfvars` and `infra/_shared/env/prd1.tfvars`
- local command: `make integration-azure-local`

Current integration-azure profiles:

- `make integration-azure-local`
  Managed Identity token and auth-header smoke against real Azure auth
- `make integration-azure-chat-local`
  direct Azure OpenAI chat provider probe through repository auth and outbound adapters
- `make integration-azure-embeddings-local`
  direct Azure OpenAI embeddings provider probe through repository auth and outbound adapters

Dedicated provider-probe activation:

- chat suite: `tests/integration_azure_chat/`
- chat infra scope: `infra/integration-azure-chat/`
- embeddings suite: `tests/integration_azure_embeddings/`
- embeddings infra scope: `infra/integration-azure-embeddings/`

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

- workflow: `.github/workflows/e2e-aks.yml` with `suite` input selecting `e2e-aks`, `e2e-aks-live-model`, `e2e-aks-live-embeddings`, `e2e-aks-live-load-balancing`, `e2e-aks-live-shared-services`, or `e2e-aks-redis`
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
- controlled failover from an in-cluster mock primary to a live Azure OpenAI secondary
- live observation of `cooldown` and `circuit_open` transitions through router metrics

Default rule:

- use this suite deliberately because it consumes real model quota and provisions broader temporary infrastructure

Default rule:

- this level remains opt-in and is not part of the default PR quality workflow

Recommended next additions:

### 6. `e2e-aks-live-embeddings`

Purpose:

- prove a real embeddings request through AKS, Workload Identity, router runtime config, and Azure OpenAI

Environment:

- AKS
- Azure OpenAI embeddings deployment
- workload identity and Azure RBAC

Current repository activation:

- local command: `make e2e-aks-live-embeddings-local`
- test suite: `tests/e2e_aks_live_embeddings/`
- infra scope: `infra/e2e-aks-live-embeddings/`
- current model profile: `text-embedding-3-small` in `germanywestcentral`

Current live embeddings coverage:

- real `POST /v1/embeddings/{deployment_id}` requests through AKS
- generated router config from Terraform outputs for embeddings deployments
- live validation that a non-empty embedding vector is returned

Default rule:

- use this suite deliberately because it provisions real Azure OpenAI capacity and consumes live embeddings quota

### 7. `e2e-aks-live-load-balancing`

Purpose:

- prove model-aware same-tier balancing and active-standby behavior on live Azure-backed infra

Environment:

- AKS
- router runtime config rendered for load-balancing scenarios
- in-cluster mock downstreams used to make traffic distribution deterministic

Current repository activation:

- local command: `make e2e-aks-live-load-balancing-local`
- test suite: `tests/e2e_aks_live_load_balancing/`
- infra scope: `infra/e2e-aks-live-load-balancing/`

Current live load-balancing coverage:

- weighted same-tier distribution for chat pools
- active-standby preference and standby failover behavior
- weighted same-tier distribution for embeddings-safe pools

Default rule:

- use this suite deliberately because it provisions AKS infrastructure specifically to validate balancing semantics under real runtime conditions

### 8. `e2e-aks-live-shared-services`

Purpose:

- prove the shared-service execution model on live Azure and AKS infrastructure

Environment:

- AKS
- router runtime config rendered for shared-service scenarios
- in-cluster mock downstreams for router-proxy shared services
- real Azure Storage account metadata for direct-backend-access shared services

Current repository activation:

- local command: `make e2e-aks-live-shared-services-local`
- test suite: `tests/e2e_aks_live_shared_services/`
- infra scope: `infra/e2e-aks-live-shared-services/`

Current live shared-services coverage:

- `GET /shared-services` exposes router-proxy and direct-backend-access services from the live registry
- `POST /v1/shared-services/{service_id}` rejects direct-backend-access services with a fail-closed response
- `router_proxy + single_endpoint` executes against an in-cluster live mock
- `router_proxy + tiered_failover` fails over from a primary mock to a secondary mock and skips the primary on the next request via shared health state

Default rule:

- use this suite deliberately because it provisions AKS infrastructure plus a real Azure storage dependency for the direct-access contract

### 9. `e2e-aks-redis`

Purpose:

- prove that Redis-backed runtime state is shared correctly across multiple router replicas on AKS

Environment:

- AKS
- two router replicas
- in-cluster Redis
- in-cluster mock upstreams for deterministic rate-limit, circuit, and limiter scenarios

Current repository activation:

- local command: `make e2e-aks-redis-local`
- test suite: `tests/e2e_aks_redis/`
- infra scope: `infra/e2e-aks-redis/`

Current Redis-backed coverage:

- request-rate limiting shared across replicas
- concurrency limiting shared across replicas
- cooldown visibility shared across replicas
- circuit-open visibility shared across replicas

Default rule:

- use this suite deliberately because it provisions a dedicated multi-replica AKS profile specifically to validate Redis-backed shared state behavior

## Current quota-aware AKS suite placement

The current `dev1` and `prd1` suite placement is intentionally split across regions and VM families:

- `e2e-aks`: `westeurope` + `Standard_D2s_v4`
- `e2e-aks-live-model`: `westeurope` + `Standard_D2ds_v4`
- `e2e-aks-live-embeddings`: `northeurope` + `Standard_D2s_v4`
- `e2e-aks-live-load-balancing`: `northeurope` + `Standard_D2ds_v4`
- `e2e-aks-live-shared-services`: `westeurope` + `Standard_D2s_v4`
- `e2e-aks-redis`: `northeurope` + `Standard_D2s_v4`

Intent:

- spread AKS validation pressure across both `westeurope` and `northeurope`
- use only VM families with explicitly known quota in the target subscription
- keep suite sizing explicit in `infra/<scope>/env/<environment>.tfvars`

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
