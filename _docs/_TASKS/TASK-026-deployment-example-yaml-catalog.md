[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-026: Deployment Example YAML Catalog
# FileName: TASK-026-deployment-example-yaml-catalog.md

**Priority:** High
**Category:** Documentation and Runtime Examples
**Estimated Effort:** Small
**Dependencies:** TASK-021, TASK-024
**Status:** **Done** (2026-03-15)

---

## Overview

Add real example router YAML files that demonstrate the main upstream and failover patterns for LLM and embeddings deployments.

Business goal:
- provide copyable deployment examples for future backend and platform work
- show how tiered upstreams can express regional failover, model fallback, and embeddings routing
- keep the official docs linked to real versioned example files

---

## Sub-Tasks

### TASK-026-01: Official deployment example router configs

**Status:** Done (2026-03-15)

Add versioned example router YAML files for regional chat failover, model-level fallback, and embeddings failover.

---

## Testing Requirements

- YAML examples stay valid against the current deployment config contract
- official docs link to the real example files

---

## Documentation Updates Required

- `docs/configuration/deployment-and-upstreams.md`
- `configs/examples/deployments-chat-regional-failover.router.yaml`
- `configs/examples/deployments-chat-model-fallback.router.yaml`
- `configs/examples/deployments-embeddings-regional-failover.router.yaml`
- `_docs/_TASKS/TASK-026-deployment-example-yaml-catalog.md`
- `_docs/_TASKS/TASK-026-01-official-deployment-example-router-configs.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/README.md`
