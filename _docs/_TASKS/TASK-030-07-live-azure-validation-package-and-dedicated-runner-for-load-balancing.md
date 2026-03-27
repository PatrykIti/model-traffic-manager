[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-030](./TASK-030-model-aware-load-balancing-within-tier.md)

# TASK-030-07: Live Azure Validation Package and Dedicated Runner for Load Balancing
# FileName: TASK-030-07-live-azure-validation-package-and-dedicated-runner-for-load-balancing.md

**Priority:** High
**Category:** Validation Planning
**Estimated Effort:** Medium
**Dependencies:** TASK-030, TASK-029
**Status:** **Done** (2026-03-17)

---

## Overview

Add a dedicated live validation package for load balancing so operators can run one command and prove balancing behavior on real Azure-backed infra.

Target outcome:
- new infra scope dedicated to load-balancing validation
- deterministic test cases for:
  - weighted balancing in the same tier
  - compatibility-group isolation
  - fallback out of a balanced pool
- a dedicated local command such as:
  `make e2e-aks-live-load-balancing-local ENVIRONMENT=dev1`

Recommended live checks:
- same-tier chat active-active pool across multiple Azure OpenAI deployments
- embeddings compatibility protection
- metrics and decision proof that traffic was distributed and/or isolated correctly

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-030-07-live-azure-validation-package-and-dedicated-runner-for-load-balancing.md`
