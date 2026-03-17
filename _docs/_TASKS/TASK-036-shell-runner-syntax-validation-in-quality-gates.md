[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-036: Shell Runner Syntax Validation in Quality Gates
# FileName: TASK-036-shell-runner-syntax-validation-in-quality-gates.md

**Priority:** High
**Category:** Developer Workflow and Hardening
**Estimated Effort:** Small
**Dependencies:** TASK-019, TASK-033, TASK-034, TASK-035
**Status:** **Done** (2026-03-17)

---

## Overview

Add automatic shell-syntax validation for repository-managed `.sh` files and simplify fragile runner syntax.

Business goal:
- catch shell syntax problems before a long Azure/AKS run provisions infrastructure
- keep `make check`, `make release-check`, and pre-commit aligned on shell-script validation
- remove fragile nested shell expansion from the Azure/AKS runner

---

## Sub-Tasks

- add a `validate-shell` target to the main `Makefile`
- include shell validation in the shared quality gate used by pre-commit
- simplify GHCR credential resolution in the AKS runner script
- update operator-facing docs so the stronger release gate is visible

---

## Testing Requirements

- `make -n validate-shell check release-check` shows shell validation in the command graph
- `bash -n docker/entrypoint.sh`
- `bash -n scripts/release/run_azure_test_suite.sh`

---

## Documentation Updates Required

- `Makefile`
- `scripts/pre_commit/run_repo_quality_gate.py`
- `scripts/release/run_azure_test_suite.sh`
- `README.md`
- `docs/getting-started/local-development.md`
- `_docs/_TASKS/TASK-036-shell-runner-syntax-validation-in-quality-gates.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/41-2026-03-17-shell-runner-syntax-validation-in-quality-gates.md`
- `_docs/_CHANGELOG/README.md`
