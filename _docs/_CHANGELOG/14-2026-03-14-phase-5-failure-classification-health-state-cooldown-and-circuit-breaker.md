[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# Filename: 14-2026-03-14-phase-5-failure-classification-health-state-cooldown-and-circuit-breaker.md

# 14. Phase 5 Failure Classification, Health State, Cooldown, and Circuit Breaker

**Date:** 2026-03-14
**Version:** 0.1.0
**Tasks:** TASK-014, TASK-014-01, TASK-014-01-01, TASK-014-01-02, TASK-014-02, TASK-014-02-01, TASK-014-02-02, TASK-014-03, TASK-014-04

## Key Changes

### Failure classification and health state
- Added a repository-owned failure classification model for transport errors, retriable upstream failures, quota exhaustion, and non-retriable responses.
- Added a health-state policy covering cooldown after `429`, temporary unhealthy state after retriable failures, and per-upstream circuit-open transitions after repeated failures.
- Extended the health-state model with cooldown and circuit deadlines plus the last recorded failure reason.

### Persistence and routing integration
- Added an in-memory health-state repository as the default runtime implementation.
- Added a Redis-backed health-state adapter behind the repository port.
- Integrated health-state loading, state updates, and unavailable-upstream filtering into chat completions and embeddings routing.

### Testing and documentation
- Added unit coverage for failure classification, health-state policy transitions, and both health-state repositories.
- Added `integration-local` coverage for cooldown and circuit-open behavior through the API.
- Updated official docs and tracking to reflect that health-state persistence, cooldown, and circuit breaker behavior are now implemented.
