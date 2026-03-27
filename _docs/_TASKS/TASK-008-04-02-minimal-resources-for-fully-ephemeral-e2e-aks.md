[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-008-04-02: Minimal Resources for Fully Ephemeral `e2e-aks`
# FileName: TASK-008-04-02-minimal-resources-for-fully-ephemeral-e2e-aks.md

**Priority:** High
**Category:** Testing Infrastructure Planning
**Estimated Effort:** Small
**Dependencies:** TASK-008-04
**Status:** **Done** (2026-03-13)

---

## Overview

Define the smallest AKS-backed test footprint for a private owner who cannot justify a long-lived cluster.

---

## Minimal Resource Set

- one temporary resource group
- one minimal AKS cluster
- workload identity plumbing
- only the Azure dependencies needed by the exact e2e scenario

Prefer:

- smallest supported node shape that still runs the workload reliably
- shortest possible lifetime
- test image registry choice that minimizes extra always-on cost

Potential registry rule:

- prefer GHCR or another low-friction image path if it avoids introducing a standing ACR cost for early-stage testing
- add ACR only if Azure-native pull and auth requirements make it necessary

---

## Recommendation

Use this level only for:

- manual verification
- nightly validation
- release-candidate checks
- features whose correctness genuinely depends on AKS runtime behavior

Do not make this the default for day-to-day pull requests.

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-008-04-02-minimal-resources-for-fully-ephemeral-e2e-aks.md`
