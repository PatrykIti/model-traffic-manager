[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-021-02: AKS Runner and Workflow Migration from Raw Manifests to Helm
# FileName: TASK-021-02-aks-runner-and-workflow-migration-from-raw-manifests-to-helm.md

**Priority:** High
**Category:** Packaging and Validation
**Estimated Effort:** Medium
**Dependencies:** TASK-021
**Status:** **To Do**

---

## Overview

Switch the local runners and workflow deployment steps from direct manifest
application to Helm release operations.

## Testing Requirements

- both AKS-backed suites deploy successfully through Helm
- cleanup still removes the deployed release and all temporary Azure resources

## Documentation Updates Required

- `docs/getting-started/local-development.md`
- `docs/operations/testing-levels-and-environments.md`
- `_docs/_TASKS/TASK-021-02-aks-runner-and-workflow-migration-from-raw-manifests-to-helm.md`
