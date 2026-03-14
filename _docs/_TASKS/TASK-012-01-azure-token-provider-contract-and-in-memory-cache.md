[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-012-01: Azure Token Provider Contract and In-Memory Cache
# FileName: TASK-012-01-azure-token-provider-contract-and-in-memory-cache.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-012
**Status:** **To Do**

---

## Overview

Define how the router acquires and reuses Azure tokens for `managed_identity` auth.

---

## Sub-Tasks

### TASK-012-01-01: Credential selection and token acquisition semantics

**Status:** To Do

Define which credential path is used and how token acquisition errors surface back into the application.

### TASK-012-01-02: Cache key, expiry skew, and refresh behavior

**Status:** To Do

Define when a cached token is reused and when the router proactively refreshes it.

---

## Testing Requirements

- token acquisition does not leak Azure SDK details into the application layer
- cache semantics are explicit and deterministic
- failure modes can be tested without real Azure access

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-012-01-azure-token-provider-contract-and-in-memory-cache.md`
- `_docs/_TASKS/TASK-012-01-01-credential-selection-and-token-acquisition-semantics.md`
- `_docs/_TASKS/TASK-012-01-02-cache-key-expiry-skew-and-refresh-behavior.md`
