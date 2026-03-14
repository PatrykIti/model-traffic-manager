[Repository README](../../README.md) | [docs](../README.md) | [Getting Started](./README.md)

# Product Overview

`model-traffic-manager` is a policy-driven AI traffic router for Azure and AKS.

It is designed to:

- expose one stable endpoint for AI traffic
- route requests across deployments, accounts, and regions
- authenticate outbound calls through Managed Identity whenever possible
- keep routing decisions observable and explainable

Operational role:

- this service is the internal LLM traffic manager used by the chatbot system backend
- tenant onboarding, placement, namespace provisioning, and SaaS control-plane routing belong to the separate orchestrator/admin service

The repository is intentionally being built in stages. The current implementation already covers the runnable shell, deployment registry, both current proxy paths, Managed Identity outbound auth, tiered multi-upstream failover, health-state behavior including cooldown and circuit breaking, deployment-level request limiting, and the first runtime observability layer. The next stages focus on higher-level Azure-backed validation and hardening.
