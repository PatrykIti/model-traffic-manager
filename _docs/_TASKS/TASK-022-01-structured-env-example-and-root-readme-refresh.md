[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-022](./TASK-022-environment-example-and-root-readme-reconciliation.md)

# TASK-022-01: Structured `.env.example` and Root README Refresh
# FileName: TASK-022-01-structured-env-example-and-root-readme-refresh.md

**Priority:** High
**Category:** Documentation Implementation
**Estimated Effort:** Small
**Dependencies:** TASK-022
**Status:** **Done** (2026-03-15)

---

## Overview

Turn the root environment example into a real operator/developer reference and remove stale statements from the repository `README.md`.

Detailed work:
1. Enumerate the application runtime settings from `AppSettings`.
2. Add categorized comments for runtime, Redis, secret-ref, and higher-level validation variables.
3. Clarify which variables are developer overrides versus script-managed markers.
4. Refresh the root `README.md` so the implementation summary matches the actual router runtime and validation surfaces.

---

## Documentation Updates Required

- `.env.example`
- `README.md`
- `_docs/_TASKS/TASK-022-01-structured-env-example-and-root-readme-refresh.md`
