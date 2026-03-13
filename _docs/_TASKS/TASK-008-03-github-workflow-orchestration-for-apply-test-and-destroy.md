[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-008-03: GitHub Workflow Orchestration for Apply, Test, and Destroy
# FileName: TASK-008-03-github-workflow-orchestration-for-apply-test-and-destroy.md

**Priority:** High
**Category:** Testing Infrastructure Planning
**Estimated Effort:** Small
**Dependencies:** TASK-008
**Status:** **Done** (2026-03-13)

---

## Overview

Define the orchestration model for temporary Azure environments.

Decision:

- GitHub Actions remains the visible orchestrator
- Azure DevOps webhook chaining is not the preferred default path

---

## Sub-Tasks

### TASK-008-03-01: `integration-azure` workflow shape

**Status:** Done

Define the workflow contract for Azure-backed integration tests without AKS.

### TASK-008-03-02: `e2e-aks` workflow shape with `always()` destroy

**Status:** Done

Define the workflow contract for fully ephemeral AKS-backed tests.

---

## Pseudocode

```text
workflow():
    build test image if needed
    terraform apply
    deploy application or test harness
    run tests
    collect logs and artifacts
    terraform destroy in always() cleanup
```

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-008-03-github-workflow-orchestration-for-apply-test-and-destroy.md`
- `_docs/_TASKS/TASK-008-03-01-integration-azure-workflow-shape.md`
- `_docs/_TASKS/TASK-008-03-02-e2e-aks-workflow-shape-with-always-destroy.md`
