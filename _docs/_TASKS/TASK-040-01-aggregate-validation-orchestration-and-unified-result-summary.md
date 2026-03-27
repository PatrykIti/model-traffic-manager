[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-040](./TASK-040-post-mvp-operational-hardening-and-ci-reliability-program.md)

# TASK-040-01: Aggregate Validation Orchestration and Unified Result Summary
# FileName: TASK-040-01-aggregate-validation-orchestration-and-unified-result-summary.md

**Priority:** High
**Category:** Workflow Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-040, TASK-040-07
**Status:** **Done** (2026-03-20)

---

## Objective

Add one aggregate runner that executes a curated ordered set of validation suites and emits one final summary with per-suite status, duration, artifact location, and cleanup state.

---

## Target Repo Areas

- `Makefile`
- `scripts/release/`
- `docs/getting-started/local-development.md`
- optional workflow wrappers under `.github/workflows/`

---

## Scope

- add one local command such as:
  - `make validate-azure-all-local ENVIRONMENT=dev1`
  - or `make validate-live-all-local ENVIRONMENT=dev1`
- execute suites sequentially, not in parallel
- collect outcome metadata:
  - suite name
  - start/end time
  - duration
  - pass/fail
  - artifact directory
  - cleanup status
- print one compact final summary block

Explicit non-goal:
- do not make this orchestrator the only supported path; per-suite commands must remain first-class

---

## Implementation Notes

- keep the suite list explicit and ordered
- allow fail-fast and continue-on-error modes as explicit options, not hidden behavior
- summary output should be machine-readable enough for later CI reuse

Suggested output shape:

```json
{
  "environment": "dev1",
  "started_at": "2026-03-18T12:00:00Z",
  "finished_at": "2026-03-18T12:42:00Z",
  "overall_status": "failed",
  "suites": [
    {
      "suite": "integration-azure-chat",
      "status": "passed",
      "duration_seconds": 118,
      "artifacts_dir": "/tmp/mtm-run-123/integration-azure-chat",
      "cleanup_status": "clean"
    }
  ]
}
```

## Sub-Tasks

### TASK-040-01-01: Matrix runner and summary generation

**Status:** Done (2026-03-20)

Add the aggregate matrix runner and the unified summary JSON/text output for sequential validation runs.

### TASK-040-01-02: Make targets and operator guidance for matrix runs

**Status:** Done (2026-03-20)

Expose the matrix runner through `make` and document how to use the aggregate local commands.

---

## Pseudocode

```text
suite_order = [
  "integration-azure",
  "integration-azure-chat",
  "integration-azure-embeddings",
  "e2e-aks",
  "e2e-aks-live-model",
  "e2e-aks-live-embeddings",
  "e2e-aks-live-load-balancing",
  "e2e-aks-live-shared-services",
  "e2e-aks-redis",
]

results = []

for suite in suite_order:
    started = now()
    exit_code = run_runner(suite, env, artifacts_root=suite_dir)
    results.append({
        suite,
        status: exit_code == 0 ? "passed" : "failed",
        duration_seconds: now() - started,
        artifacts_dir: suite_dir,
        cleanup_status: read_cleanup_marker(suite_dir),
    })
    if fail_fast and exit_code != 0:
        break

print_summary(results)
exit nonzero_if_any_failed(results)
```

---

## Risks

- one aggregate command can hide the fact that suites are still independent; the summary must keep failures attributable
- long sequential runs can be expensive; this should stay opt-in

---

## Testing Requirements

- `make -n <aggregate-target>` shows the intended ordered suite execution
- runner logic for fail-fast and continue-on-error is unit-testable or shell-testable
- final summary is emitted both on success and failure

---

## Documentation Updates Required

- `Makefile`
- `scripts/release/`
- `docs/getting-started/local-development.md`
- `_docs/_TASKS/TASK-040-01-aggregate-validation-orchestration-and-unified-result-summary.md`
- `_docs/_TASKS/TASK-040-01-01-matrix-runner-and-summary-generation.md`
- `_docs/_TASKS/TASK-040-01-02-make-targets-and-operator-guidance-for-matrix-runs.md`
