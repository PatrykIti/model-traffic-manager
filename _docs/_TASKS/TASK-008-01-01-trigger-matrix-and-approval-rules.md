[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-008-01-01: Trigger Matrix and Approval Rules
# FileName: TASK-008-01-01-trigger-matrix-and-approval-rules.md

**Priority:** High
**Category:** Testing Infrastructure Planning
**Estimated Effort:** Small
**Dependencies:** TASK-008-01
**Status:** **Done** (2026-03-13)

---

## Overview

Define the allowed triggers for each expensive test level.

---

## Trigger Rules

```text
on_pull_request_default:
    run unit
    run integration-local

on_pull_request_opt_in:
    optionally run integration-azure
    optionally run e2e-aks

on_workflow_dispatch:
    allow integration-azure
    allow e2e-aks

on_schedule:
    allow integration-azure
    optionally allow e2e-aks
```

---

## Approval Rules

- `integration-azure` may be allowed on labeled PRs or manual dispatch
- `e2e-aks` should require manual dispatch, explicit label, or release-grade trigger
- production-like AKS test runs should never happen implicitly on every branch push

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-008-01-01-trigger-matrix-and-approval-rules.md`
