[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-021-01: Helm Chart Structure and Values Surface
# FileName: TASK-021-01-helm-chart-structure-and-values-surface.md

**Priority:** High
**Category:** Packaging
**Estimated Effort:** Medium
**Dependencies:** TASK-021
**Status:** **To Do**

---

## Overview

Create the repository-owned Helm chart and define its main template layout,
values file structure, and release inputs.

## Sub-Tasks

### TASK-021-01-01: Values contract for image, config, identity, service, and probes

**Status:** To Do

Define the minimal but stable values contract exposed by the chart.

## Testing Requirements

- the chart renders cleanly with repository-owned baseline values
- template structure stays small and explicit enough for review and debugging

## Documentation Updates Required

- `_docs/_TASKS/TASK-021-01-helm-chart-structure-and-values-surface.md`
- `_docs/_TASKS/TASK-021-01-01-values-contract-for-image-config-identity-service-and-probes.md`
