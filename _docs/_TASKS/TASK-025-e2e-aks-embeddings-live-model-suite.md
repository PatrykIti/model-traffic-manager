[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-025: E2E AKS Embeddings Live-Model Suite
# FileName: TASK-025-e2e-aks-embeddings-live-model-suite.md

**Priority:** High
**Category:** Higher-Level Validation
**Estimated Effort:** Medium
**Dependencies:** TASK-011, TASK-020
**Status:** **To Do**

---

## Overview

Add a second AKS live-model suite that validates the real embeddings path
through AKS, Workload Identity, router config, and Azure OpenAI.

Business goal:
- give embeddings the same end-to-end proof level that chat now has
- keep the chat live suite focused while adding endpoint parity
- reuse as much of the existing live-model scope and runner shape as possible

## Sub-Tasks

### TASK-025-01: Live-model scope and config reuse for embeddings

**Status:** To Do

Reuse or extend the current live-model scope for embeddings validation.

### TASK-025-02: AKS embeddings live suite and response contract

**Status:** To Do

Add the live embeddings AKS suite and define its assertion model.

### TASK-025-03: Docs and task/changelog alignment

**Status:** To Do

Document the new suite and keep internal tracking aligned.

## Testing Requirements

- the suite proves a real embeddings response through the router on AKS
- cleanup still runs after failures
- the assertion contract checks embeddings structure without making the suite
  quota-heavy

## Documentation Updates Required

- `docs/getting-started/local-development.md`
- `docs/operations/testing-levels-and-environments.md`
- `_docs/_TASKS/TASK-025-e2e-aks-embeddings-live-model-suite.md`
- `_docs/_TASKS/TASK-025-01-live-model-scope-and-config-reuse-for-embeddings.md`
- `_docs/_TASKS/TASK-025-02-aks-embeddings-live-suite-and-response-contract.md`
- `_docs/_TASKS/TASK-025-03-docs-and-task-changelog-alignment.md`
