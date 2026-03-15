[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-023-02: Embeddings Live Provider Request Path and Auth Matrix
# FileName: TASK-023-02-embeddings-live-provider-request-path-and-auth-matrix.md

**Priority:** High
**Category:** Higher-Level Validation
**Estimated Effort:** Medium
**Dependencies:** TASK-023
**Status:** **To Do**

---

## Overview

Add a live embeddings provider path and split its auth validation into explicit
Managed Identity and API-key modes.

## Sub-Tasks

### TASK-023-02-01: Managed Identity provider path

**Status:** To Do

Validate the embeddings path against the provider using Managed Identity.

### TASK-023-02-02: API-key fallback provider path

**Status:** To Do

Validate the embeddings path against the provider using explicit API-key
fallback.

## Testing Requirements

- embeddings live validation exists for both main auth modes
- failures remain attributable to the chosen auth mode instead of an ambiguous
  mixed path

## Documentation Updates Required

- `_docs/_TASKS/TASK-023-02-embeddings-live-provider-request-path-and-auth-matrix.md`
- `_docs/_TASKS/TASK-023-02-01-managed-identity-provider-path.md`
- `_docs/_TASKS/TASK-023-02-02-api-key-fallback-provider-path.md`
