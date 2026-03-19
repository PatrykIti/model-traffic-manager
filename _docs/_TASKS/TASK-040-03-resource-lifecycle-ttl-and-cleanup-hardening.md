[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-040](./TASK-040-post-mvp-operational-hardening-and-ci-reliability-program.md)

# TASK-040-03: Resource Lifecycle, TTL, and Cleanup Hardening
# FileName: TASK-040-03-resource-lifecycle-ttl-and-cleanup-hardening.md

**Priority:** High
**Category:** Infrastructure Reliability
**Estimated Effort:** Medium
**Dependencies:** TASK-040
**Status:** **To Do**

---

## Objective

Strengthen cleanup and ownership semantics so temporary validation runs leave behind as little risk and cost as possible.

---

## Target Repo Areas

- `scripts/release/run_azure_test_suite.sh`
- `.github/workflows/e2e-azure-janitor.yml`
- `infra/*`
- docs under `docs/operations/`

---

## Scope

- ensure every created Azure scope carries stable ownership tags
- ensure janitor rules align with current suite naming and TTL semantics
- add cleanup markers for:
  - federated credential creation/deletion
  - namespace creation/deletion
  - image-pull secret creation
  - port-forward teardown
- avoid false-positive cleanup failure when a resource was never created

Candidate tags:
- `codex-repo`
- `codex-scope`
- `codex-environment`
- `codex-run-id`
- `created_on`
- `expires_on`
- `suite`

---

## Pseudocode

```text
created_resources = []

if create_federated_credential():
    created_resources.append("federated_credential")

if create_namespace():
    created_resources.append("namespace")

on_exit:
    for resource in reverse(created_resources):
        best_effort_cleanup(resource)
    write_cleanup_report()
```

---

## Implementation Notes

- cleanup reports should distinguish:
  - `not_created`
  - `deleted`
  - `already_gone`
  - `cleanup_failed`
- janitor logic should target only repository-owned resources

---

## Risks

- over-broad janitor queries can delete non-test resources if ownership filters are weak
- incomplete cleanup reports make cost debugging harder than before

---

## Testing Requirements

- simulate partial creation paths and verify cleanup remains safe
- janitor selection logic should be testable with representative tag payloads

---

## Documentation Updates Required

- `scripts/release/run_azure_test_suite.sh`
- `.github/workflows/e2e-azure-janitor.yml`
- `docs/operations/`
- `_docs/_TASKS/TASK-040-03-resource-lifecycle-ttl-and-cleanup-hardening.md`
