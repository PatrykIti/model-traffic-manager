[Repository README](../../README.md) | [docs](../README.md) | [Operations](./README.md)

# AKS Configuration Delivery

This page describes three practical ways to deliver router configuration to the application in AKS.

## Current runtime contract

Today, the application reads router config from a file path defined by:

- `MODEL_TRAFFIC_MANAGER_CONFIG_PATH`

That means the current implementation already supports approaches where the YAML ends up as a file inside the container.

It does **not** yet support reading the full router YAML directly from a single environment variable.

## Approach 1: Kubernetes Secret mounted as a file

### How it works

1. Terraform or another deployment pipeline writes the YAML into a Kubernetes `Secret` in the target namespace.
2. Helm mounts that `Secret` into the pod as a file.
3. Helm sets `MODEL_TRAFFIC_MANAGER_CONFIG_PATH` to the mounted file path.

### Example shape

- Secret key: `router.yaml`
- mounted path: `/etc/model-traffic-manager/router.yaml`
- env var: `MODEL_TRAFFIC_MANAGER_CONFIG_PATH=/etc/model-traffic-manager/router.yaml`

### Pros

- works with the current code without further changes
- keeps the application contract simple
- avoids stuffing large multiline YAML into environment variables
- easy to reason about in Helm charts through extra volumes and extra volume mounts

### Cons

- if Terraform writes the secret value directly into Kubernetes, the value can end up in Terraform state
- the whole YAML is treated as secret material even when large parts are just operational config

### Recommendation

This is the **best fit for the current implementation** if you want to manage the value through namespace-scoped Kubernetes Secrets.

## Approach 2: Kubernetes Secret injected as an environment variable

### How it works

1. Terraform or another deployment pipeline writes the YAML into a Kubernetes `Secret`.
2. Helm injects the secret value into an environment variable.
3. The application would need to parse the YAML from that env var.

### Current support

This is **not supported by the current code**.

To support it, the application would need an additional setting such as:

- `MODEL_TRAFFIC_MANAGER_CONFIG_YAML`

and startup logic that prefers env-var YAML over file-based config when present.

### Pros

- simple pod spec wiring when teams prefer env-based configuration
- no need to mount an extra volume

### Cons

- worse ergonomics for large multiline YAML payloads
- harder to inspect and debug than a mounted file
- environment variables are a poor fit for larger structured documents
- still carries the Terraform state caveat if the value is materialized through Terraform-managed Secrets

### Recommendation

Only choose this if your platform strongly prefers env-based injection **and** we explicitly add support for it in the application.

## Approach 3: ConfigMap for router config plus Secret for true secret values

### How it works

1. Store the router YAML in a Kubernetes `ConfigMap`.
2. Store only true secret material in Kubernetes `Secret` objects or another secret backend.
3. Keep secret references in the YAML, not raw secret values.
4. Mount the config file into the pod and point `MODEL_TRAFFIC_MANAGER_CONFIG_PATH` to it.

### Pros

- best semantic separation between config and secrets
- aligns with the router design, where YAML mainly describes topology and policy
- makes the YAML easier to audit and version
- reserves Secrets for actual secret material such as API keys

### Cons

- requires discipline so that secret values do not leak into the ConfigMap
- if you still source the ConfigMap data from Terraform, config values will still exist in Terraform state

### Recommendation

This is the **best long-term operational model** once the router starts using secret references like `secret_ref` for actual sensitive values.

## AKS-specific note

You do **not** need the Secrets Store CSI Driver for any of the three approaches above.

If your platform already manages namespace-scoped `Secret` or `ConfigMap` resources through Terraform and Helm, that is a valid model for this application.

The main design choice is not CSI vs non-CSI. The main choice is:

- file-based config vs env-based config
- and mixed config/secrets vs separated config/secrets

## Recommended decision

For the current codebase:

1. use a file-based approach
2. mount the config into the pod
3. set `MODEL_TRAFFIC_MANAGER_CONFIG_PATH`

If you want the simplest drop-in model today, use:

- **Kubernetes Secret mounted as a file**

If you want the cleaner long-term operating model, evolve toward:

- **ConfigMap for router YAML + Secret for actual secret material**

Avoid:

- full router YAML in one environment variable

unless the application is explicitly extended to support that path.
