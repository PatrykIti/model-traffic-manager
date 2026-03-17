[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-030](./TASK-030-model-aware-load-balancing-within-tier.md)

# TASK-030-05: Advanced Balancing Controls, Examples, and Documentation
# FileName: TASK-030-05-advanced-balancing-controls-examples-and-documentation.md

**Priority:** High
**Category:** Documentation and Hardening Planning
**Estimated Effort:** Medium
**Dependencies:** TASK-030, TASK-030-03, TASK-030-04
**Status:** **Done** (2026-03-17)

---

## Overview

Evaluate whether operators need balancing controls beyond `weight` and document the recommended patterns.

Candidate controls:
- `balancing_policy`
- `target_share_percent`
- `max_share_percent`
- `warm_standby`
- `drain`

Recommended approach:
- start with `weight + compatibility_group`
- add more advanced controls only if they improve explainability instead of turning the selector into an opaque policy engine

Documentation requirement:
- official examples must explain the trade-offs of `weight`, `compatibility_group`, and any future controls in plain language

## Sub-Tasks

### TASK-030-05-01: Balancing policy contract and selector semantics

**Status:** To Do

Define whether and how policies such as `weighted_round_robin` and `active_standby` should enter the config contract.

### TASK-030-05-02: Warm-standby and drain semantics

**Status:** To Do

Define how non-primary but ready upstreams should behave without pretending they are unhealthy.

### TASK-030-05-03: Share caps and target-share controls

**Status:** To Do

Evaluate whether `target_share_percent` and `max_share_percent` are needed on top of `weight`.

### TASK-030-05-04: Commented YAML examples and official docs

**Status:** To Do

Add commented YAMLs and docs that explain when advanced controls should and should not be used.

### TASK-030-05-05: Live validation package for advanced balancing behavior

**Status:** To Do

Define or extend live validation so advanced balancing controls can be proven on real Azure-backed infra.

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-030-05-advanced-balancing-controls-examples-and-documentation.md`
- `_docs/_TASKS/TASK-030-05-01-balancing-policy-contract-and-selector-semantics.md`
- `_docs/_TASKS/TASK-030-05-02-warm-standby-and-drain-semantics.md`
- `_docs/_TASKS/TASK-030-05-03-share-caps-and-target-share-controls.md`
- `_docs/_TASKS/TASK-030-05-04-commented-yaml-examples-and-official-docs.md`
- `_docs/_TASKS/TASK-030-05-05-live-validation-package-for-advanced-balancing-behavior.md`
