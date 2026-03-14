[Repository README](../../README.md) | [docs](../README.md) | [Getting Started](./README.md)

# Product Overview

`model-traffic-manager` is a policy-driven AI traffic router for Azure and AKS.

It is designed to:

- expose one stable endpoint for AI traffic
- route requests across deployments, accounts, and regions
- authenticate outbound calls through Managed Identity whenever possible
- keep routing decisions observable and explainable

The repository is intentionally being built in stages. The current implementation already covers the runnable shell, deployment registry, and the first real chat completions proxy path, while the next stages add embeddings, Managed Identity, failover, health state, and observability.
