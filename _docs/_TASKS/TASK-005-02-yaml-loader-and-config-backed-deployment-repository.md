[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-005-02: YAML Loader and Config-Backed Deployment Repository
# FileName: TASK-005-02-yaml-loader-and-config-backed-deployment-repository.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-005-01
**Status:** **Done** (2026-03-13)

---

## Overview

Load the YAML file at startup, validate it, and expose deployments through a repository contract.

This work item owns:
- YAML parsing
- conversion into typed config model
- repository implementation backed by validated config
- container/runtime wiring updates

---

## Target Files

```text
app/application/ports/deployment_repository.py
app/infrastructure/config/yaml_loader.py
app/infrastructure/config/deployment_repository.py
app/infrastructure/bootstrap/container.py
app/entrypoints/api/main.py
```

---

## Pseudocode

```text
startup():
    raw_yaml = read config file
    router_config = validate raw_yaml
    deployment_repository = build repository from validated deployments
    store both in container
```

---

## Testing Requirements

- startup fails on invalid YAML/config
- the repository returns deployments from validated config
- the application container exposes validated config and the repository

---

## Documentation Updates Required

- `docs/architecture/system-overview.md`
- `docs/configuration/configuration-model.md`
- `_docs/_TASKS/TASK-005-02-yaml-loader-and-config-backed-deployment-repository.md`
