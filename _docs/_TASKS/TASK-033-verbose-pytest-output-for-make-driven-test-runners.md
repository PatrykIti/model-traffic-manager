[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-033: Verbose Pytest Output for Make-Driven Test Runners
# FileName: TASK-033-verbose-pytest-output-for-make-driven-test-runners.md

**Priority:** Medium
**Category:** Developer Workflow
**Estimated Effort:** Small
**Dependencies:** TASK-019, TASK-029, TASK-030
**Status:** **Done** (2026-03-17)

---

## Overview

Make every current `make` target that runs pytest print clearer test execution output.

Business goal:
- show exactly which test is running in local and Azure-backed workflows
- make `make` output more useful when validating router behavior live on Azure and AKS
- keep the reporting format consistent across local smoke, local coverage runs, and higher-level infra runners

---

## Sub-Tasks

- add one shared verbose pytest flag set for direct `make` targets
- make the Azure/AKS wrapper announce the pytest flags it uses and print per-test names
- document the behavior so operators know what to expect from local runner output

---

## Testing Requirements

- `make -n test` and `make -n smoke` show verbose pytest flags
- the Azure/AKS runner shell script remains syntactically valid

---

## Documentation Updates Required

- `Makefile`
- `scripts/release/run_azure_test_suite.sh`
- `docs/getting-started/local-development.md`
- `_docs/_TASKS/TASK-033-verbose-pytest-output-for-make-driven-test-runners.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/38-2026-03-17-verbose-pytest-output-for-make-driven-test-runners.md`
- `_docs/_CHANGELOG/README.md`
