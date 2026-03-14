[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-012-03: Documentation, Security Contract, and Operations Guidance
# FileName: TASK-012-03-documentation-security-contract-and-operations-guidance.md

**Priority:** High
**Category:** Documentation and Security
**Estimated Effort:** Small
**Dependencies:** TASK-012
**Status:** **To Do**

---

## Overview

Document how Managed Identity works in the router and how operators should reason about it.

Detailed work:
1. Update the official configuration and deployment docs.
2. Clarify the separation between router outbound auth and future client auth.
3. Add operational notes around scope selection, optional client IDs, and token caching.

---

## Testing Requirements

- the official docs explain the new auth mode without implying client-token forwarding
- operational guidance stays aligned with the actual runtime cache and credential behavior
- security-sensitive wording avoids suggesting secret storage where it is not needed

---

## Documentation Updates Required

- `docs/configuration/deployment-and-upstreams.md`
- `docs/operations/deployment-model.md`
- `docs/getting-started/implementation-status.md`
- `_docs/_TASKS/TASK-012-03-documentation-security-contract-and-operations-guidance.md`
