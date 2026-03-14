[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-019-01-02: Apply-Test-Destroy Wrapper for `integration-azure`
# FileName: TASK-019-01-02-apply-test-destroy-wrapper-for-integration-azure.md

**Priority:** High
**Category:** Developer Workflow
**Estimated Effort:** Small
**Dependencies:** TASK-019-01
**Status:** **Done** (2026-03-14)

---

## Overview

Wrap local `integration-azure` execution into one command with guaranteed cleanup.

---

## Testing Requirements

- the wrapper performs `terraform apply`, runs the test suite, and always attempts `terraform destroy`
- test failure must not skip cleanup

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-019-01-02-apply-test-destroy-wrapper-for-integration-azure.md`
