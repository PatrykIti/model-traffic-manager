[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-021](./TASK-021-mvp-closure-runtime-state-activation-and-contract-hardening.md)

# TASK-021-02: Half-Open Circuit Recovery and Health-State Transition Hardening
# FileName: TASK-021-02-half-open-circuit-recovery-and-health-state-transition-hardening.md

**Priority:** High
**Category:** Domain and Application Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-021, TASK-014
**Status:** **Done** (2026-03-15)

---

## Overview

The current circuit-breaker behavior re-enters traffic as fully healthy after the open window expires. The MVP requires a real half-open recovery phase with a single probe request.

Detailed work:
1. Introduce an explicit half-open recovery state or equivalent guarded runtime behavior.
2. Allow only one probe request after `half_open_after_seconds`.
3. Close the circuit on probe success.
4. Re-open the circuit on probe failure with a deterministic follow-up window.
5. Keep routing deterministic when healthy and half-open candidates coexist.

---

## Testing Requirements

- unit tests for state normalization into half-open recovery
- unit tests for probe success and probe failure transitions
- routing tests that prefer healthy peers over half-open candidates
- request-orchestration tests that allow only one probe attempt at a time

---

## Documentation Updates Required

- `docs/routing/failover-and-health.md`
- `docs/reference/decision-reasons.md`
- `docs/getting-started/implementation-status.md`
- `_docs/_TASKS/TASK-021-02-half-open-circuit-recovery-and-health-state-transition-hardening.md`
