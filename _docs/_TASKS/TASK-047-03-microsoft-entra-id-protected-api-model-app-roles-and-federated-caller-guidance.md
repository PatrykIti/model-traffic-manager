[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-047](./TASK-047-inbound-client-auth-with-api-bearer-tokens-and-microsoft-entra-id.md)

# TASK-047-03: Microsoft Entra ID Protected-API Model, App Roles, and Federated Caller Guidance
# FileName: TASK-047-03-microsoft-entra-id-protected-api-model-app-roles-and-federated-caller-guidance.md

**Priority:** High
**Category:** Identity Architecture
**Estimated Effort:** Medium
**Dependencies:** TASK-047-01
**Status:** To Do

---

## Overview

Define the Microsoft Entra ID app-registration model for inbound router authentication.

Recommended architecture:

- one router API app registration that represents `model-traffic-manager` as the protected resource
- one Application ID URI or API audience owned by that router API app
- app roles exposed by the router API app for app-only callers
- one client app registration or managed identity per calling service
- one federated credential per external workload identity pattern on the client side

Important clarification:

- the router API app is the audience
- the per-service caller app is the client identity
- app roles belong on the router API app and are assigned to the calling client apps or service principals

---

## Sub-Tasks

### TASK-047-03-01: Router API app registration, Application ID URI, and app-role design

**Status:** To Do

Define how the router is represented as a protected API in Entra ID.

### TASK-047-03-02: Caller app registration, federated credential pattern, and role-assignment flow

**Status:** To Do

Define how each calling service gets an app-only token for the router without client secrets.

---

## Testing Requirements

- documentation and examples must distinguish delegated scopes from app roles clearly
- authorization design should make least-privilege caller onboarding possible

---

## Documentation Updates Required

- `docs/configuration/auth-and-identity.md`
- `_docs/_TASKS/TASK-047-03-microsoft-entra-id-protected-api-model-app-roles-and-federated-caller-guidance.md`
- `_docs/_TASKS/TASK-047-03-01-router-api-app-registration-application-id-uri-and-app-role-design.md`
- `_docs/_TASKS/TASK-047-03-02-caller-app-registration-federated-credential-pattern-and-role-assignment-flow.md`
