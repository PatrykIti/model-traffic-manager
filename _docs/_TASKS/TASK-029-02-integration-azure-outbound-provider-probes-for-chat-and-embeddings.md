[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-029](./TASK-029-live-azure-validation-expansion-for-router-surfaces.md)

# TASK-029-02: `integration-azure` Outbound Provider Probes for Chat and Embeddings
# FileName: TASK-029-02-integration-azure-outbound-provider-probes-for-chat-and-embeddings.md

**Priority:** High
**Category:** Validation Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-029, TASK-029-01
**Status:** **To Do**

---

## Overview

Extend `integration-azure` beyond token acquisition so it proves real outbound provider responses for both chat-related and embeddings-related paths.

Candidate checks:
- Managed Identity token for Azure OpenAI scope
- live outbound call for chat-compatible provider path
- live outbound call for embeddings-compatible provider path
- auth-header preparation with explicit `client_id` where configured

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-029-02-integration-azure-outbound-provider-probes-for-chat-and-embeddings.md`
