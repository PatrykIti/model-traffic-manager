[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-040-06](./TASK-040-06-ci-trigger-matrix-cost-gating-and-scheduling-policy.md)

# TASK-040-06-01: Suite Trigger Policy in Registry and Workflows
# FileName: TASK-040-06-01-suite-trigger-policy-in-registry-and-workflows.md

**Priority:** High
**Category:** CI Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-040-06, TASK-040-07
**Status:** **Done** (2026-03-20)

---

## Overview

Define nightly and release eligibility in the canonical suite registry and expose that policy to GitHub workflows.

## Documentation Updates Required

- `scripts/release/validation_suite_registry.py`
- `.github/workflows/`
