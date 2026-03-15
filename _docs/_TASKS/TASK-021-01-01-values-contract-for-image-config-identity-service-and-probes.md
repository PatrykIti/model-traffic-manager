[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-021-01-01: Values Contract for Image, Config, Identity, Service, and Probes
# FileName: TASK-021-01-01-values-contract-for-image-config-identity-service-and-probes.md

**Priority:** High
**Category:** Packaging
**Estimated Effort:** Small
**Dependencies:** TASK-021-01
**Status:** **To Do**

---

## Overview

Define the values keys for image source, router config delivery, service account
and Workload Identity wiring, service exposure, and probe configuration.

## Testing Requirements

- values remain explicit and environment-readable
- the chart can render both the smoke and live-model AKS variants without
  template duplication

## Documentation Updates Required

- `_docs/_TASKS/TASK-021-01-01-values-contract-for-image-config-identity-service-and-probes.md`
