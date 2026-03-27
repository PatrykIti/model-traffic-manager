[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-024](./TASK-024-shared-services-execution-model-and-backend-facing-proxy-surface.md)

# TASK-024-01: Shared-Service Config and Domain Contract for Execution Modes
# FileName: TASK-024-01-shared-service-config-and-domain-contract-for-execution-modes.md

**Priority:** High
**Category:** Domain and Configuration Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-024
**Status:** **Done** (2026-03-15)

---

## Overview

Encode shared-service execution policy directly in the YAML and domain model.

Required capabilities:
- `registry_only`
- `router_proxy` with `provider_managed`
- `router_proxy` with `single_endpoint`
- `router_proxy` with `tiered_failover`

The contract must reject impossible combinations and keep LLM-specific concepts out of shared-service definitions.

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-024-01-shared-service-config-and-domain-contract-for-execution-modes.md`
