[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-047-02](./TASK-047-02-runtime-authentication-middleware-and-request-principal-propagation.md)

# TASK-047-02-02: Entra JWT Validation, JWKS Refresh, and Authorization Decision Flow
# FileName: TASK-047-02-02-entra-jwt-validation-jwks-refresh-and-authorization-decision-flow.md

**Priority:** High
**Category:** Runtime Security
**Estimated Effort:** Medium
**Dependencies:** TASK-047-02
**Status:** **Done** (2026-03-27)

---

## Overview

Implement the Entra ID inbound auth path for service callers.

Technical details:

- extract bearer JWT from `Authorization`
- fetch and cache JWKS/signing keys safely
- validate signature, issuer, tenant, audience, `nbf`, `exp`, and token version assumptions
- distinguish app-only token paths from delegated user-token paths
- prefer app-role based authorization for app-only callers and verify `roles` claims
- optionally allow ACL-based caller checks only if explicitly configured

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-047-02-02-entra-jwt-validation-jwks-refresh-and-authorization-decision-flow.md`
