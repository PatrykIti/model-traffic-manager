[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-009-02-01: Outbound Invoker Contract and `httpx` Implementation
# FileName: TASK-009-02-01-outbound-invoker-contract-and-httpx-implementation.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-009-02
**Status:** **Done** (2026-03-13)

---

## Overview

Create the first outbound call abstraction for the router.

This work item owns:
- application port for outbound calls
- DTO or contract for outbound result
- infrastructure implementation using `httpx`

---

## Target Files

```text
app/application/ports/outbound_invoker.py
app/application/dto/outbound_response.py
app/infrastructure/http/httpx_outbound_invoker.py
```

---

## Pseudocode

```text
send(endpoint, body, headers, timeout):
    call upstream via httpx
    return status, headers subset, parsed JSON or raw text
```

---

## Testing Requirements

- use `respx` or equivalent for local integration and unit-level adapter tests
- connection and timeout failures are surfaced predictably

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-009-02-01-outbound-invoker-contract-and-httpx-implementation.md`
