[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-047](./TASK-047-inbound-client-auth-with-api-bearer-tokens-and-microsoft-entra-id.md)

# TASK-047-02: Runtime Authentication Middleware and Request Principal Propagation
# FileName: TASK-047-02-runtime-authentication-middleware-and-request-principal-propagation.md

**Priority:** High
**Category:** Runtime Security
**Estimated Effort:** Large
**Dependencies:** TASK-047-01
**Status:** **Done** (2026-03-27)

---

## Overview

Implement the FastAPI-side runtime path for inbound caller authentication.

Technical scope:

1. bearer token extraction from `Authorization`
2. optional Entra JWT validation using JWKS/signing keys
3. normalized request principal attached to request state
4. endpoint protection across chat, embeddings, shared services, and registry endpoints as configured
5. explicit `401` versus `403` behavior

---

## Sub-Tasks

### TASK-047-02-01: API token extraction, validation, and constant-time verification

**Status:** Done (2026-03-27)

Implement router-owned API token validation with secret resolution and token metadata lookup.

### TASK-047-02-02: Entra JWT validation, JWKS refresh, and authorization decision flow

**Status:** Done (2026-03-27)

Implement JWT signature and claim validation for Entra access tokens plus role-based authorization for app-only callers.

### TASK-047-02-03: Request principal context and audit-safe observability fields

**Status:** Done (2026-03-27)

Propagate normalized caller identity into request context, error mapping, and safe observability metadata.

---

## Testing Requirements

- malformed, missing, expired, wrong-audience, and wrong-role tokens are covered
- request state carries a stable principal object for downstream use cases and logging

---

## Documentation Updates Required

- `docs/architecture/request-lifecycle.md`
- `docs/operations/observability-and-health.md`
- `_docs/_TASKS/TASK-047-02-runtime-authentication-middleware-and-request-principal-propagation.md`
- `_docs/_TASKS/TASK-047-02-01-api-token-extraction-validation-and-constant-time-verification.md`
- `_docs/_TASKS/TASK-047-02-02-entra-jwt-validation-jwks-refresh-and-authorization-decision-flow.md`
- `_docs/_TASKS/TASK-047-02-03-request-principal-context-and-audit-safe-observability-fields.md`
