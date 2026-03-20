[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-040](./TASK-040-post-mvp-operational-hardening-and-ci-reliability-program.md)

# TASK-040-08: Operator Runbooks and Failure Triage Guides
# FileName: TASK-040-08-operator-runbooks-and-failure-triage-guides.md

**Priority:** High
**Category:** Operational Documentation
**Estimated Effort:** Medium
**Dependencies:** TASK-040, TASK-040-02, TASK-040-03, TASK-040-04, TASK-040-05
**Status:** **Done** (2026-03-20)

---

## Objective

Create operator-facing runbooks for the most common Azure-backed and AKS-backed validation failures.

---

## Target Repo Areas

- `docs/operations/`
- potentially new `docs/operations/runbooks/`

---

## Scope

Runbooks should cover at least:

- Azure OpenAI permission errors
- role-assignment eventual consistency
- GHCR auth or image-pull failures
- AKS rollout and pod readiness failures
- `kubectl port-forward` instability
- storage fixture provisioning failures
- quota exhaustion
- cleanup / destroy failures

Preferred format:
- failure signature
- likely cause
- quick checks
- remediation steps
- whether rerun is safe

Example section shape:

```text
Symptom:
  401 PermissionDenied from Azure OpenAI
Likely cause:
  executor principal is not assigned to Cognitive Services OpenAI User
Checks:
  az role assignment list ...
Fix:
  rerun suite after role assignment propagation or apply role-assignment fix
```

## Sub-Tasks

### TASK-040-08-01: Auth and RBAC runbooks for live validation

**Status:** Done (2026-03-20)

Document Azure OpenAI permission and RBAC propagation failures.

### TASK-040-08-02: AKS runtime and GHCR runbooks

**Status:** Done (2026-03-20)

Document rollout, pod-readiness, port-forward, and GHCR/image-pull failures.

### TASK-040-08-03: Quota, storage, and cleanup runbooks

**Status:** Done (2026-03-20)

Document quota, storage fixture, cleanup failures, and the runbook index.

---

## Risks

- missing runbooks turns every live-suite failure into bespoke debugging
- over-detailed docs without a signature-to-fix structure will not help operators under time pressure

---

## Testing Requirements

- docs must reference real failure signatures already observed in the live matrix
- links from testing-level docs to runbooks should be explicit

---

## Documentation Updates Required

- `docs/operations/`
- `_docs/_TASKS/TASK-040-08-operator-runbooks-and-failure-triage-guides.md`
- `_docs/_TASKS/TASK-040-08-01-auth-and-rbac-runbooks-for-live-validation.md`
- `_docs/_TASKS/TASK-040-08-02-aks-runtime-and-ghcr-runbooks.md`
- `_docs/_TASKS/TASK-040-08-03-quota-storage-and-cleanup-runbooks.md`
