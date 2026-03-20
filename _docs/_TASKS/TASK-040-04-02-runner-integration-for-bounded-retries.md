[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-040-04](./TASK-040-04-retry-and-resilience-policy-for-runner-side-external-operations.md)

# TASK-040-04-02: Runner Integration for Bounded Retries
# FileName: TASK-040-04-02-runner-integration-for-bounded-retries.md

**Priority:** High
**Category:** Reliability Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-040-04-01
**Status:** **Done** (2026-03-20)

---

## Overview

Integrate bounded retries into the shared Azure/AKS runner for transient GHCR, Azure control-plane, Kubernetes watch, Terraform apply, and port-forward startup failures.

## Documentation Updates Required

- `scripts/release/run_azure_test_suite.sh`
