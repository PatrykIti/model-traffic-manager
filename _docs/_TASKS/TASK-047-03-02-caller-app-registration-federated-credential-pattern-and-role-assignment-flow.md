[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-047-03](./TASK-047-03-microsoft-entra-id-protected-api-model-app-roles-and-federated-caller-guidance.md)

# TASK-047-03-02: Caller App Registration, Federated Credential Pattern, and Role-Assignment Flow
# FileName: TASK-047-03-02-caller-app-registration-federated-credential-pattern-and-role-assignment-flow.md

**Priority:** High
**Category:** Identity Architecture
**Estimated Effort:** Small
**Dependencies:** TASK-047-03
**Status:** **In Progress** (2026-03-27)

---

## Overview

Define the caller-side onboarding flow.

Recommended caller pattern:

- one client app registration or managed identity per calling service
- one or more federated identity credentials on that caller identity, matching the external workload issuer/subject/audience
- assign the router API app role to that caller identity
- the caller requests an access token for the router API audience

Operational note:

- app roles are the recommended authorization layer for app-only service callers
- ACL-by-client-ID can exist as an escape hatch, but it should not be the primary model

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-047-03-02-caller-app-registration-federated-credential-pattern-and-role-assignment-flow.md`
