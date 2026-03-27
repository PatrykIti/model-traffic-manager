[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-004-02-02: Settings, Container, Logging, and Lifespan Shell
# FileName: TASK-004-02-02-settings-container-logging-and-lifespan-shell.md

**Priority:** High
**Category:** Runtime Bootstrap
**Estimated Effort:** Medium
**Dependencies:** TASK-004-02
**Status:** **Done** (2026-03-13)

---

## Overview

Own the runtime wiring that future use cases and adapters will rely on.

This work item creates:
- configuration/settings loading shell
- bootstrap container shell
- structured logging shell
- app lifespan shell for startup/shutdown orchestration

---

## Target Files

```text
app/infrastructure/config/settings.py
app/infrastructure/bootstrap/container.py
app/infrastructure/observability/logging.py
```

---

## Pseudocode

```text
load_settings():
    read environment variables
    apply defaults safe for local bootstrap
    return typed settings object

build_container(settings):
    return lightweight container object with settings and placeholder services

configure_logging(settings):
    initialize structlog/logging defaults for local and CI runs
```

---

## Detailed Work Items

1. Define a typed settings object with fields required for bootstrap only.
2. Create a lightweight container or composition root, not a service locator maze.
3. Configure structured logging with a simple local-friendly output.
4. Expose startup/shutdown hooks that can later load config and initialize infrastructure safely.

---

## Testing Requirements

- settings can be loaded with defaults in local test runs
- container wiring works without Redis or external providers
- logging setup does not crash app startup

---

## Documentation Updates Required

- `docs/architecture/README.md`
- `docs/operations/README.md`
- `_docs/_TASKS/TASK-004-02-02-settings-container-logging-and-lifespan-shell.md`
