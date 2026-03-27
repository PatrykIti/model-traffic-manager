[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 47: Expanded Live Validation Workflow Rollout

**Date:** 2026-03-18
**Version:** 0.1.0
**Tasks:**
- TASK-029-07
- TASK-029-07-01
- TASK-029-07-02
- TASK-029-07-03

---

## Key Changes

### Workflow Rollout

- refactored the Azure-backed workflows to select validation profiles through `suite` inputs
- aligned workflow execution with the repository runner script instead of maintaining duplicated per-profile logic

### Documentation

- updated official testing docs and local-development guidance for the final expanded validation matrix
- clarified that the same suite names now exist consistently across `make` targets and GitHub workflow inputs

### Process Closure

- closed the validation-expansion package in the task board and changelog after the full matrix rollout
