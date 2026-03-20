[Repository README](../../../README.md) | [docs](../../README.md) | [Operations](../README.md) | [Runbooks](./README.md)

# AKS Rollout and Port-Forward Failures

## Symptom

- `kubectl rollout status ... timed out`
- pod stuck in `ContainerCreating`
- `kubectl exec` or live tests fail right after rollout
- `httpx.ReadError`, `httpx.ConnectError`, or `httpx.ReadTimeout` against the local forwarded endpoint

## Likely Cause

- pod was not actually ready yet even though deployment rollout moved forward
- image pull or startup is slower than expected
- `kubectl port-forward` was not stable when tests started
- concurrent suites were fighting over kubeconfig or local ports

## Quick Checks

```bash
kubectl get all -n e2e-router
kubectl describe deployment/router-app -n e2e-router
kubectl get events -n e2e-router --sort-by=.metadata.creationTimestamp
```

Also inspect:
- `port-forward*.log`
- pod logs
- `cleanup-report.json`

## Fix

- confirm the runner waited for `Ready` pods, not only deployment rollout
- confirm the run used an isolated `KUBECONFIG`
- inspect port-forward logs for resets or early termination
- rerun if the failure is clearly transport-flaky and not a router logic error

## Safe To Rerun

- yes, if diagnostics show a transient startup or port-forward failure
