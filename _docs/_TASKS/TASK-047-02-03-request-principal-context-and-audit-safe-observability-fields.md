[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-047-02](./TASK-047-02-runtime-authentication-middleware-and-request-principal-propagation.md)

# TASK-047-02-03: Request Principal Context and Audit-Safe Observability Fields
# FileName: TASK-047-02-03-request-principal-context-and-audit-safe-observability-fields.md

**Priority:** High
**Category:** Observability and Security
**Estimated Effort:** Small
**Dependencies:** TASK-047-02
**Status:** To Do

---

## Overview

Propagate safe caller metadata after successful authentication.

Recommended fields:

- `auth_mode`
- `principal_id`
- `principal_display_name`
- `consumer_role`
- `entra_app_id` or `azp`
- `token_id` for API bearer tokens if configured

Guardrails:

- never log raw bearer tokens or full JWTs
- avoid high-cardinality or PII-heavy caller fields unless explicitly justified

---

## Documentation Updates Required

- `docs/operations/observability-and-health.md`
- `_docs/_TASKS/TASK-047-02-03-request-principal-context-and-audit-safe-observability-fields.md`
