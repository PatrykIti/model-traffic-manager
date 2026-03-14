# model-traffic-manager

`model-traffic-manager` is a policy-driven AI traffic router for Azure and AKS.

The repository is being prepared to host a small, observable, explainable service that routes AI traffic across deployments, accounts, and regions without turning into a generic AI platform.

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
- [AGENTS.md](./AGENTS.md) is the working agreement for repository rules, documentation standards, task workflow, and definition of done.

## Current status

The repository has completed the bootstrap and configuration foundation phases, includes both Phase 2 proxy paths, supports Phase 3 Managed Identity outbound auth, and now includes the first Phase 5 health-state behavior.

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

Still ahead:

- rate limiting, concurrency limiting, and richer observability

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
