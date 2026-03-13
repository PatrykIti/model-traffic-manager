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

The repository is still in the foundation stage. At the moment it contains the target architecture, routing model, and process rules that will guide the first implementation milestones.

## Quick navigation

- [Official docs](./docs/README.md)
- [Internal docs](./_docs/README.md)
- [Contribution guide](./CONTRIBUTING.md)
- [Repository rules](./AGENTS.md)
