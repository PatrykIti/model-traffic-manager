[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-029-05](./TASK-029-05-live-shared-services-validation-on-azure-and-aks.md)

# TASK-029-05-03: Live Shared-Services Suite, Runner, and Docs Rollout
# FileName: TASK-029-05-03-live-shared-services-suite-runner-and-docs-rollout.md

**Priority:** High
**Category:** Validation Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-029-05-02
**Status:** **Done** (2026-03-18)

---

## Overview

Add the live shared-services test suite, expose it through a dedicated `make` target, and document the new profile.

## Documentation Updates Required

- `tests/e2e_aks_live_shared_services/`
- `Makefile`
- `scripts/release/run_azure_test_suite.sh`
- `.env.example`
- `docs/operations/testing-levels-and-environments.md`
- `docs/getting-started/local-development.md`
- `docs/getting-started/implementation-status.md`
