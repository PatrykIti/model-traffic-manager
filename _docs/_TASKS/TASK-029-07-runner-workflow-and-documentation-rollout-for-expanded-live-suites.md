[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-029](./TASK-029-live-azure-validation-expansion-for-router-surfaces.md)

# TASK-029-07: Runner, Workflow, and Documentation Rollout for Expanded Live Suites
# FileName: TASK-029-07-runner-workflow-and-documentation-rollout-for-expanded-live-suites.md

**Priority:** High
**Category:** Workflow and Documentation Planning
**Estimated Effort:** Medium
**Dependencies:** TASK-029, TASK-029-02, TASK-029-03, TASK-029-04, TASK-029-05, TASK-029-06
**Status:** **Done** (2026-03-18)

---

## Overview

Align local runners, CI workflows, environment variables, and official docs with the expanded live validation matrix.

Required scope:
- local one-command runners
- GitHub workflows and trigger rules
- env var contract
- official docs for testing levels and local development

## Sub-Tasks

### TASK-029-07-01: Workflow suite-input rollout for Azure profiles

**Status:** Done (2026-03-18)

Refactor the GitHub workflows so profile selection happens through `suite` inputs and the shared runner script.

### TASK-029-07-02: Testing docs and environment contract reconciliation

**Status:** Done (2026-03-18)

Update official testing docs and local-development guidance for the full validation matrix.

### TASK-029-07-03: Task board and changelog reconciliation for expanded matrix

**Status:** Done (2026-03-18)

Close the validation-expansion package cleanly in the task board and changelog.

---

## Documentation Updates Required

- `.github/workflows/integration-azure.yml`
- `.github/workflows/e2e-aks.yml`
- `docs/operations/testing-levels-and-environments.md`
- `docs/getting-started/local-development.md`
- `_docs/_TASKS/TASK-029-07-runner-workflow-and-documentation-rollout-for-expanded-live-suites.md`
- `_docs/_TASKS/TASK-029-07-01-workflow-suite-input-rollout-for-azure-profiles.md`
- `_docs/_TASKS/TASK-029-07-02-testing-docs-and-env-contract-reconciliation.md`
- `_docs/_TASKS/TASK-029-07-03-task-board-and-changelog-reconciliation-for-expanded-matrix.md`
