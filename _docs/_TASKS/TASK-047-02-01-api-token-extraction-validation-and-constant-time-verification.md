[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-047-02](./TASK-047-02-runtime-authentication-middleware-and-request-principal-propagation.md)

# TASK-047-02-01: API Token Extraction, Validation, and Constant-Time Verification
# FileName: TASK-047-02-01-api-token-extraction-validation-and-constant-time-verification.md

**Priority:** High
**Category:** Runtime Security
**Estimated Effort:** Medium
**Dependencies:** TASK-047-02
**Status:** **In Progress** (2026-03-27)

---

## Overview

Implement the bearer-token inbound auth path.

Technical details:

- parse `Authorization: Bearer <token>`
- reject missing or malformed bearer headers with `401`
- resolve token descriptors from config and secret provider
- hash incoming token candidate and verify via constant-time comparison
- map matched token metadata into the normalized request principal
- return `403` when authentication succeeded but route-level authorization disallows the principal

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-047-02-01-api-token-extraction-validation-and-constant-time-verification.md`
