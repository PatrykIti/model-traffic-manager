[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-028: Explicit Cooldown State Semantics and Observability
# FileName: TASK-028-explicit-cooldown-state-semantics-and-observability.md

**Priority:** High
**Category:** Domain and Observability Hardening
**Estimated Effort:** Small
**Dependencies:** TASK-014, TASK-021
**Status:** **Done** (2026-03-16)

---

## Overview

Make `cooldown` a real operational state instead of only an implicit behavior attached to other temporary states.

Business goal:
- separate the reason for temporary exclusion from the temporary exclusion state itself
- make operator diagnostics clearer when an upstream is intentionally cooled down
- keep the runtime behavior aligned with the MVP routing model

---

## Sub-Tasks

### TASK-028-01: Cooldown state transitions, routing reasons, and docs alignment

**Status:** Done (2026-03-16)

Implement explicit cooldown transitions in domain policy and selector behavior, then align tests and official docs.

---

## Testing Requirements

- rate-limited and below-threshold unhealthy failures enter explicit `cooldown`
- selector rejection reasons distinguish cooldown from other blocked states
- legacy temporary states normalize cleanly into cooldown behavior
- `uv run ruff check .`
- `uv run mypy app`
- `PYTHONPATH=. uv run pytest tests/unit tests/integration/api -q`

---

## Documentation Updates Required

- `docs/routing/failover-and-health.md`
- `docs/reference/decision-reasons.md`
- `docs/getting-started/implementation-status.md`
- `_docs/_TASKS/TASK-028-explicit-cooldown-state-semantics-and-observability.md`
- `_docs/_TASKS/TASK-028-01-cooldown-state-transitions-routing-reasons-and-docs-alignment.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/README.md`
