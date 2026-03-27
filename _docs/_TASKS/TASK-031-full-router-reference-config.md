[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-031: Full Router Reference Config
# FileName: TASK-031-full-router-reference-config.md

**Priority:** High
**Category:** Documentation and Runtime Examples
**Estimated Effort:** Small
**Dependencies:** TASK-024, TASK-026, TASK-027, TASK-030
**Status:** **Done** (2026-03-17)

---

## Overview

Add one full, commented router config reference next to `configs/example.router.yaml`.

Business goal:
- keep `configs/example.router.yaml` small and runnable
- provide one commented file that shows the full available contract of the router in one place
- make it easy for operators and backend engineers to understand how the different configuration areas fit together

---

## Sub-Tasks

### TASK-031-01: Full capabilities router YAML and official docs alignment

**Status:** Done (2026-03-17)

Add `configs/full-capabilities.router.yaml`, wire it into official docs, and keep it covered by the config loader test suite.

---

## Testing Requirements

- the full reference YAML validates through the current config loader
- docs clearly distinguish the minimal bootstrap config from the full reference config

---

## Documentation Updates Required

- `configs/full-capabilities.router.yaml`
- `docs/configuration/configuration-model.md`
- `docs/getting-started/local-development.md`
- `_docs/_TASKS/TASK-031-full-router-reference-config.md`
- `_docs/_TASKS/TASK-031-01-full-capabilities-router-yaml-and-official-docs-alignment.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/README.md`
