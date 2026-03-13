[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-009-01: Chat Proxy Contract and Error Model
# FileName: TASK-009-01-chat-proxy-contract-and-error-model.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-009
**Status:** **Done** (2026-03-13)

---

## Overview

Define the contract for the first real proxy route so the rest of Phase 2 has a stable behavioral target.

Scope:
- incoming request shape policy
- outbound response passthrough policy
- basic application/domain error taxonomy
- HTTP mapping for expected failure classes

---

## Security Contract

- visibility: `internal`
- client auth path: out of scope in this phase; route remains internal-only by operational convention
- rate-limit bucket: deferred to a future task, but the contract must not prevent adding it
- nonce / signature / HMAC: not used in this phase
- reCAPTCHA: not applicable
- internal mode: yes

---

## Sub-Tasks

### TASK-009-01-01: Inbound request and passthrough response contract

**Status:** Done (2026-03-13)

Define how much of the OpenAI-style payload is accepted raw and how the outbound response is returned.

### TASK-009-01-02: Error taxonomy and HTTP mapping for the first proxy path

**Status:** Done (2026-03-13)

Define the error surface and how application errors map to HTTP responses.

---

## Testing Requirements

- contract decisions are testable without real Azure
- the response passthrough rule is explicit enough for integration tests

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-009-01-chat-proxy-contract-and-error-model.md`
- `_docs/_TASKS/TASK-009-01-01-inbound-request-and-passthrough-response-contract.md`
- `_docs/_TASKS/TASK-009-01-02-error-taxonomy-and-http-mapping-for-the-first-proxy-path.md`
