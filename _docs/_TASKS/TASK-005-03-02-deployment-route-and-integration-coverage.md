[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-005-03-02: Deployment Route and Integration Coverage
# FileName: TASK-005-03-02-deployment-route-and-integration-coverage.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-005-03
**Status:** **Done** (2026-03-13)

---

## Overview

Expose the deployment registry through the API and prove the runtime behavior with tests.

This work item owns:
- `app/entrypoints/api/routes_deployments.py`
- integration coverage for `/deployments`
- startup path updates required to wire the use case into the app state/container

---

## Pseudocode

```text
GET /deployments:
    resolve list_deployments use case from container
    execute use case
    return deployment summaries
```

---

## Testing Requirements

- integration test covers `/deployments`
- endpoint returns the validated config content, not hand-built fixtures disconnected from startup
- response shape is deterministic and documented

---

## Documentation Updates Required

- `docs/getting-started/implementation-status.md`
- `docs/configuration/deployment-and-upstreams.md`
- `_docs/_TASKS/TASK-005-03-02-deployment-route-and-integration-coverage.md`
