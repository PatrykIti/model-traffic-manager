[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-032: Live Load-Balancing Rendered Config Scalar Typing Fix
# FileName: TASK-032-live-load-balancing-rendered-config-scalar-typing-fix.md

**Priority:** High
**Category:** Validation and Test Hardening
**Estimated Effort:** Small
**Dependencies:** TASK-030
**Status:** **Done** (2026-03-17)

---

## Overview

Fix the dedicated live load-balancing runner so its generated router config stays valid after YAML parsing.

Business goal:
- keep `make e2e-aks-live-load-balancing-local ENVIRONMENT=<env>` runnable without manual YAML fixes
- prevent date-like scalar values such as `2025-04-14` from being parsed as YAML dates instead of strings
- add a regression test so the rendered config path stays covered by automated validation

---

## Sub-Tasks

- update the live load-balancing renderer to quote `model_version` values explicitly
- cover the rendered output with a config-loader test that validates the generated YAML end to end

---

## Testing Requirements

- `tests/unit/infrastructure/config/test_yaml_loader.py` validates the rendered live load-balancing config
- the rendered config keeps `model_version` values as strings for chat and embeddings upstreams

---

## Documentation Updates Required

- `scripts/release/render_live_load_balancing_router_config.py`
- `tests/unit/infrastructure/config/test_yaml_loader.py`
- `_docs/_TASKS/TASK-032-live-load-balancing-rendered-config-scalar-typing-fix.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/37-2026-03-17-live-load-balancing-rendered-config-scalar-typing-fix.md`
- `_docs/_CHANGELOG/README.md`
