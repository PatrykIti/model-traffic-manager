[Repository README](../../README.md) | [docs](../README.md) | [Getting Started](./README.md)

# Product Overview

`model-traffic-manager` is a policy-driven AI traffic router for Azure and AKS.

It is designed to:

- expose one stable endpoint for AI traffic
- route requests across deployments, accounts, and regions
- authenticate outbound calls through Managed Identity whenever possible
- keep routing decisions observable and explainable

The repository is intentionally being built in stages. The current implementation already covers the runnable shell, deployment registry, both current proxy paths, Managed Identity outbound auth, and tiered multi-upstream failover, while the next stages add persistent health state, limiting, and observability.
