[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-040](./TASK-040-post-mvp-operational-hardening-and-ci-reliability-program.md)

# TASK-040-02: Structured Artifact Bundle and Diagnostics Manifest
# FileName: TASK-040-02-structured-artifact-bundle-and-diagnostics-manifest.md

**Priority:** High
**Category:** Diagnostics and Observability
**Estimated Effort:** Medium
**Dependencies:** TASK-040, TASK-040-07
**Status:** **Done** (2026-03-20)

---

## Objective

Standardize the diagnostic output produced by every Azure-backed and AKS-backed suite so one failed run leaves behind a predictable, high-value artifact set.

---

## Target Repo Areas

- `scripts/release/run_azure_test_suite.sh`
- `scripts/release/`
- `.github/workflows/`
- `docs/operations/`

---

## Scope

Artifact bundle per suite should include at minimum:

- rendered router config, when a suite uses a renderer
- Terraform outputs JSON
- raw suite command metadata
- `kubectl get all`, `kubectl describe`, events, and logs for AKS suites
- port-forward logs where relevant
- metrics snapshot before and after critical scenarios when available
- summary manifest describing all emitted files

Suggested manifest path:
- `${artifacts_dir}/manifest.json`

Suggested manifest content:

```json
{
  "suite": "e2e-aks-live-model",
  "environment": "dev1",
  "files": {
    "terraform_outputs": "terraform-outputs.json",
    "router_config": "router-live-model.yaml",
    "kubectl_get_all": "kubectl-get-all.txt",
    "router_logs": "router.log"
  }
}
```

## Sub-Tasks

### TASK-040-02-01: Stable artifact directory and manifest generator

**Status:** Done (2026-03-20)

Introduce a stable artifact directory contract and a manifest generator.

### TASK-040-02-02: Runner artifact capture for integration and AKS suites

**Status:** Done (2026-03-20)

Capture a standardized artifact bundle for integration and AKS suites.

### TASK-040-02-03: Workflow upload and docs alignment for artifact bundles

**Status:** Done (2026-03-20)

Align GitHub workflow uploads and operator docs to the standardized artifact bundle.

---

## Pseudocode

```text
artifacts_dir = tmp_root / suite
mkdir artifacts_dir

write_file(terraform_outputs.json)
copy_if_exists(rendered_router_yaml)
copy_if_exists(port_forward_log)
copy_if_exists(kubectl_get_all)
copy_if_exists(kubectl_events)
copy_if_exists(router_logs)

manifest = build_manifest(files_present)
write_json(manifest.json, manifest)
```

---

## Implementation Notes

- artifact names should be stable across local and CI runs
- missing optional files should be reflected in the manifest rather than causing runner failure
- any request/response samples must be sanitized before persistence

---

## Risks

- larger artifact bundles can increase CI storage cost
- careless log capture can leak tokens or secrets; sanitization rules must be explicit

---

## Testing Requirements

- one failing AKS suite should still produce a manifest and diagnostics bundle
- artifact upload configuration in workflows should reference the standardized paths

---

## Documentation Updates Required

- `scripts/release/run_azure_test_suite.sh`
- `scripts/release/write_validation_artifact_manifest.py`
- `.github/workflows/`
- `docs/operations/`
- `_docs/_TASKS/TASK-040-02-structured-artifact-bundle-and-diagnostics-manifest.md`
- `_docs/_TASKS/TASK-040-02-01-stable-artifact-directory-and-manifest-generator.md`
- `_docs/_TASKS/TASK-040-02-02-runner-artifact-capture-for-integration-and-aks-suites.md`
- `_docs/_TASKS/TASK-040-02-03-workflow-upload-and-docs-alignment-for-artifact-bundles.md`
