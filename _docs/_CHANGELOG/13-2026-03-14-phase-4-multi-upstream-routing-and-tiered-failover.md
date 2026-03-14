[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# Filename: 13-2026-03-14-phase-4-multi-upstream-routing-and-tiered-failover.md

# 13. Phase 4 Multi-Upstream Routing and Tiered Failover

**Date:** 2026-03-14
**Version:** 0.1.0
**Tasks:** TASK-013, TASK-013-01, TASK-013-01-01, TASK-013-01-02, TASK-013-02, TASK-013-02-01, TASK-013-02-02, TASK-013-03

## Key Changes

### Routing policy
- Added a domain-level `tiered_failover` selector with deterministic weighted round robin inside the selected tier.
- Added request-level candidate exclusion so retries can move to the next eligible upstream in the same or higher tier.
- Added route-selection reasons that preserve explainable routing context for later observability work.

### Use-case orchestration
- Updated chat completions and embeddings use cases to honor `max_attempts` and configured retryable status codes.
- Added failover on retriable transport failures and retriable upstream status codes while preserving non-retriable passthrough behavior.
- Wired the selector into the bootstrap container so both current proxy paths use the same routing policy.

### Testing and documentation
- Added unit coverage for the selector, weighted round robin behavior, and failover orchestration in both use cases.
- Added `integration-local` coverage for same-tier and cross-tier failover at the API level.
- Updated repository and official routing docs to reflect that tiered multi-upstream failover is now implemented.
