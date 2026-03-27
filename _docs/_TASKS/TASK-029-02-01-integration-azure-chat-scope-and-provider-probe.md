[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-029-02](./TASK-029-02-integration-azure-outbound-provider-probes-for-chat-and-embeddings.md)

# TASK-029-02-01: `integration-azure-chat` Scope and Provider Probe
# FileName: TASK-029-02-01-integration-azure-chat-scope-and-provider-probe.md

**Priority:** High
**Category:** Validation Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-029-02
**Status:** **Done** (2026-03-18)

---

## Overview

Add a dedicated Azure-only scope and test suite that proves direct Azure OpenAI chat calls through the repository auth and outbound adapters.

## Documentation Updates Required

- `infra/integration-azure-chat/`
- `tests/integration_azure_chat/`
- `Makefile`
- `scripts/release/run_azure_test_suite.sh`
- `docs/operations/testing-levels-and-environments.md`
- `docs/getting-started/local-development.md`
