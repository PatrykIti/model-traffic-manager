[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-005-03: Deployment Listing Use Case and API Surface
# FileName: TASK-005-03-deployment-listing-use-case-and-api-surface.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-005-02
**Status:** **Done** (2026-03-13)

---

## Overview

Implement the first real use case and expose it through the API.

Scope:
- deployment repository port
- deployment summary DTO
- deployment listing use case
- `/deployments` route
- unit and integration coverage

---

## Sub-Tasks

### TASK-005-03-01: Application port, DTO, and use case

**Status:** Done (2026-03-13)

Create the application contract for listing deployments.

### TASK-005-03-02: Deployment route and integration coverage

**Status:** Done (2026-03-13)

Expose the use case through the API and prove it through tests.

---

## Testing Requirements

- listing use case returns deterministic deployment summaries
- API route returns deployments from validated config
- API response shape stays stable and explicit

---

## Documentation Updates Required

- `docs/getting-started/implementation-status.md`
- `docs/configuration/deployment-and-upstreams.md`
- `_docs/_TASKS/TASK-005-03-deployment-listing-use-case-and-api-surface.md`
- `_docs/_TASKS/TASK-005-03-01-application-port-dto-and-use-case.md`
- `_docs/_TASKS/TASK-005-03-02-deployment-route-and-integration-coverage.md`
