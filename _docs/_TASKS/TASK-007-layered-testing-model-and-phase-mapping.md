[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-007: Layered Testing Model and Phase Mapping
# FileName: TASK-007-layered-testing-model-and-phase-mapping.md

**Priority:** High
**Category:** Testing Strategy
**Estimated Effort:** Small
**Dependencies:** TASK-005
**Status:** **Done** (2026-03-13)

---

## Overview

Define the permanent layered testing model for the repository and map each testing level to the relevant implementation phases.

Business goal:
- make it explicit which test scope belongs to which stage of delivery
- avoid mixing local integration, Azure integration, and AKS end-to-end concerns
- preserve lower-level tests even after higher-level environments are introduced

---

## Sub-Tasks

### TASK-007-01: Official and repository-level testing policy update

**Status:** Done

Add the layered testing model to `AGENTS.md` and to the official docs as a persistent repository rule.

---

## Testing Requirements

- `AGENTS.md` clearly defines the four testing levels and their purpose
- official docs clearly define the phase mapping and cumulative rule
- documentation links remain valid

---

## Documentation Updates Required

- `AGENTS.md`
- `docs/operations/README.md`
- `docs/operations/testing-levels-and-environments.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/README.md`
- `_docs/_CHANGELOG/7-2026-03-13-layered-testing-model-and-phase-mapping.md`
