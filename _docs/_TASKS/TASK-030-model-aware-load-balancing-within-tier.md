[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-030: Model-Aware Load Balancing Within Tier
# FileName: TASK-030-model-aware-load-balancing-within-tier.md

**Priority:** High
**Category:** Routing and Config Planning
**Estimated Effort:** Large
**Dependencies:** TASK-013, TASK-021, TASK-026
**Status:** **To Do**

---

## Overview

Design and implement model-aware load balancing for upstreams that share the same routing tier.

Business goal:
- preserve the current weighted balancing behavior where it is safe
- prevent logically incompatible upstreams from being balanced together by accident
- allow operators to express intentional active-active traffic distribution across compatible model endpoints

Key rule:
- balancing and failover are different concerns
- same-tier balancing should happen only inside a compatible pool
- higher-tier fallback may intentionally cross model variants when explicitly configured

---

## Security Contract

- the router must not silently balance traffic across incompatible model contracts
- embeddings pools must not mix vector spaces that can corrupt downstream retrieval quality
- any advanced balancing controls must remain explainable and testable

---

## Sub-Tasks

### TASK-030-01: Upstream compatibility metadata and balancing policy contract

**Status:** To Do

Define the minimum metadata needed to decide whether upstreams in the same tier may be balanced together.

### TASK-030-02: Selector behavior for compatible pools within a tier

**Status:** To Do

Extend selection so weighted round robin works inside an explicit compatibility pool instead of blindly across all same-tier upstreams.

### TASK-030-03: Chat-specific active-active balancing patterns

**Status:** To Do

Support safe balancing for equivalent chat models across regions, accounts, or deployment copies.

### TASK-030-04: Embeddings-specific safety rules

**Status:** To Do

Prevent unsafe embeddings balancing across different embedding models or vector spaces unless explicitly allowed by a stronger compatibility contract.

### TASK-030-05: Advanced balancing controls, examples, and documentation

**Status:** To Do

Evaluate whether additional controls beyond `weight` are needed and document recommended patterns with real examples.

### TASK-030-06: Commented example YAML catalog for load-balancing scenarios

**Status:** To Do

Add clear, operator-focused example router configs with inline comments that explain active-active balancing, model fallback, and embeddings-safe balancing.

### TASK-030-07: Live Azure validation package and dedicated runner for load balancing

**Status:** To Do

Add a dedicated live infra/test package plus a new `make` entry point that proves same-tier load balancing and compatibility-aware routing on real Azure-backed infrastructure.

---

## Recommended Design Direction

First iteration:
- keep `weight`
- add explicit compatibility metadata
- balance only within the same `tier` and the same compatibility group

Candidate upstream fields:
- `model_name`
- `model_version`
- `deployment_name`
- `compatibility_group`
- `balancing_policy`

Potential later controls:
- `target_share_percent`
- `max_share_percent`
- `warm_standby`
- `drain`

Example requirement:
- official examples must include explanatory comments in YAML, not only bare fields
- examples should cover chat, embeddings, and mixed multi-account scenarios separately

---

## Documentation Updates Required

- `docs/configuration/deployment-and-upstreams.md`
- `docs/routing/routing-strategy.md`
- `docs/reference/decision-reasons.md`
- `_docs/_TASKS/TASK-030-model-aware-load-balancing-within-tier.md`
- `_docs/_TASKS/TASK-030-01-upstream-compatibility-metadata-and-balancing-policy-contract.md`
- `_docs/_TASKS/TASK-030-02-selector-behavior-for-compatible-pools-within-a-tier.md`
- `_docs/_TASKS/TASK-030-03-chat-specific-active-active-balancing-patterns.md`
- `_docs/_TASKS/TASK-030-04-embeddings-specific-safety-rules.md`
- `_docs/_TASKS/TASK-030-05-advanced-balancing-controls-examples-and-documentation.md`
- `_docs/_TASKS/TASK-030-06-commented-example-yaml-catalog-for-load-balancing-scenarios.md`
- `_docs/_TASKS/TASK-030-07-live-azure-validation-package-and-dedicated-runner-for-load-balancing.md`
- `_docs/_TASKS/README.md`
