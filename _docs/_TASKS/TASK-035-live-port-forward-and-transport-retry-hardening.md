[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-035: Live Port-Forward and Transport Retry Hardening
# FileName: TASK-035-live-port-forward-and-transport-retry-hardening.md

**Priority:** High
**Category:** Validation and Runner Hardening
**Estimated Effort:** Small
**Dependencies:** TASK-020, TASK-029, TASK-034
**Status:** **Done** (2026-03-17)

---

## Overview

Harden live AKS test execution against transient local transport failures around `kubectl port-forward`.

Business goal:
- stop flaky `ReadError` and `ConnectError` failures when the router pod is healthy but the local forwarded connection is not yet stable
- avoid fixed local-port collisions between repeated local runs
- preserve better diagnostics when the forwarded channel is the failing component

---

## Sub-Tasks

- allocate a dynamic local port for router port-forwarding instead of always using `18080`
- wait for `GET /health/ready` over the forwarded local endpoint before starting pytest
- include the port-forward log in diagnostics
- retry live-model test requests on transient `httpx.TransportError` failures

---

## Testing Requirements

- `bash -n scripts/release/run_azure_test_suite.sh` stays valid
- live-model tests keep retry behavior for transport-level failures without weakening status assertions

---

## Documentation Updates Required

- `scripts/release/run_azure_test_suite.sh`
- `tests/e2e_aks_live_model/test_chat_live_model.py`
- `_docs/_TASKS/TASK-035-live-port-forward-and-transport-retry-hardening.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/40-2026-03-17-live-port-forward-and-transport-retry-hardening.md`
- `_docs/_CHANGELOG/README.md`
