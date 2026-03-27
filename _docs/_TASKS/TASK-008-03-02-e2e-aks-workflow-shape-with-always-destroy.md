[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-008-03-02: `e2e-aks` Workflow Shape with `always()` Destroy
# FileName: TASK-008-03-02-e2e-aks-workflow-shape-with-always-destroy.md

**Priority:** High
**Category:** Testing Infrastructure Planning
**Estimated Effort:** Small
**Dependencies:** TASK-008-03
**Status:** **Done** (2026-03-13)

---

## Overview

Define the fully ephemeral AKS workflow used only when cluster runtime validation is truly needed.

---

## Workflow Shape

```text
job e2e-aks:
    checkout
    authenticate to Azure
    build and publish test image
    terraform apply ephemeral AKS environment
    deploy app to cluster
    run smoke and e2e tests
    collect cluster logs, events, and pod diagnostics
    terraform destroy in always()
```

---

## Non-Negotiable Rule

`destroy` must run under `if: always()` or the equivalent unconditional cleanup mechanism.

Also add a separate janitor workflow that deletes expired resource groups in case the main workflow is interrupted.

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-008-03-02-e2e-aks-workflow-shape-with-always-destroy.md`
