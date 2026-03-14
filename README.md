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

The repository has completed the bootstrap and configuration foundation phases and now includes the first Phase 2 proxy path.

What is already implemented:

- the runnable FastAPI application shell and quality automation
- startup-time YAML validation and a config-backed deployment registry
- health endpoints and `GET /deployments`
- `POST /v1/chat/completions/{deployment_id}` with single-upstream selection
- outbound auth modes `none` and `api_key`

Still ahead:

- `POST /v1/embeddings/{deployment_id}`
- outbound `managed_identity`
- tiered multi-upstream routing and failover
- health-state persistence, cooldown, and circuit breaker behavior
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
