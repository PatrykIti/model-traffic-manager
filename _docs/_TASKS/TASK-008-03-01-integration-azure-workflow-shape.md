[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-008-03-01: `integration-azure` Workflow Shape
# FileName: TASK-008-03-01-integration-azure-workflow-shape.md

**Priority:** High
**Category:** Testing Infrastructure Planning
**Estimated Effort:** Small
**Dependencies:** TASK-008-03
**Status:** **Done** (2026-03-13)

---

## Overview

Define the least expensive cloud-backed workflow that still proves real Azure behavior.

---

## Workflow Shape

```text
job integration-azure:
    checkout
    authenticate to Azure
    terraform apply minimal Azure resources
    run Azure-backed integration tests
    collect test artifacts
    terraform destroy in always()
```

---

## Notes

- this workflow should be cheaper and more frequent than `e2e-aks`
- use it first when a feature depends on Azure behavior but not on AKS deployment runtime

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-008-03-01-integration-azure-workflow-shape.md`
