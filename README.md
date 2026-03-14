# model-traffic-manager

`model-traffic-manager` is a policy-driven AI traffic router for Azure and AKS.

The repository is being prepared to host a small, observable, explainable service that routes AI traffic across deployments, accounts, and regions without turning into a generic AI platform.

This router is intended to run as an internal LLM traffic manager for the chatbot system backend. It is not the SaaS tenant orchestrator or the tenant control-plane router.

## What this repository covers

- a single stable endpoint for AI workloads
- routing across multiple Azure AI / Azure OpenAI accounts and regions
- secretless outbound authentication via Managed Identity whenever possible
- explainable routing, health state tracking, failover, cooldown, and circuit breaker behavior
- official product/application documentation in `docs/`
- internal delivery and AI-assistance documentation in `_docs/`

## Documentation model

- [docs/README.md](./docs/README.md) contains the official application documentation for operators, contributors, and future users of the router.
- [_docs/README.md](./_docs/README.md) contains internal planning, task tracking, changelog, and implementation guidance used to evolve the repository with AI-assisted workflows.
- [_docs/SaaS-Chatbot-System-Orchiestration.md](./_docs/SaaS-Chatbot-System-Orchiestration.md) is an informational internal reference describing the orchestration layer above the chatbot system. It exists to keep the router and future backend work aligned with the expected platform boundary and to remind us that this repository is not the SaaS control-plane router.
- [AGENTS.md](./AGENTS.md) is the working agreement for repository rules, documentation standards, task workflow, and definition of done.

## Current status

The repository has completed the bootstrap and configuration foundation phases, includes both Phase 2 proxy paths, supports Phase 3 Managed Identity outbound auth, and now includes Phase 5 health-state behavior plus deployment-level limiting.

What is already implemented:

- the runnable FastAPI application shell and quality automation
- startup-time YAML validation and a config-backed deployment registry
- health endpoints and `GET /deployments`
- `POST /v1/chat/completions/{deployment_id}` with tiered multi-upstream failover
- `POST /v1/embeddings/{deployment_id}` with tiered multi-upstream failover
- outbound auth modes `none`, `api_key`, and `managed_identity`
- weighted round robin inside the lowest available tier for request selection
- in-memory health-state persistence, cooldown after `429`, and per-upstream circuit breaker transitions
- a Redis-backed health-state adapter behind the repository port
- deployment-level request-rate limiting and concurrency limiting
- Redis-backed limiter adapters behind repository ports
- request correlation with `x-request-id`
- structured runtime decision events and a Prometheus `/metrics` endpoint
- trace foundation for inbound requests and outbound model attempts
- opt-in `integration-azure` and `e2e-aks` workflows plus a repo-local Terraform wrapper for higher-level validation

Still ahead:

- timeout/pool tuning and broader hardening

## Local bootstrap

```text
make bootstrap
make check
make run
```

## Quick navigation

- [Official docs](./docs/README.md)
- [Internal docs](./_docs/README.md)
- [Contribution guide](./CONTRIBUTING.md)
- [Repository rules](./AGENTS.md)
