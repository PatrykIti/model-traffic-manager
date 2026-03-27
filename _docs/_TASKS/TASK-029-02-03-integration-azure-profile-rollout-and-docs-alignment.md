[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-029-02](./TASK-029-02-integration-azure-outbound-provider-probes-for-chat-and-embeddings.md)

# TASK-029-02-03: Integration-Azure Profile Rollout and Docs Alignment
# FileName: TASK-029-02-03-integration-azure-profile-rollout-and-docs-alignment.md

**Priority:** High
**Category:** Workflow and Documentation
**Estimated Effort:** Small
**Dependencies:** TASK-029-02-01, TASK-029-02-02
**Status:** **Done** (2026-03-18)

---

## Overview

Expose the new Azure-only provider-probe profiles through `make`, runner wiring, environment contracts, and official docs.

## Documentation Updates Required

- `Makefile`
- `scripts/release/run_azure_test_suite.sh`
- `.env.example`
- `docs/operations/testing-levels-and-environments.md`
- `docs/getting-started/local-development.md`
- `_docs/_TASKS/TASK-029-02-03-integration-azure-profile-rollout-and-docs-alignment.md`
