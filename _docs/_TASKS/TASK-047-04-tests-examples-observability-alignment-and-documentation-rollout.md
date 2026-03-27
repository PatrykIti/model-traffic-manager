[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-047](./TASK-047-inbound-client-auth-with-api-bearer-tokens-and-microsoft-entra-id.md)

# TASK-047-04: Tests, Examples, Observability Alignment, and Documentation Rollout
# FileName: TASK-047-04-tests-examples-observability-alignment-and-documentation-rollout.md

**Priority:** High
**Category:** Validation and Documentation
**Estimated Effort:** Medium
**Dependencies:** TASK-047-01, TASK-047-02, TASK-047-03
**Status:** To Do

---

## Overview

Close inbound auth with examples, tests, and documentation.

Detailed work:

1. add example router configs for bearer-token and Entra inbound auth
2. add unit and integration coverage for both modes
3. update observability docs so caller metadata appears safely in diagnostics
4. document token rotation, app-role assignment, and federated-credential onboarding

---

## Testing Requirements

- route endpoints reject unauthenticated and unauthorized callers correctly
- examples stay aligned with the validated config contract

---

## Documentation Updates Required

- `docs/getting-started/implementation-status.md`
- `docs/operations/observability-and-health.md`
- `_docs/_TASKS/TASK-047-04-tests-examples-observability-alignment-and-documentation-rollout.md`
- `_docs/_TASKS/README.md`
