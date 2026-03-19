[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-040](./TASK-040-post-mvp-operational-hardening-and-ci-reliability-program.md)

# TASK-040-04: Retry and Resilience Policy for Runner-Side External Operations
# FileName: TASK-040-04-retry-and-resilience-policy-for-runner-side-external-operations.md

**Priority:** High
**Category:** Runner Reliability
**Estimated Effort:** Medium
**Dependencies:** TASK-040, TASK-040-07
**Status:** **To Do**

---

## Objective

Add a consistent retry and eventual-consistency policy for the runner’s interaction with Azure, Kubernetes, GHCR, and Terraform.

---

## Target Repo Areas

- `scripts/release/run_azure_test_suite.sh`
- `scripts/release/`
- docs under `docs/operations/`

---

## Scope

Operations that should be reviewed for retry/backoff:

- `docker login ghcr.io`
- `docker buildx build --push`
- `terraform apply` post-provision polling helpers
- `az aks get-credentials`
- `az identity federated-credential create/delete`
- `kubectl rollout status`
- `kubectl port-forward`
- first live requests after RBAC/role assignment propagation

Policy requirements:

- retries must be explicit per operation class
- backoff must be bounded
- fatal non-retriable errors must still fail fast

---

## Pseudocode

```text
retry_with_backoff(
    command,
    attempts=5,
    base_delay=2,
    retriable_patterns=[
        "TooManyRequests",
        "connection reset",
        "timed out",
        "context deadline exceeded",
    ],
)
```

For first live probes:

```text
for attempt in 1..N:
    response = call_endpoint()
    if response is success:
        break
    if response matches eventual_consistency_window:
        sleep(backoff)
        continue
    fail
```

---

## Risks

- over-retrying can hide real regressions
- under-retrying leaves the live matrix flaky and expensive to rerun

---

## Testing Requirements

- runner-level helper behavior must be demonstrably deterministic under mocked failure patterns
- retry logs must clearly state attempt number and failure reason

---

## Documentation Updates Required

- `scripts/release/run_azure_test_suite.sh`
- `docs/operations/`
- `_docs/_TASKS/TASK-040-04-retry-and-resilience-policy-for-runner-side-external-operations.md`
