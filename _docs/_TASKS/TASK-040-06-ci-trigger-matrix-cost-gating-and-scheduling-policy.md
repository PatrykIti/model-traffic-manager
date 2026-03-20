[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-040](./TASK-040-post-mvp-operational-hardening-and-ci-reliability-program.md)

# TASK-040-06: CI Trigger Matrix, Cost Gating, and Scheduling Policy
# FileName: TASK-040-06-ci-trigger-matrix-cost-gating-and-scheduling-policy.md

**Priority:** High
**Category:** CI Policy
**Estimated Effort:** Medium
**Dependencies:** TASK-040, TASK-040-07
**Status:** **Done** (2026-03-20)

---

## Objective

Define which validation suites should run on PRs, which should stay manual-only, which should be nightly, and which should guard releases.

---

## Target Repo Areas

- `.github/workflows/`
- `docs/operations/testing-levels-and-environments.md`
- `docs/getting-started/local-development.md`

---

## Scope

Recommended matrix:

- PR mandatory:
  - `make check`
  - optional `integration-azure` smoke only if touched areas justify it
- manual:
  - all expensive live suites
- nightly:
  - selected live suites with controlled cost
- release candidate:
  - aggregate full matrix

Need explicit rules for:
- path-based gating
- manual dispatch defaults
- nightly cadence
- branch restrictions
- artifact retention and naming

---

## Pseudocode

```text
if event == pull_request:
    run quality only
    optionally run cheap cloud smoke if changed_paths match critical areas

if event == workflow_dispatch:
    allow suite selection

if event == schedule:
    run curated nightly matrix

if release_candidate:
    run aggregate matrix
```

## Sub-Tasks

### TASK-040-06-01: Suite trigger policy in registry and workflows

**Status:** Done (2026-03-20)

Define nightly and release eligibility in the canonical suite registry and expose that policy to workflows.

### TASK-040-06-02: Nightly and release validation workflows

**Status:** Done (2026-03-20)

Add a curated nightly workflow and a release-validation workflow driven by the suite registry.

### TASK-040-06-03: CI trigger matrix docs and policy reconciliation

**Status:** Done (2026-03-20)

Document the final trigger matrix across PR, manual, nightly, and release validation paths.

---

## Risks

- running expensive suites too often will create cost and quota noise
- running them too rarely will make the matrix stale and untrusted

---

## Testing Requirements

- workflow trigger rules should be validated by the repository workflow validator
- docs must explain the trigger matrix in operator-facing language

---

## Documentation Updates Required

- `.github/workflows/`
- `docs/operations/testing-levels-and-environments.md`
- `_docs/_TASKS/TASK-040-06-ci-trigger-matrix-cost-gating-and-scheduling-policy.md`
- `_docs/_TASKS/TASK-040-06-01-suite-trigger-policy-in-registry-and-workflows.md`
- `_docs/_TASKS/TASK-040-06-02-nightly-and-release-validation-workflows.md`
- `_docs/_TASKS/TASK-040-06-03-ci-trigger-matrix-docs-and-policy-reconciliation.md`
