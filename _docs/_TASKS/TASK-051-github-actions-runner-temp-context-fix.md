[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-051: GitHub Actions `runner.temp` Context Fix
# FileName: TASK-051-github-actions-runner-temp-context-fix.md

**Priority:** Medium
**Category:** Workflow Reliability
**Estimated Effort:** Small
**Dependencies:** TASK-040, TASK-041
**Status:** **Done** (2026-03-27)

---

## Overview

Fix workflow validation failures caused by referencing the `runner` context in job-level `env` blocks where that context is not accepted by the GitHub Actions workflow parser.

The release-validation and nightly-validation workflows already upload artifacts from `runner.temp`, and the shared shell runner already falls back to `RUNNER_TEMP` automatically. The fix is therefore to remove the invalid job-level expression rather than introducing new workflow complexity.

---

## Testing Requirements

- affected workflow files pass repository guardrails
- the shell runner still resolves the artifact root through `RUNNER_TEMP` on GitHub-hosted runners

---

## Documentation Updates Required

- `.github/workflows/validation-nightly.yml`
- `.github/workflows/release-validation.yml`
- `_docs/_TASKS/TASK-051-github-actions-runner-temp-context-fix.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/README.md`
