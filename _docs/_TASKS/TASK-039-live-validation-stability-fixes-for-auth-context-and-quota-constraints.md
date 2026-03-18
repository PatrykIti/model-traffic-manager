[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-039: Live Validation Stability Fixes for Auth, Context, and Quota Constraints
# FileName: TASK-039-live-validation-stability-fixes-for-auth-context-and-quota-constraints.md

**Priority:** High
**Category:** Validation Stability
**Estimated Effort:** Medium
**Dependencies:** TASK-029-02, TASK-029-05, TASK-029-06, TASK-029-07
**Status:** **Done** (2026-03-18)

---

## Overview

Stabilize the expanded live validation matrix after first real runs exposed auth, Kubernetes-context, storage-fixture, and quota issues.

Business goal:
- make `integration-azure-chat` and `integration-azure-embeddings` succeed under the actual executing principal
- isolate AKS kubeconfig per run so concurrent or overlapping suites do not stomp on each other's context
- avoid B-series quota exhaustion by moving AKS validation scopes to a VM family aligned with the broader infrastructure
- keep the shared-services Azure Storage fixture compatible with the chosen storage module behavior

---

## Sub-Tasks

- grant Azure OpenAI user access to the executor principal used by integration-azure provider probes
- isolate AKS runner kubeconfig per run
- move AKS validation defaults away from the constrained B-series family
- re-enable shared-services storage fixture provisioning by avoiding a module-incompatible storage auth setting

---

## Testing Requirements

- `bash -n scripts/release/run_azure_test_suite.sh`
- `uv run ruff check tests/integration_azure_chat/test_chat_provider_live.py tests/integration_azure_embeddings/test_embeddings_provider_live.py scripts/release/render_live_redis_router_config.py tests/e2e_aks_redis/test_redis_multi_replica_live.py`
- `PYTHONPATH=. uv run pytest tests/integration_azure_chat/test_chat_provider_live.py tests/integration_azure_embeddings/test_embeddings_provider_live.py tests/e2e_aks_redis/test_redis_multi_replica_live.py -q`
- `terraform -chdir=infra/e2e-aks-redis validate`
- `terraform -chdir=infra/e2e-aks-live-shared-services validate`

---

## Documentation Updates Required

- `scripts/release/run_azure_test_suite.sh`
- `infra/integration-azure-chat/`
- `infra/integration-azure-embeddings/`
- `infra/e2e-aks/variables.tf`
- `infra/e2e-aks-live-model/variables.tf`
- `infra/e2e-aks-live-embeddings/variables.tf`
- `infra/e2e-aks-live-load-balancing/variables.tf`
- `infra/e2e-aks-live-shared-services/`
- `infra/e2e-aks-redis/variables.tf`
- `_docs/_TASKS/TASK-039-live-validation-stability-fixes-for-auth-context-and-quota-constraints.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/48-2026-03-18-live-validation-stability-fixes-for-auth-context-and-quota-constraints.md`
- `_docs/_CHANGELOG/README.md`
