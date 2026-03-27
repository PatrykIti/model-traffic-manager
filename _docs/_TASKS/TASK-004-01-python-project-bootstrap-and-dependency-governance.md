[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-004-01: Python Project Bootstrap and Dependency Governance
# FileName: TASK-004-01-python-project-bootstrap-and-dependency-governance.md

**Priority:** High
**Category:** Runtime Bootstrap
**Estimated Effort:** Medium
**Dependencies:** TASK-004
**Status:** **Done** (2026-03-13)

---

## Overview

Create the repository contract that makes the project a real Python application rather than a documentation-only repository.

Scope:
- define project metadata and exact dependency pins
- create Python version and ignore policies
- create the initial package tree for `app/`, `tests/`, `configs/`, and `docker/`

---

## Architecture

Primary outputs:

```text
pyproject.toml
uv.lock
.python-version
.gitignore
app/
tests/
configs/
docker/
```

---

## Sub-Tasks

### TASK-004-01-01: `pyproject.toml`, `.python-version`, `.gitignore`, and lock contract

**Status:** Done (2026-03-13)

Define the exact runtime and developer dependency contract for the repository.

### TASK-004-01-02: Base application, tests, config, and docker directory layout

**Status:** Done (2026-03-13)

Create the directory skeleton that future tasks will implement inside.

---

## Pseudocode

```text
bootstrap_python_project():
    write pyproject metadata and exact direct dependencies
    pin Python version
    define tool configuration for ruff, mypy, pytest
    create repository ignore policy
    create the base runtime and tests package layout
```

---

## Implementation Checklist

| Area | Files / Paths | Purpose |
|------|---------------|---------|
| Project metadata | `pyproject.toml` | Project identity, exact pins, tool configuration |
| Locking | `uv.lock` | Reproducible dependency tree |
| Python version | `.python-version` | Local and CI version alignment |
| Ignore rules | `.gitignore` | Prevent env/cache/build noise |
| Runtime layout | `app/...` | Clean Architecture skeleton |
| Test layout | `tests/...` | Unit and integration test roots |
| Bootstrap assets roots | `configs/`, `docker/` | Future configuration and container assets |

---

## Testing Requirements

- `uv` can resolve and lock the chosen dependencies
- tool configuration parses correctly for `ruff`, `mypy`, and `pytest`
- the directory structure matches the intended Clean Architecture split

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-004-01-python-project-bootstrap-and-dependency-governance.md`
- `_docs/_TASKS/TASK-004-01-01-pyproject-python-version-gitignore-and-lock-contract.md`
- `_docs/_TASKS/TASK-004-01-02-base-application-tests-config-and-docker-layout.md`
- `_docs/_CHANGELOG/README.md`
