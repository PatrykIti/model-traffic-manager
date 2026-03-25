[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-044](./TASK-044-e2e-aks-live-observability-profile-for-azure-monitor-and-consumer-role.md)

# TASK-044-04: Runner, Workflow, Runbook, and Documentation Rollout for the Observability Suite
# FileName: TASK-044-04-runner-workflow-runbook-and-documentation-rollout-for-the-observability-suite.md

**Priority:** High
**Category:** Workflow and Documentation
**Estimated Effort:** Medium
**Dependencies:** TASK-044-01, TASK-044-02, TASK-044-03
**Status:** **Done** (2026-03-25)

---

## Overview

Roll the new live observability suite into the repository's runner, workflow, diagnostics, and operator documentation model.

Detailed work:

1. register `e2e-aks-live-observability` in the validation suite registry
2. wire the shared runner so artifacts include telemetry query outputs
3. update testing docs and local commands
4. extend the existing Application Insights runbook with the exact live-suite interpretation path

---

## Testing Requirements

- registry and shell validation cover the new suite
- workflow and runner docs align with the final suite ID and environment contract

---

## Documentation Updates Required

- `docs/operations/testing-levels-and-environments.md`
- `docs/getting-started/local-development.md`
- `docs/operations/runbooks/application-insights-request-flow-triage.md`
- `_docs/_TASKS/TASK-044-04-runner-workflow-runbook-and-documentation-rollout-for-the-observability-suite.md`
- `_docs/_TASKS/README.md`
