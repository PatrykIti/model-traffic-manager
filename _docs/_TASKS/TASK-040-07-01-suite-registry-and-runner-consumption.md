[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-040-07](./TASK-040-07-workflow-and-runner-contract-registry-normalization.md)

# TASK-040-07-01: Suite Registry and Runner Consumption
# FileName: TASK-040-07-01-suite-registry-and-runner-consumption.md

**Priority:** High
**Category:** Workflow Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-040-07
**Status:** **Done** (2026-03-20)

---

## Overview

Introduce the canonical validation suite registry and make the shared Azure/AKS runner consume it instead of a hardcoded suite matrix.

## Documentation Updates Required

- `scripts/release/validation_suite_registry.py`
- `scripts/release/run_azure_test_suite.sh`
