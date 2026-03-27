[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-040-05](./TASK-040-05-quota-aware-infrastructure-profile-selection-and-vm-family-strategy.md)

# TASK-040-05-01: Environment-Specific AKS Validation Profile Matrix
# FileName: TASK-040-05-01-environment-specific-aks-validation-profile-matrix.md

**Priority:** High
**Category:** Infrastructure Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-040-05
**Status:** **Done** (2026-03-19)

---

## Overview

Encode the current quota-aware AKS validation placement directly in per-scope `env/*.tfvars` files.

## Documentation Updates Required

- `infra/e2e-aks/env/`
- `infra/e2e-aks-live-model/env/`
- `infra/e2e-aks-live-embeddings/env/`
- `infra/e2e-aks-live-load-balancing/env/`
- `infra/e2e-aks-live-shared-services/env/`
- `infra/e2e-aks-redis/env/`
