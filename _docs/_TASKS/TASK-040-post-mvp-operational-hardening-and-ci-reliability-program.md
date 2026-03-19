[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-040: Post-MVP Operational Hardening and CI Reliability Program
# FileName: TASK-040-post-mvp-operational-hardening-and-ci-reliability-program.md

**Priority:** High
**Category:** Operations and CI Planning
**Estimated Effort:** Large
**Dependencies:** TASK-019, TASK-029, TASK-039
**Status:** **Done** (2026-03-18)

---

## Overview

Define the post-MVP hardening program for local runners, Azure-backed validation, diagnostics, workflow gating, and operator support.

Business goal:
- keep the expanded validation matrix reliable enough to use continuously
- reduce the cost of diagnosing failures in Azure-backed and AKS-backed suites
- turn the current working set of live profiles into a maintainable operational system

Non-goal:
- do not add new router product features here
- this package is about runner quality, diagnostics, cleanup, workflow behavior, and operational safety

---

## Security Contract

- diagnostics and artifacts must not leak secrets, tokens, or raw secret values
- cleanup logic must only target resources, namespaces, and credentials created by the repository-owned validation workflows
- quota-aware profile selection must remain explicit and auditable; it must not silently widen infrastructure cost or privilege scope
- workflow rollout must not accidentally make expensive live suites mandatory on every PR

---

## Sub-Tasks

### TASK-040-01: Aggregate validation orchestration and unified result summary

**Status:** To Do

Add one higher-level orchestrator for sequential execution of the full validation matrix and emit one normalized summary for the entire run.

### TASK-040-02: Structured artifact bundle and diagnostics manifest

**Status:** To Do

Capture a richer and more uniform artifact set for every Azure-backed and AKS-backed suite, with a machine-readable manifest for triage.

### TASK-040-03: Resource lifecycle, TTL, and cleanup hardening

**Status:** To Do

Strengthen cleanup, ownership markers, and janitor behavior so partial failures do not leave behind confusing or expensive leftovers.

### TASK-040-04: Retry and resilience policy for runner-side external operations

**Status:** To Do

Add consistent retry, backoff, and eventual-consistency handling around the runner’s Azure, Kubernetes, GHCR, and Terraform integration points.

### TASK-040-05: Quota-aware infrastructure profile selection and VM-family strategy

**Status:** To Do

Make validation profile sizing explicit per environment and per suite, with a documented fallback strategy for quota-constrained subscriptions.

### TASK-040-06: CI trigger matrix, cost gating, and scheduling policy

**Status:** To Do

Formalize which suites are PR-safe, which are manual-only, which are nightly, and which belong to release validation.

### TASK-040-07: Workflow and runner contract registry normalization

**Status:** To Do

Define one explicit suite registry so `make`, runner scripts, workflows, docs, and future tooling all use the same source of truth.

### TASK-040-08: Operator runbooks and failure triage guides

**Status:** To Do

Document common failure signatures, diagnostics, and response steps for Azure-backed and AKS-backed validation runs.

---

## Program Structure

Recommended sequencing:

1. `TASK-040-07`
   establish one suite registry before more rollout logic drifts again
2. `TASK-040-04`
   stabilize the runner against transient cloud and cluster failures
3. `TASK-040-02`
   make diagnostics richer before broadening orchestration
4. `TASK-040-03`
   harden cleanup and ownership tracking
5. `TASK-040-05`
   formalize quota-aware sizing and fallback behavior
6. `TASK-040-06`
   decide when the expensive suites should run automatically
7. `TASK-040-01`
   add a top-level orchestrator once the suite contracts are stable
8. `TASK-040-08`
   publish operator-facing runbooks with final failure patterns and workflows

---

## Testing Requirements

- every subtask must keep `make check` and `make release-check` usable as the local operator contract
- new orchestration or workflow logic must be validated through existing shell checks and workflow validation
- no hardening task is complete without explicit diagnostic proof for the changed runner/workflow surface

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-040-post-mvp-operational-hardening-and-ci-reliability-program.md`
- `_docs/_TASKS/TASK-040-01-aggregate-validation-orchestration-and-unified-result-summary.md`
- `_docs/_TASKS/TASK-040-02-structured-artifact-bundle-and-diagnostics-manifest.md`
- `_docs/_TASKS/TASK-040-03-resource-lifecycle-ttl-and-cleanup-hardening.md`
- `_docs/_TASKS/TASK-040-04-retry-and-resilience-policy-for-runner-side-external-operations.md`
- `_docs/_TASKS/TASK-040-05-quota-aware-infrastructure-profile-selection-and-vm-family-strategy.md`
- `_docs/_TASKS/TASK-040-06-ci-trigger-matrix-cost-gating-and-scheduling-policy.md`
- `_docs/_TASKS/TASK-040-07-workflow-and-runner-contract-registry-normalization.md`
- `_docs/_TASKS/TASK-040-08-operator-runbooks-and-failure-triage-guides.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/49-2026-03-18-post-mvp-operational-hardening-and-ci-reliability-program.md`
- `_docs/_CHANGELOG/README.md`
