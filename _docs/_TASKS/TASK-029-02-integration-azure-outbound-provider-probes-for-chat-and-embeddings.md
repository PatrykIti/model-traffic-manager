[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-029](./TASK-029-live-azure-validation-expansion-for-router-surfaces.md)

# TASK-029-02: `integration-azure` Outbound Provider Probes for Chat and Embeddings
# FileName: TASK-029-02-integration-azure-outbound-provider-probes-for-chat-and-embeddings.md

**Priority:** High
**Category:** Validation Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-029, TASK-029-01
**Status:** **Done** (2026-03-18)

---

## Overview

Extend `integration-azure` beyond token acquisition so it proves real outbound provider responses for both chat-related and embeddings-related paths.

Candidate checks:
- Managed Identity token for Azure OpenAI scope
- live outbound call for chat-compatible provider path
- live outbound call for embeddings-compatible provider path
- auth-header preparation with explicit `client_id` where configured

## Sub-Tasks

### TASK-029-02-01: `integration-azure-chat` scope and provider probe

**Status:** Done (2026-03-18)

Add a dedicated Azure-only scope, outputs contract, and live chat provider test.

### TASK-029-02-02: `integration-azure-embeddings` scope and provider probe

**Status:** Done (2026-03-18)

Add a dedicated Azure-only scope, outputs contract, and live embeddings provider test.

### TASK-029-02-03: Integration-azure profile rollout and docs alignment

**Status:** Done (2026-03-18)

Expose the new chat and embeddings probe profiles through `make`, runner wiring, env vars, and docs.

---

## Documentation Updates Required

- `infra/integration-azure-chat/`
- `infra/integration-azure-embeddings/`
- `tests/integration_azure_chat/`
- `tests/integration_azure_embeddings/`
- `Makefile`
- `scripts/release/run_azure_test_suite.sh`
- `.env.example`
- `docs/operations/testing-levels-and-environments.md`
- `docs/getting-started/local-development.md`
- `_docs/_TASKS/TASK-029-02-integration-azure-outbound-provider-probes-for-chat-and-embeddings.md`
- `_docs/_TASKS/TASK-029-02-01-integration-azure-chat-scope-and-provider-probe.md`
- `_docs/_TASKS/TASK-029-02-02-integration-azure-embeddings-scope-and-provider-probe.md`
- `_docs/_TASKS/TASK-029-02-03-integration-azure-profile-rollout-and-docs-alignment.md`
