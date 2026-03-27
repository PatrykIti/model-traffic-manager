[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-012-02-01: Container Wiring and Config/Runtime Validation Alignment
# FileName: TASK-012-02-01-container-wiring-and-config-runtime-validation-alignment.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Small
**Dependencies:** TASK-012-02
**Status:** **Done** (2026-03-14)

---

## Overview

Align the bootstrap container, auth wiring, and config expectations for `managed_identity`.

Detailed work:
1. Register the token provider and cache in the bootstrap container.
2. Keep config validation and runtime assumptions synchronized for `scope` and optional `client_id`.
3. Preserve the existing `none` and `api_key` behaviors without regression.

---

## Testing Requirements

- the container exposes the correct auth dependencies for the existing use cases
- invalid Managed Identity config still fails early at startup
- adding the new wiring does not change the existing Phase 2 auth paths

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-012-02-01-container-wiring-and-config-runtime-validation-alignment.md`
