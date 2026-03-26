[Repository README](../../README.md) | [Internal docs](../README.md)

# Changelog

This directory stores the repository changelog history.

The **Index** table below acts as the changelog board and shows what was completed and when.

## Workflow

1. After completing a task or a coherent group of tasks, create a new changelog file in `_docs/_CHANGELOG/`.
2. Use the naming convention below and list every completed task/subtask ID covered by the entry.
3. Add a row to the **Index** table with the number, date, title, and change type.
4. Synchronize this index with the task board in `_docs/_TASKS/README.md`.

## File naming

- Format: `{N}-{YYYY-MM-DD}-short-title.md`
- Example: `1-2025-11-22-project-init-and-rpc.md`
- `N` increases sequentially and is never reused

## Entry format

- Title line with the changelog number and short title
- `Date`, `Version`, and `Tasks`
- `Key Changes` grouped by area
- Concise but explicit explanation of what changed
- Reference template: [EXAMPLE_CHANGELOG.md](./EXAMPLE_CHANGELOG.md)

## Index

| No. | Date | Title | Type |
|-----|------|-------|------|
| 1 | 2026-03-13 | Repo governance, task workflow and AGENTS rules | docs/process |
| 2 | 2026-03-13 | Repository foundation, public docs structure, and English markdown standard | docs/process |
| 3 | 2026-03-13 | Phase 0 bootstrap planning and task decomposition | docs/planning |
| 4 | 2026-03-13 | Phase 0 bootstrap implementation and runtime shell | bootstrap |
| 5 | 2026-03-13 | Phase 1 domain, config validation, and deployment registry bootstrap | feature/bootstrap |
| 6 | 2026-03-13 | AKS configuration delivery approaches documentation | docs/aks |
| 7 | 2026-03-13 | Layered testing model and phase mapping | docs/testing |
| 8 | 2026-03-13 | Cost-aware Azure test infrastructure orchestration model | docs/testing-infra |
| 9 | 2026-03-13 | Phase 2 single-upstream routing and first proxy path | feature/routing |
| 10 | 2026-03-14 | Phase 2 status reconciliation and forward backlog expansion | docs/planning |
| 11 | 2026-03-14 | Phase 2 embeddings proxy path and surface parity | feature/routing |
| 12 | 2026-03-14 | Phase 3 Managed Identity outbound auth and token cache | feature/auth |
| 13 | 2026-03-14 | Phase 4 multi-upstream routing and tiered failover | feature/routing |
| 14 | 2026-03-14 | Phase 5 failure classification, health state, cooldown, and circuit breaker | feature/health |
| 15 | 2026-03-14 | Basic rate limiting and concurrency limiting | feature/limits |
| 16 | 2026-03-14 | Explainable routing and runtime observability foundation | feature/observability |
| 17 | 2026-03-14 | Azure-backed validation activation and test harness scaffolding | validation/infra |
| 18 | 2026-03-14 | Release hardening and final TASK-016 completion | hardening/release |
| 19 | 2026-03-14 | Terraform scope model and tfvars alignment | infra/structure |
| 20 | 2026-03-14 | Shared tfvars baseline and scope-aware naming | infra/structure |
| 21 | 2026-03-14 | Local one-command Azure-backed test runners | workflow/testing |
| 22 | 2026-03-15 | E2E AKS live-model suite and platform reference docs | validation/e2e |
| 23 | 2026-03-15 | MVP closure, runtime state activation, and contract hardening | feature/mvp-closure |
| 24 | 2026-03-15 | Environment example and root README reconciliation | docs/root |
| 25 | 2026-03-15 | Shared services execution model and backend-facing proxy surface | feature/shared-services |
| 26 | 2026-03-15 | Shared services planning closure and task reconciliation | docs/planning |
| 27 | 2026-03-15 | Shared-service example YAML catalog | docs/examples |
| 28 | 2026-03-15 | Deployment example YAML catalog | docs/examples |
| 29 | 2026-03-15 | Auth and identity example YAML catalog | docs/examples |
| 30 | 2026-03-16 | Explicit cooldown state semantics and observability | feature/health |
| 31 | 2026-03-16 | Live Azure validation expansion planning | docs/planning |
| 32 | 2026-03-16 | E2E AKS live embeddings profile | validation/e2e |
| 33 | 2026-03-16 | E2E AKS live chat failover scenarios | validation/e2e |
| 34 | 2026-03-17 | Live chat failover mock image pull fix | validation/e2e |
| 35 | 2026-03-17 | Model-aware load balancing within tier | feature/routing |
| 36 | 2026-03-17 | Full router reference config | docs/examples |
| 37 | 2026-03-17 | Live load-balancing rendered config scalar typing fix | validation/e2e |
| 38 | 2026-03-17 | Verbose pytest output for make-driven test runners | workflow/testing |
| 39 | 2026-03-17 | AKS runner pod readiness and exec target hardening | validation/e2e |
| 40 | 2026-03-17 | Live port-forward and transport retry hardening | validation/e2e |
| 41 | 2026-03-17 | Shell runner syntax validation in quality gates | workflow/testing |
| 42 | 2026-03-17 | Randomized OpenAI account and subdomain suffixes for live scopes | validation/infra |
| 43 | 2026-03-18 | Live load-balancing transport flake hardening | validation/e2e |
| 44 | 2026-03-18 | Integration-azure chat and embeddings provider probes | validation/integration |
| 45 | 2026-03-18 | Live shared-services validation on Azure and AKS | validation/e2e |
| 46 | 2026-03-18 | Redis-backed multi-replica AKS validation | validation/e2e |
| 47 | 2026-03-18 | Expanded live validation workflow rollout | workflow/testing |
| 48 | 2026-03-18 | Live validation stability fixes for auth, context, and quota constraints | validation/stability |
| 49 | 2026-03-18 | Post-MVP operational hardening and CI reliability program | docs/planning |
| 50 | 2026-03-19 | Quota-aware AKS suite placement matrix | infra/planning |
| 51 | 2026-03-20 | Suite registry normalization for runners and workflows | workflow/architecture |
| 52 | 2026-03-20 | Bounded retry policy for live validation runners | runner/reliability |
| 53 | 2026-03-20 | Structured validation artifact bundles | diagnostics/artifacts |
| 54 | 2026-03-20 | Resource lifecycle and cleanup hardening | infra/reliability |
| 55 | 2026-03-20 | CI trigger matrix and validation scheduling policy | ci/policy |
| 56 | 2026-03-20 | Aggregate validation matrix runner | workflow/orchestration |
| 57 | 2026-03-20 | Operator runbooks for live validation failures | docs/operations |
| 58 | 2026-03-21 | Semantic release workflow and public changelog | workflow/release |
| 59 | 2026-03-25 | Azure Monitor request-flow observability | feature/observability |
| 60 | 2026-03-25 | Consumer role traffic grouping | feature/observability |
| 61 | 2026-03-25 | Live observability AKS suite | validation/e2e |
| 62 | 2026-03-26 | Observability live suite log capture and query hardening | validation/reliability |
| 63 | 2026-03-26 | Live observability scope destroy hardening | validation/reliability |
