[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-047-03](./TASK-047-03-microsoft-entra-id-protected-api-model-app-roles-and-federated-caller-guidance.md)

# TASK-047-03-01: Router API App Registration, Application ID URI, and App-Role Design
# FileName: TASK-047-03-01-router-api-app-registration-application-id-uri-and-app-role-design.md

**Priority:** High
**Category:** Identity Architecture
**Estimated Effort:** Small
**Dependencies:** TASK-047-03
**Status:** **Done** (2026-03-27)

---

## Overview

Define the protected-API side of the Entra model.

Design points:

- choose one stable Application ID URI for the router API
- expose app roles for machine callers, for example `invoke.router`
- if delegated user flows are ever needed later, scopes can be added separately; they should not replace app roles for daemon callers
- ensure audience validation uses the router API app identity, not the caller app identity

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-047-03-01-router-api-app-registration-application-id-uri-and-app-role-design.md`
