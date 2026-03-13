[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-004-02-01: API Entrypoint, Health Routes, and Error Shell
# FileName: TASK-004-02-01-api-entrypoint-health-routes-and-error-shell.md

**Priority:** High
**Category:** Runtime Bootstrap
**Estimated Effort:** Medium
**Dependencies:** TASK-004-02
**Status:** **Done** (2026-03-13)

---

## Overview

Own the public HTTP shell for the initial bootstrap.

Target behavior:
- the service starts
- `/health/live` answers liveness
- `/health/ready` answers readiness
- the app has a stable place for future exception-to-HTTP mapping

---

## Target Files

```text
app/entrypoints/api/main.py
app/entrypoints/api/routes_health.py
app/entrypoints/api/error_handlers.py
```

---

## Pseudocode

```text
routes_health:
    GET /health/live -> {"status": "ok", "kind": "live"}
    GET /health/ready -> {"status": "ok", "kind": "ready"}

main:
    app = FastAPI(...)
    include health router
    install error handlers
```

---

## Detailed Work Items

1. Create a FastAPI app factory or top-level app object.
2. Create dedicated health route module instead of putting everything in `main.py`.
3. Create an error handler module even if the first version only registers a minimal shell.
4. Reserve URL and module conventions that match the target architecture.

---

## Testing Requirements

- liveness endpoint returns `200`
- readiness endpoint returns `200`
- app module imports without side effects that require real infrastructure

---

## Documentation Updates Required

- `docs/getting-started/README.md`
- `docs/operations/README.md`
- `_docs/_TASKS/TASK-004-02-01-api-entrypoint-health-routes-and-error-shell.md`
