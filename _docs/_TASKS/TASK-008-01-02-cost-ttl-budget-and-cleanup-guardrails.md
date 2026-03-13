[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-008-01-02: Cost, TTL, Budget, and Cleanup Guardrails
# FileName: TASK-008-01-02-cost-ttl-budget-and-cleanup-guardrails.md

**Priority:** High
**Category:** Testing Infrastructure Planning
**Estimated Effort:** Small
**Dependencies:** TASK-008-01
**Status:** **Done** (2026-03-13)

---

## Overview

Define the non-negotiable cost and cleanup controls for temporary Azure environments.

---

## Guardrails

- every temporary test environment must live in its own resource group
- every resource group must carry tags:
  - `purpose=e2e`
  - `owner=model-traffic-manager`
  - `run_id=<github_run_id>`
  - `ttl_hours=<n>`
  - `created_at=<timestamp>`
- workflows must destroy the environment in an `always()` cleanup path
- a separate janitor workflow must delete expired test environments
- concurrency limits should prevent multiple overlapping expensive runs unless explicitly intended
- environment naming must include PR number, SHA, or workflow run ID

---

## Cost Policy

- prefer the smallest valid node pool and the smallest resource set
- create only the resources required by the specific test level
- do not provision AKS unless the scenario truly needs in-cluster runtime validation

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-008-01-02-cost-ttl-budget-and-cleanup-guardrails.md`
