[Repository README](../../../README.md) | [docs](../../README.md) | [Operations](../README.md) | [Runbooks](./README.md)

# GHCR and Image-Pull Failures

## Symptom

- `401 Unauthorized` from GHCR
- `ImagePullBackOff`
- local runner fails on `docker login ghcr.io`
- pod rollout stalls because the router or mock image cannot be pulled

## Likely Cause

- missing or invalid GHCR token
- missing image-pull secret in the test namespace
- helper deployment used the wrong service account
- GHCR transient outage or throttling

## Quick Checks

```bash
kubectl get events -n e2e-router --sort-by=.metadata.creationTimestamp
```

Inspect:
- runner output for `docker login` / `docker buildx build --push`
- namespace secret and service-account patching
- artifact bundle logs

## Fix

- confirm `GHCR_TOKEN` / `GHCR_USERNAME` or authenticated `gh` session
- confirm the runner created and patched `ghcr-pull`
- confirm helper pods use `serviceAccountName: router-app` when they rely on the same pull secret
- rerun if the failure matches transient GHCR/network conditions

## Safe To Rerun

- yes, once GHCR auth or service-account wiring is fixed
