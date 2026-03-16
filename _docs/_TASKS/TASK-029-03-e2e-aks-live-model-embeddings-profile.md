[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-029](./TASK-029-live-azure-validation-expansion-for-router-surfaces.md)

# TASK-029-03: `e2e-aks-live-model` Embeddings Profile
# FileName: TASK-029-03-e2e-aks-live-model-embeddings-profile.md

**Priority:** High
**Category:** Validation Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-029, TASK-029-01
**Status:** **To Do**

---

## Overview

Add a live embeddings deployment and AKS validation path so the router proves embeddings end-to-end against real Azure OpenAI infrastructure.

Candidate checks:
- real `POST /v1/embeddings/{deployment_id}` through AKS
- non-empty embedding vector response
- generated router config from Terraform outputs for embeddings deployments

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-029-03-e2e-aks-live-model-embeddings-profile.md`
