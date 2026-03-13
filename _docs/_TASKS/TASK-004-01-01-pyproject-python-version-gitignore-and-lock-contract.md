[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-004-01-01: `pyproject.toml`, `.python-version`, `.gitignore`, and Lock Contract
# FileName: TASK-004-01-01-pyproject-python-version-gitignore-and-lock-contract.md

**Priority:** High
**Category:** Runtime Bootstrap
**Estimated Effort:** Medium
**Dependencies:** TASK-004-01
**Status:** **Done** (2026-03-13)

---

## Overview

Define the precise repository contract for Python runtime, dependencies, developer tooling, and ignore policy.

This work item owns:
- `pyproject.toml`
- `uv.lock`
- `.python-version`
- `.gitignore`

---

## Target Files

```text
pyproject.toml
uv.lock
.python-version
.gitignore
```

---

## Pseudocode

```text
define_project_contract():
    set project metadata
    require Python 3.12.x
    pin all direct runtime and dev dependencies exactly
    configure ruff, mypy, pytest, and pytest-cov
    generate uv.lock
    ignore virtualenvs, caches, coverage, and local runtime artifacts
```

---

## Detailed Work Items

1. Create `pyproject.toml` with:
   - project name, version, description
   - exact runtime dependency pins from `_docs/_MVP/STACK.md`
   - exact dev dependency pins
   - tool sections for `ruff`, `mypy`, and `pytest`
2. Create `.python-version` pinned to `3.12.x` target.
3. Create `.gitignore` for:
   - `.venv/`
   - `__pycache__/`
   - `.mypy_cache/`
   - `.pytest_cache/`
   - coverage outputs
   - local env/config artifacts that should not be committed
4. Generate `uv.lock` and commit it together with `pyproject.toml`.

---

## Testing Requirements

- `uv lock` succeeds
- tool configuration is accepted by `uv run ruff --version`, `uv run mypy --version`, and `uv run pytest --version`
- no dependency range violates the exact pinning rule

---

## Documentation Updates Required

- `README.md`
- `CONTRIBUTING.md`
- `_docs/_TASKS/TASK-004-01-01-pyproject-python-version-gitignore-and-lock-contract.md`
- future changelog entry for bootstrap implementation
