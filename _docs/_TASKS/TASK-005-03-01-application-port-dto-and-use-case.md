[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-005-03-01: Application Port, DTO, and Use Case
# FileName: TASK-005-03-01-application-port-dto-and-use-case.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-005-03
**Status:** **Done** (2026-03-13)

---

## Overview

Create the application layer contract for deployment listing.

This work item owns:
- deployment repository port
- deployment summary DTO
- `ListDeployments` use case

---

## Target Files

```text
app/application/ports/deployment_repository.py
app/application/dto/deployment_summary.py
app/application/use_cases/list_deployments.py
```

---

## Testing Requirements

- the use case depends only on the repository port
- unit tests use fakes or stubs, not framework-specific mocks
- returned summaries reflect upstream/provider/region information

---

## Documentation Updates Required

- `docs/architecture/request-lifecycle.md`
- `_docs/_TASKS/TASK-005-03-01-application-port-dto-and-use-case.md`
