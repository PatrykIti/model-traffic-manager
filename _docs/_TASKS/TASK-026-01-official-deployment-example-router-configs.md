[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-026](./TASK-026-deployment-example-yaml-catalog.md)

# TASK-026-01: Official Deployment Example Router Configs
# FileName: TASK-026-01-official-deployment-example-router-configs.md

**Priority:** High
**Category:** Documentation Implementation
**Estimated Effort:** Small
**Dependencies:** TASK-026
**Status:** **Done** (2026-03-15)

---

## Overview

Publish three example router configs that show the currently supported deployment patterns for model traffic:

1. chat with regional failover
2. chat with model-level fallback across tiers
3. embeddings with regional failover

The examples should be full router configs so they can be copied and adapted directly.

---

## Documentation Updates Required

- `docs/configuration/deployment-and-upstreams.md`
- `configs/examples/deployments-chat-regional-failover.router.yaml`
- `configs/examples/deployments-chat-model-fallback.router.yaml`
- `configs/examples/deployments-embeddings-regional-failover.router.yaml`
- `_docs/_TASKS/TASK-026-01-official-deployment-example-router-configs.md`
