[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-008-01: Trigger Policy and Cost Guardrails for Temporary Azure Environments
# FileName: TASK-008-01-trigger-policy-and-cost-guardrails-for-temporary-azure-environments.md

**Priority:** High
**Category:** Testing Infrastructure Planning
**Estimated Effort:** Small
**Dependencies:** TASK-008
**Status:** **Done** (2026-03-13)

---

## Overview

Define when temporary Azure infrastructure is allowed to run and how the repository prevents accidental cost explosions.

---

## Sub-Tasks

### TASK-008-01-01: Trigger matrix and approval rules

**Status:** Done

Define which workflows run on PRs, labels, manual dispatch, and schedules.

### TASK-008-01-02: Cost, TTL, budget, and cleanup guardrails

**Status:** Done

Define the hard guardrails that keep Azure test spend bounded.

---

## Recommended Trigger Matrix

### Default pull requests

Run:

- `unit`
- `integration-local`

Do not run:

- full `integration-azure`
- full `e2e-aks`

### Pull requests with explicit opt-in

Allow:

- `integration-azure` for selected scenarios
- `e2e-aks` only behind explicit opt-in such as a label or manual dispatch

### Manual dispatch

Allow:

- `integration-azure`
- fully ephemeral `e2e-aks`

### Nightly or scheduled runs

Allow:

- `integration-azure`
- optionally `e2e-aks`

### Pre-release or release-candidate checks

Allow:

- the most expensive end-to-end path

---

## Recommendation

For a private owner without strong ROI yet:

- never run full ephemeral AKS on every normal PR
- require explicit opt-in or manual dispatch for AKS-backed tests
- keep Azure-backed tests targeted and event-driven

---

## Testing Requirements

- the trigger matrix must clearly block accidental full-AKS-per-PR behavior
- opt-in mechanics must be explicit and reviewable

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-008-01-trigger-policy-and-cost-guardrails-for-temporary-azure-environments.md`
- `_docs/_TASKS/TASK-008-01-01-trigger-matrix-and-approval-rules.md`
- `_docs/_TASKS/TASK-008-01-02-cost-ttl-budget-and-cleanup-guardrails.md`
