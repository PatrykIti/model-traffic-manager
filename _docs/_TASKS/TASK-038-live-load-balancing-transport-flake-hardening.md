[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-038: Live Load-Balancing Transport Flake Hardening
# FileName: TASK-038-live-load-balancing-transport-flake-hardening.md

**Priority:** High
**Category:** Validation and Test Hardening
**Estimated Effort:** Small
**Dependencies:** TASK-030, TASK-035
**Status:** **Done** (2026-03-18)

---

## Overview

Harden the dedicated live load-balancing AKS suite against transient local transport failures without weakening the behavioral assertions.

Business goal:
- stop `ReadTimeout`, `ReadError`, and `ConnectError` from failing the whole suite when the router pod itself is healthy
- keep deterministic same-tier distribution assertions meaningful
- retry transient local transport failures while still requiring clean 8/2 active-active observation windows

---

## Sub-Tasks

- add request retry handling for transient `httpx.TransportError` failures
- restart active-active measurement windows when transport retries occurred
- keep the active-standby and failover assertions unchanged apart from transport resilience

---

## Testing Requirements

- `uv run ruff check tests/e2e_aks_live_load_balancing/test_load_balancing_live.py`
- `PYTHONPATH=. uv run pytest tests/e2e_aks_live_load_balancing/test_load_balancing_live.py -q`

---

## Documentation Updates Required

- `tests/e2e_aks_live_load_balancing/test_load_balancing_live.py`
- `_docs/_TASKS/TASK-038-live-load-balancing-transport-flake-hardening.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/43-2026-03-18-live-load-balancing-transport-flake-hardening.md`
- `_docs/_CHANGELOG/README.md`
