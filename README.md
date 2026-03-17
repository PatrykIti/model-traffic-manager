# model-traffic-manager

`model-traffic-manager` is a policy-driven AI traffic router for Azure and AKS.

The repository hosts a small, observable, explainable service that routes AI traffic across deployments, accounts, and regions without turning into a generic AI platform.

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
- [_docs/CHATBOT_PLATFORM.md](./_docs/CHATBOT_PLATFORM.md) is an informational internal reference describing the expected chatbot platform structure above the router, including the control plane, runtime API, UI, and persistence split that should remain outside this repository.
- [AGENTS.md](./AGENTS.md) is the working agreement for repository rules, documentation standards, task workflow, and definition of done.

## Current status

The repository currently implements the full application-side MVP contract described in `docs/` and `_docs/_MVP/`.

What is already implemented:

- the runnable FastAPI application shell and quality automation
- startup-time YAML validation and config-backed registries for deployments and shared services
- health endpoints plus `GET /deployments` and `GET /shared-services`
- `POST /v1/shared-services/{service_id}` for router-callable shared services
- `POST /v1/chat/completions/{deployment_id}` with tiered multi-upstream failover
- `POST /v1/embeddings/{deployment_id}` with tiered multi-upstream failover
- strict MVP deployment-contract validation for chat and embeddings surfaces
- outbound auth modes `none`, `api_key`, and `managed_identity`
- weighted round robin inside the lowest available tier for request selection
- cooldown after `429`, quota-aware failure classification, circuit opening, and half-open recovery probes
- in-memory and Redis-backed runtime state for health and limiter coordination
- deployment-level request-rate limiting and concurrency limiting
- rejected-candidate diagnostics and explicit failover reasons in runtime events
- shared-service execution modes that distinguish direct backend access, single-endpoint router proxy, and tiered-failover router proxy
- request correlation with `x-request-id`
- structured runtime decision events and a Prometheus `/metrics` endpoint
- trace foundation for inbound requests and outbound model attempts
- opt-in `integration-azure`, `e2e-aks`, and `e2e-aks-live-model` validation flows
- persistent outbound HTTP client tuning with explicit connection limits and timeout policy
- `make release-check` as the current release gate for quality, shell syntax, workflow, and Terraform validation

## Quick start

```text
make bootstrap
make check
make run
```

For local configuration and overrides:

- copy or reference values from [`.env.example`](./.env.example)
- keep the router YAML in [`configs/example.router.yaml`](./configs/example.router.yaml) or point `MODEL_TRAFFIC_MANAGER_CONFIG_PATH` to another file
- use `MODEL_TRAFFIC_MANAGER_RUNTIME_STATE_BACKEND=redis` together with `MODEL_TRAFFIC_MANAGER_REDIS_URL` when you want shared runtime state locally

Useful local endpoints after startup:

- `GET /health/live`
- `GET /health/ready`
- `GET /deployments`
- `GET /shared-services`
- `POST /v1/shared-services/{service_id}`
- `POST /v1/chat/completions/{deployment_id}`
- `POST /v1/embeddings/{deployment_id}`

## Validation levels

The repository keeps three practical validation tiers:

- default local quality: `make check`
- Azure-backed integration without AKS: `make integration-azure-local`
- AKS end-to-end validation:
  `make e2e-aks-local` for smoke coverage and `make e2e-aks-live-model-local` for real model-response validation

The higher-level suites are intentionally opt-in because they provision temporary Azure resources and, in the live-model profile, consume real model quota.

## Quick navigation

- [Official docs](./docs/README.md)
- [Internal docs](./_docs/README.md)
- [Contribution guide](./CONTRIBUTING.md)
- [Repository rules](./AGENTS.md)
