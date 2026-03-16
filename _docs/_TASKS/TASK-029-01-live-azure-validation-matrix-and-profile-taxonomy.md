[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-029](./TASK-029-live-azure-validation-expansion-for-router-surfaces.md)

# TASK-029-01: Live Azure Validation Matrix and Profile Taxonomy
# FileName: TASK-029-01-live-azure-validation-matrix-and-profile-taxonomy.md

**Priority:** High
**Category:** Validation Planning
**Estimated Effort:** Small
**Dependencies:** TASK-029
**Status:** **Done** (2026-03-16)

---

## Overview

Define which behaviors belong to which live validation profile.

Recommended placement:

- `integration-azure`
  token acquisition, outbound auth, direct provider probes
- `e2e-aks`
  cluster smoke and runtime wiring
- `e2e-aks-live-model`
  real routed chat and embeddings paths
- dedicated Redis-backed AKS profile
  multi-replica coordination
- dedicated shared-service live profile
  router-proxied service execution and direct-access boundary checks

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-029-01-live-azure-validation-matrix-and-profile-taxonomy.md`
