[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-009-04: API Route and Local Integration Proof
# FileName: TASK-009-04-api-route-and-local-integration-proof.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-009-03
**Status:** **Done** (2026-03-13)

---

## Overview

Expose the first proxy path through the API and prove the full local flow.

Scope:
- route module for chat completions
- container wiring for the use case and its dependencies
- `integration-local` test coverage using mocked upstream responses

---

## Security Contract

- visibility: `internal`
- client auth path: not yet implemented; route is internal-only by deployment convention in this phase
- rate-limit bucket: deferred
- nonce / signature / HMAC: not used in this phase
- reCAPTCHA: not applicable
- internal mode: yes

---

## Sub-Tasks

### TASK-009-04-01: `routes_chat.py` and application wiring

**Status:** Done (2026-03-13)

Create the API route and wire the use case into the container/app state.

### TASK-009-04-02: `integration-local` coverage with mocked upstream behavior

**Status:** Done (2026-03-13)

Prove the full local request path without real Azure.

---

## Testing Requirements

- integration test covers success path
- integration test covers deployment-not-found path
- integration test covers a representative upstream failure path

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-009-04-api-route-and-local-integration-proof.md`
- `_docs/_TASKS/TASK-009-04-01-routes-chat-and-application-wiring.md`
- `_docs/_TASKS/TASK-009-04-02-integration-local-coverage-with-mocked-upstream-behavior.md`
