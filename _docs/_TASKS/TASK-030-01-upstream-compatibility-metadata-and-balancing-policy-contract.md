[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-030](./TASK-030-model-aware-load-balancing-within-tier.md)

# TASK-030-01: Upstream Compatibility Metadata and Balancing Policy Contract
# FileName: TASK-030-01-upstream-compatibility-metadata-and-balancing-policy-contract.md

**Priority:** High
**Category:** Domain and Configuration Planning
**Estimated Effort:** Medium
**Dependencies:** TASK-030
**Status:** **To Do**

---

## Overview

Define the config and domain metadata that lets the router decide whether same-tier upstreams are safe to balance together.

Recommended minimum:
- `compatibility_group`
- `model_name`
- `model_version`
- optional `deployment_name`

Recommended behavior:
- if compatibility metadata is absent, keep current behavior only where the operator has explicitly chosen to allow balancing
- otherwise fail closed for ambiguous multi-model pools

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-030-01-upstream-compatibility-metadata-and-balancing-policy-contract.md`
