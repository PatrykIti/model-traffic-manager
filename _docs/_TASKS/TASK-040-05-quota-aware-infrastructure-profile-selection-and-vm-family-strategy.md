[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-040](./TASK-040-post-mvp-operational-hardening-and-ci-reliability-program.md)

# TASK-040-05: Quota-Aware Infrastructure Profile Selection and VM-Family Strategy
# FileName: TASK-040-05-quota-aware-infrastructure-profile-selection-and-vm-family-strategy.md

**Priority:** High
**Category:** Infrastructure Planning
**Estimated Effort:** Medium
**Dependencies:** TASK-040, TASK-040-07
**Status:** **Done** (2026-03-19)

---

## Objective

Make suite sizing explicit per environment so validation profiles do not drift into quota failures or unnecessarily expensive infrastructure.

---

## Target Repo Areas

- `infra/_shared/env/`
- `infra/**/env/`
- `scripts/release/run_azure_test_suite.sh`
- official docs for testing and operations

---

## Scope

Define a repeatable strategy for:

- default VM family and size per suite
- optional `cheap`, `standard`, `full` profile classes
- environment overrides, especially for quota-constrained subscriptions
- guidance on `max_surge` vs `max_unavailable` for low-quota AKS scenarios

Recommended rule:
- prefer per-environment explicit sizing over hidden automatic discovery
- document supported fallbacks instead of guessing at runtime

## Sub-Tasks

### TASK-040-05-01: Environment-specific AKS validation profile matrix

**Status:** Done (2026-03-19)

Encode the active suite placement directly in per-scope env tfvars.

### TASK-040-05-02: Operator guidance for quota-aware suite placement

**Status:** Done (2026-03-19)

Document the current matrix and the override strategy for future quota changes.

---

## Pseudocode

```text
profile_matrix = {
  dev1: {
    e2e-aks: "Standard_D2s_v4",
    e2e-aks-live-model: "Standard_D2s_v4",
    e2e-aks-redis: "Standard_D2s_v4",
  },
  prd1: {
    e2e-aks: "Standard_D4ds_v5",
  },
}

vm_size = explicit_tfvars_override or profile_matrix[env][suite]
```

---

## Risks

- silent runtime fallback can make cost debugging impossible
- one global VM default is too coarse for a mixed validation matrix

---

## Testing Requirements

- `terraform validate` should succeed for all suite scopes with the new sizing contract
- docs must clearly explain how to override suite sizing when quotas differ by environment

---

## Documentation Updates Required

- `infra/_shared/env/`
- `infra/**/env/`
- `docs/operations/`
- `docs/getting-started/local-development.md`
- `_docs/_TASKS/TASK-040-05-quota-aware-infrastructure-profile-selection-and-vm-family-strategy.md`
- `_docs/_TASKS/TASK-040-05-01-environment-specific-aks-validation-profile-matrix.md`
- `_docs/_TASKS/TASK-040-05-02-operator-guidance-for-quota-aware-suite-placement.md`
