[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-029-07](./TASK-029-07-runner-workflow-and-documentation-rollout-for-expanded-live-suites.md)

# TASK-029-07-01: Workflow Suite-Input Rollout for Azure Profiles
# FileName: TASK-029-07-01-workflow-suite-input-rollout-for-azure-profiles.md

**Priority:** High
**Category:** Workflow Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-029-07
**Status:** **Done** (2026-03-18)

---

## Overview

Refactor the GitHub workflows so the Azure-backed validation matrix is selected through `workflow_dispatch` suite inputs instead of duplicated per-profile logic.

## Documentation Updates Required

- `.github/workflows/integration-azure.yml`
- `.github/workflows/e2e-aks.yml`
