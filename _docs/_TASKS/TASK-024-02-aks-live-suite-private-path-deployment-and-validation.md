[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-024-02: AKS Live-Suite Private-Path Deployment and Validation
# FileName: TASK-024-02-aks-live-suite-private-path-deployment-and-validation.md

**Priority:** High
**Category:** Higher-Level Validation
**Estimated Effort:** Medium
**Dependencies:** TASK-024
**Status:** **To Do**

---

## Overview

Run the AKS live-model suite over the private network path and validate a real
request through the router to Azure OpenAI without public exposure.

## Testing Requirements

- the live suite proves a real model response over the private path
- cleanup still removes all temporary networking resources on failure

## Documentation Updates Required

- `docs/operations/testing-levels-and-environments.md`
- `_docs/_TASKS/TASK-024-02-aks-live-suite-private-path-deployment-and-validation.md`
