[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-023](./TASK-023-shared-services-access-model-and-router-execution-surface.md)

# TASK-023-01: Shared-Service Taxonomy, Routing Profiles, and Failover Policy Split
# FileName: TASK-023-01-shared-service-taxonomy-routing-profiles-and-failover-policy-split.md

**Priority:** High
**Category:** Architecture Planning
**Estimated Effort:** Medium
**Dependencies:** TASK-023
**Status:** **Done** (2026-03-15)

---

## Overview

Define a small set of shared-service execution profiles instead of reusing the LLM routing model blindly.

Target outcome:
- `provider_managed`
  services with a single semantic endpoint and provider-managed availability; router failover is not used
- `single_endpoint`
  router-managed HTTP execution with auth/observability, but no multi-upstream failover
- `tiered_failover`
  router-managed multi-upstream execution for stateless HTTP services where explicit failover is required
- `direct_backend_access`
  services intentionally not proxied through the router; router may expose metadata only

Design rule:
- Azure Storage with RA-GRS or equivalent provider-managed redundancy should default to `provider_managed` or `direct_backend_access`, not `tiered_failover`

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-023-01-shared-service-taxonomy-routing-profiles-and-failover-policy-split.md`
