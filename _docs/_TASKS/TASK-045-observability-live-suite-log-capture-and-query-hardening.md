[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-045: Observability Live Suite Log Capture and Query Hardening
# FileName: TASK-045-observability-live-suite-log-capture-and-query-hardening.md

**Priority:** High
**Category:** Validation Reliability
**Estimated Effort:** Small
**Dependencies:** TASK-044
**Status:** **Done** (2026-03-26)

---

## Overview

Harden the new live observability suite after the first real run exposed two operator-facing problems:

- console output was too noisy and truncated, making post-failure diagnosis slow
- the first Application Insights query path was too narrow and the startup-log assertion relied on a short log tail

Result:

- make-driven and suite-driven test runs now persist fuller logs to files
- the observability suite now uses a more robust request-flow query strategy and startup-log capture

---

## Testing Requirements

- `uv run ruff check .`
- `uv run mypy app`
- `bash -n scripts/release/run_azure_test_suite.sh`
- `uv run pytest --cov=app --cov-report=term-missing --cov-fail-under=85`
- `uv run pre-commit run --all-files`

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-045-observability-live-suite-log-capture-and-query-hardening.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/62-2026-03-26-observability-live-suite-log-capture-and-query-hardening.md`
- `_docs/_CHANGELOG/README.md`
