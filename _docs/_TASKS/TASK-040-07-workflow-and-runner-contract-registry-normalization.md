[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-040](./TASK-040-post-mvp-operational-hardening-and-ci-reliability-program.md)

# TASK-040-07: Workflow and Runner Contract Registry Normalization
# FileName: TASK-040-07-workflow-and-runner-contract-registry-normalization.md

**Priority:** High
**Category:** Workflow Architecture
**Estimated Effort:** Medium
**Dependencies:** TASK-040
**Status:** **Done** (2026-03-20)

---

## Objective

Create one explicit suite registry so `make`, workflow inputs, runner scripts, and docs all derive from the same contract instead of drifting apart.

---

## Target Repo Areas

- `scripts/release/`
- `Makefile`
- `.github/workflows/`
- docs under `docs/`

---

## Scope

The registry should define, per suite:

- suite id
- scope dir
- test path
- requires AKS
- requires image build/push
- outputs JSON env var
- docs label
- artifact label
- whether the suite is cheap/manual/nightly/release

Possible forms:
- JSON
- YAML
- Python module
- shell-readable metadata file

Recommended direction:
- prefer a structured machine-readable file plus a thin loader in scripts

## Sub-Tasks

### TASK-040-07-01: Suite registry and runner consumption

**Status:** Done (2026-03-20)

Introduce the canonical suite registry and wire it into the shared Azure/AKS runner.

### TASK-040-07-02: Make, workflow, and docs alignment to suite registry

**Status:** Done (2026-03-20)

Align `Makefile`, GitHub workflows, and docs to the canonical suite registry.

---

## Pseudocode

```json
{
  "e2e-aks-live-model": {
    "scope_dir": "infra/e2e-aks-live-model",
    "tests_path": "tests/e2e_aks_live_model",
    "requires_aks": true,
    "requires_image": true,
    "outputs_env": "E2E_LIVE_MODEL_OUTPUTS_JSON"
  }
}
```

```text
suite = load_suite_metadata(selected_suite)
runner.configure_from_suite(suite)
```

---

## Risks

- duplicating suite metadata across bash, make, workflows, and docs will reintroduce drift quickly

---

## Testing Requirements

- suite lookup must fail clearly for unknown suite ids
- runner and workflow validation must consume the same suite metadata successfully

---

## Documentation Updates Required

- `scripts/release/`
- `Makefile`
- `.github/workflows/`
- `docs/`
- `_docs/_TASKS/TASK-040-07-workflow-and-runner-contract-registry-normalization.md`
- `_docs/_TASKS/TASK-040-07-01-suite-registry-and-runner-consumption.md`
- `_docs/_TASKS/TASK-040-07-02-make-workflow-and-docs-alignment-to-suite-registry.md`
