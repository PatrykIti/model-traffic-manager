[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-040-03](./TASK-040-03-resource-lifecycle-ttl-and-cleanup-hardening.md)

# TASK-040-03-02: Runner Cleanup Report and Resource Markers
# FileName: TASK-040-03-02-runner-cleanup-report-and-resource-markers.md

**Priority:** High
**Category:** Reliability Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-040-03-01
**Status:** **Done** (2026-03-20)

---

## Overview

Add explicit cleanup reporting for federated credentials, namespaces, image-pull secrets, and port-forward teardown.

## Documentation Updates Required

- `scripts/release/run_azure_test_suite.sh`
