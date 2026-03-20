[Repository README](../../README.md) | [Internal docs](../README.md)

# Task Board

This board tracks every repository work item, including main tasks, subtasks, and deeper breakdown levels.

## Workflow

1. Create a main task in `_docs/_TASKS/` for every repository task.
2. Store the business-oriented scope in the main task file, for example `TASK-002-repository-foundation.md`.
3. Store technical details, pseudocode, and target structure in subtasks, for example `TASK-002-01-public-docs-structure.md`.
4. Split subtasks further when they become too broad or too large, for example `TASK-002-01-01-routing-reference.md`.
5. Add the work item to the correct table in this board and update the statistics.
6. When the work is complete, add a changelog entry in `_docs/_CHANGELOG/`, update its index, and move the work item to **Done**.
7. Update the relevant documentation after every task.

## Naming rules

- Main task: `TASK-001-english-slug.md`
- Subtask: `TASK-001-01-english-slug.md`
- Subtask subtask: `TASK-001-01-01-english-slug.md`
- Use English ASCII slugs with hyphens.

## Task file format

- Header lines:
  - `# TASK-XXX: Title`
  - `# FileName: TASK-XXX-english-slug.md`
- Required fields: `Priority`, `Category`, `Estimated Effort`, `Dependencies`, `Status`
- Required sections: `Overview`, `Sub-Tasks`, `Testing Requirements`, `Documentation Updates Required`
- Main tasks describe business intent, scope, dependencies, and outcome.
- Subtasks describe technical details, pseudocode, target structure, implementation order, and risks.
- Add `Security Contract` for API or security-sensitive work.
- Every documentation Markdown file should have navigation controls near the top.
- Reference template: [EXAMPLE_TASK.md](./EXAMPLE_TASK.md)

## Status rules

- Allowed statuses: `To Do`, `In Progress`, `Done`
- `In Progress` and `Done` must include a date in the task file
- Update the statistics and the appropriate table every time the status changes

## Changelog link

- Every completed work item must be reflected in `_docs/_CHANGELOG/`
- A single changelog entry may cover multiple completed IDs, but it must list them explicitly

## Statistics

- **To Do:** 0 work items
- **In Progress:** 0 work items
- **Done:** 244 work items

---

## To Do

| ID | Title | Priority | Effort | Notes |
|----|-------|----------|--------|-------|
---

## In Progress

| ID | Title | Priority | Effort | Notes |
|----|-------|----------|--------|-------|

---

## Done

| ID | Title | Priority | Effort | Notes |
|----|-------|----------|--------|-------|
| TASK-001 | Repository Governance and Documentation Workflow | High | Medium | Repository rules, indexes, and `AGENTS.md` |
| TASK-001-01 | `AGENTS.md` and Task/Changelog Rules | High | Medium | Technical workflow baseline and documentation guardrails |
| TASK-002 | Repository Foundation and English Documentation Standard | High | Large | Pre-commit, official docs structure, and repository collaboration files |
| TASK-002-01 | Pre-Commit, Official Docs Structure, and Collaboration Files | High | Medium | `.pre-commit`, `docs/`, root metadata, contribution files |
| TASK-002-02 | English Markdown Migration and Documentation Split | High | Medium | English-only policy and translation of repository Markdown files |
| TASK-003 | Pre-Implementation Bootstrap Planning and Backlog Definition | High | Medium | Phase 0 backlog and sequencing defined |
| TASK-003-01 | Phase 0 Workstream Decomposition and Sequencing | High | Medium | Detailed task tree for bootstrap readiness |
| TASK-004-01 | Python Project Bootstrap and Dependency Governance | High | Medium | Python contract, lock file, and base layout completed |
| TASK-004-01-01 | `pyproject.toml`, `.python-version`, `.gitignore`, and Lock Contract | High | Medium | Exact dependency and tool contract implemented |
| TASK-004-01-02 | Base Application, Tests, Config, and Docker Layout | High | Medium | Clean Architecture skeleton roots created |
| TASK-004-02 | FastAPI Application Shell and Runtime Wiring | High | Medium | Minimal runnable HTTP shell completed |
| TASK-004-02-01 | API Entrypoint, Health Routes, and Error Shell | High | Medium | Health endpoints and error shell implemented |
| TASK-004-02-02 | Settings, Container, Logging, and Lifespan Shell | High | Medium | Runtime wiring and startup shell implemented |
| TASK-004-03 | Developer Workflow and Quality Automation | High | Medium | Local commands, CI, and parity completed |
| TASK-004-03-01 | Canonical Local Commands and Task Runner | High | Medium | `Makefile` and standard command set implemented |
| TASK-004-03-02 | CI Workflow and Pre-Commit Parity | High | Medium | PR workflow and quality alignment implemented |
| TASK-004 | Phase 0 Repository Bootstrap and Readiness Foundation | High | Large | Full bootstrap implemented and validated |
| TASK-004-04 | Local Runtime Bootstrap Assets | High | Medium | Docker and runtime input assets implemented and verified |
| TASK-004-04-01 | Dockerfile, Entrypoint, and Image Policy | High | Medium | Docker build verified successfully |
| TASK-004-04-02 | Example Router YAML and Environment Contract | High | Medium | Bootstrap runtime inputs implemented |
| TASK-004-05 | Official Documentation Foundation in `docs/` | High | Medium | First real official docs content created |
| TASK-004-05-01 | Getting Started, System Overview, and Implementation Status | High | Medium | Product-facing entry docs implemented |
| TASK-004-05-02 | Architecture, Configuration, Routing, Operations, and Reference Pages | High | Medium | Public technical docs baseline implemented |
| TASK-004-06 | Smoke Tests and Definition-of-Done Activation | High | Medium | Bootstrap validation and quality gate active |
| TASK-005 | Phase 1 Domain, Config, and Deployment Registry Bootstrap | High | Large | Domain/config foundation and deployment registry implemented |
| TASK-005-01 | Domain and Configuration Model Foundation | High | Medium | Typed domain objects and config contract implemented |
| TASK-005-01-01 | Domain Entities, Value Objects, and Error Contract | High | Medium | Pure domain model and invariants implemented |
| TASK-005-01-02 | Pydantic Config Models and Semantic Validation Rules | High | Medium | Typed YAML contract and semantic validation implemented |
| TASK-005-02 | YAML Loader and Config-Backed Deployment Repository | High | Medium | Startup loading and repository wiring implemented |
| TASK-005-03 | Deployment Listing Use Case and API Surface | High | Medium | First real use case and HTTP surface implemented |
| TASK-005-03-01 | Application Port, DTO, and Use Case | High | Medium | Listing contract in application layer implemented |
| TASK-005-03-02 | Deployment Route and Integration Coverage | High | Medium | `/deployments` route and integration proof implemented |
| TASK-005-04 | Documentation, Task Tracking, and Validation Alignment | High | Small | Docs/task/changelog alignment completed |
| TASK-006 | AKS Configuration Delivery Documentation | High | Small | Official AKS config delivery guidance added |
| TASK-006-01 | Official AKS Config Delivery Approaches Page | High | Small | Three AKS config delivery approaches documented |
| TASK-007 | Layered Testing Model and Phase Mapping | High | Small | Permanent testing levels and phase mapping documented |
| TASK-007-01 | Official and Repository-Level Testing Policy Update | High | Small | Layered testing policy added to AGENTS and official docs |
| TASK-008 | Cost-Aware Azure Test Infrastructure Orchestration Model | High | Medium | Low-cost temporary Azure test infra strategy defined |
| TASK-008-01 | Trigger Policy and Cost Guardrails for Temporary Azure Environments | High | Small | Trigger and budget rules for expensive test environments |
| TASK-008-01-01 | Trigger Matrix and Approval Rules | High | Small | Explicit trigger policy for Azure-backed tests |
| TASK-008-01-02 | Cost, TTL, Budget, and Cleanup Guardrails | High | Small | TTL tags, janitor, and forced cleanup strategy |
| TASK-008-02 | Terraform Wrapper Structure and Module Composition Model | High | Small | Repo-local wrapper strategy defined |
| TASK-008-02-01 | Repo-Local Wrapper Structure and State Boundaries | High | Small | Wrapper and state isolation rules defined |
| TASK-008-02-02 | Module Mapping for `integration-azure` and `e2e-aks` | High | Small | Reusable module composition per test level defined |
| TASK-008-03 | GitHub Workflow Orchestration for Apply, Test, and Destroy | High | Small | GitHub-centered orchestration model defined |
| TASK-008-03-01 | `integration-azure` Workflow Shape | High | Small | Lower-cost Azure workflow shape defined |
| TASK-008-03-02 | `e2e-aks` Workflow Shape with `always()` Destroy | High | Small | Full ephemeral AKS workflow shape defined |
| TASK-008-04 | Minimal Azure Resource Sets by Testing Level | High | Small | Azure footprint minimization strategy defined |
| TASK-008-04-01 | Minimal Resources for `integration-azure` | High | Small | Minimal Azure service set defined |
| TASK-008-04-02 | Minimal Resources for Fully Ephemeral `e2e-aks` | High | Small | Minimal temporary AKS footprint defined |
| TASK-009 | Phase 2 Single-Upstream Routing and First Proxy Path | High | Large | First real routing path for chat completions implemented |
| TASK-009-01 | Chat Proxy Contract and Error Model | High | Medium | Request/response and HTTP error behavior implemented |
| TASK-009-01-01 | Inbound Request and Passthrough Response Contract | High | Small | Raw request and response passthrough implemented |
| TASK-009-01-02 | Error Taxonomy and HTTP Mapping for the First Proxy Path | High | Small | Minimum failure surface and HTTP mapping implemented |
| TASK-009-02 | Outbound Invocation and Auth Header Preparation | High | Medium | HTTPX, secret provider, and auth headers implemented |
| TASK-009-02-01 | Outbound Invoker Contract and `httpx` Implementation | High | Medium | Application port and HTTPX adapter implemented |
| TASK-009-02-02 | Secret Provider Contract and Env-Backed Bootstrap Implementation | High | Medium | `api_key` secret lookup bootstrap path implemented |
| TASK-009-02-03 | Auth Header Builder for `none` and `api_key` | High | Small | Auth header logic for Phase 2 implemented |
| TASK-009-03 | Single-Upstream Selection and `RouteChatCompletion` Use Case | High | Medium | Application routing orchestration implemented |
| TASK-009-03-01 | Single-Upstream Candidate Selection from the Deployment Registry | High | Small | Deterministic single-upstream choice implemented |
| TASK-009-03-02 | `RouteChatCompletion` Orchestration and Response Handling | High | Medium | Main use case flow implemented |
| TASK-009-04 | API Route and Local Integration Proof | High | Medium | FastAPI route and full local proof implemented |
| TASK-009-04-01 | `routes_chat.py` and Application Wiring | High | Small | Route registration and container wiring implemented |
| TASK-009-04-02 | `integration-local` Coverage with Mocked Upstream Behavior | High | Medium | Respx-backed end-to-end local tests implemented |
| TASK-009-05 | Documentation, Task Tracking, and Validation Alignment | High | Small | Final docs and tracking updates completed |
| TASK-010 | Phase 2 Status Reconciliation and Forward Backlog Expansion | High | Small | Post-Phase-2 cleanup and forward planning completed |
| TASK-010-01 | Official Documentation and Repository Metadata Reconciliation | High | Small | Stale status wording and tracking mismatch corrected |
| TASK-010-02 | Forward Task Tree Expansion for the Remaining MVP | High | Small | Task tree extended through the remaining MVP work |
| TASK-011 | Phase 2 Embeddings Proxy Path and Surface Parity | High | Medium | Second single-upstream proxy path implemented |
| TASK-011-01 | Embeddings Request/Response Contract and API Surface | High | Small | Embeddings route contract and HTTP surface implemented |
| TASK-011-02 | `RouteEmbeddings` Use Case and Outbound Reuse | High | Medium | Embeddings use case added on existing outbound/auth plumbing |
| TASK-011-03 | `integration-local` Coverage, Docs, and Example Config Alignment | High | Medium | Local proof, example config, and docs updated for embeddings |
| TASK-012 | Phase 3 Managed Identity Outbound Auth and Token Cache | High | Large | Managed Identity auth and token cache implemented |
| TASK-012-01 | Azure Token Provider Contract and In-Memory Cache | High | Medium | Token acquisition and reuse rules implemented |
| TASK-012-01-01 | Credential Selection and Token Acquisition Semantics | High | Small | Azure credential acquisition wrapped behind a repository port |
| TASK-012-01-02 | Cache Key, Expiry Skew, and Refresh Behavior | High | Small | In-memory token reuse and refresh behavior implemented |
| TASK-012-02 | Managed Identity Auth Header Integration and Bootstrap Wiring | High | Medium | Managed Identity wired through auth builder and container |
| TASK-012-02-01 | Container Wiring and Config/Runtime Validation Alignment | High | Small | Runtime wiring aligned with the existing config contract |
| TASK-012-02-02 | Unit and Local Integration Coverage with Credential Stubs | High | Medium | Managed Identity path proven locally with stubs |
| TASK-012-03 | Documentation, Security Contract, and Operations Guidance | High | Small | Official docs updated for Managed Identity behavior |
| TASK-013 | Phase 4 Multi-Upstream Routing and Tiered Failover | High | Large | Tiered selection and request-level failover implemented |
| TASK-013-01 | Routing Decision Model and Deterministic Selection Policy | High | Medium | Tier-aware selector and balancing model implemented |
| TASK-013-01-01 | Availability Filtering by State and Tier Grouping | High | Small | Lowest-tier candidate grouping behavior implemented |
| TASK-013-01-02 | Weighted Round Robin Implementation and Deterministic Tests | High | Small | Deterministic weighted rotation implemented and tested |
| TASK-013-02 | Request-Attempt Orchestration and Failover for Chat and Embeddings | High | Medium | Retry flow across same-tier and higher-tier candidates implemented |
| TASK-013-02-01 | Retriable vs Non-Retriable Failure Flow | High | Small | Retry rules and stop conditions implemented |
| TASK-013-02-02 | Decision Reasons and Next-Candidate Transitions | High | Small | Selector reasons and candidate progression implemented |
| TASK-013-03 | API and Local Integration Coverage with Documentation Alignment | High | Medium | Local failover proof and routing docs updated |
| TASK-014 | Phase 5 Failure Classification, Health State, Cooldown, and Circuit Breaker | High | Large | Health-aware routing and persistence implemented |
| TASK-014-01 | Failure Taxonomy and Retriable Classification | High | Medium | Failure classification model and retry semantics implemented |
| TASK-014-01-01 | HTTP, Network, and Quota Signatures and Mapping Rules | High | Small | Response and transport failure mappings implemented |
| TASK-014-01-02 | `Retry-After` Parsing and Cooldown Semantics | High | Small | `Retry-After` parsing and cooldown handling implemented |
| TASK-014-02 | Health State Repository and State-Transition Rules | High | Medium | Health-state persistence and transition policy implemented |
| TASK-014-02-01 | In-Memory Bootstrap Repository and Transition Tests | High | Small | Default in-memory health repository implemented |
| TASK-014-02-02 | Redis-Backed Repository Adapter and Persistence Behavior | High | Medium | Redis health-state adapter implemented behind the port |
| TASK-014-03 | Circuit Breaker Thresholds and Router Integration | High | Medium | Cooldown and circuit-open state integrated into routing |
| TASK-014-04 | Operations Docs, Observability Hooks, and Validation Alignment | High | Small | Public docs and tracking updated for health-state behavior |
| TASK-015 | Basic Rate Limiting and Concurrency Limiting | High | Medium | Deployment-level request-rate and concurrency limiting implemented |
| TASK-015-01 | Deployment-Level Limit Contracts and Rejection Model | High | Small | Application-facing limiter contracts and rejection errors implemented |
| TASK-015-02 | Local and Redis-Backed Limiter Adapters | High | Medium | In-memory and Redis-backed limiter adapters implemented |
| TASK-015-03 | Entrypoint Integration, Tests, and Docs | High | Medium | HTTP rejection behavior, tests, and docs updated for limits |
| TASK-016-01 | Decision Reason Logging, Request Correlation, and Operator Diagnostics | High | Medium | Runtime decision events and request correlation implemented |
| TASK-016-01-01 | Structured Event Schema for Selection, Failover, Limiter, and Breaker Updates | High | Small | Runtime event schema implemented in code and docs |
| TASK-016-01-02 | Reference Documentation and Troubleshooting Views | High | Small | Decision reason reference expanded for runtime events |
| TASK-016-02 | Metrics, Traces, and Readiness/Health Observability Expansion | High | Medium | `/metrics`, trace foundation, and observability runtime wiring implemented |
| TASK-016-03 | `integration-azure` and `e2e-aks` Activation | High | Large | Azure-backed workflows, repo-local wrapper, and higher-level test suites activated |
| TASK-016-04 | Performance, Timeout Policy, Pool Tuning, and Release Checks | High | Medium | Timeout policy, pool tuning, and release gate implemented |
| TASK-016 | Explainable Routing, Observability, and Release Hardening | High | Large | Observability, validation activation, and hardening completed |
| TASK-017 | Terraform Scope Model and Tfvars Alignment | High | Medium | Scope-first Terraform layout and tfvars model aligned |
| TASK-017-01 | Terraform Scope and Tfvars Guidance | High | Small | Internal guidance for scope boundaries and tfvars rules added |
| TASK-017-01-01 | Scope Boundaries for Validation Infrastructure | High | Small | Active scope boundaries documented |
| TASK-017-01-02 | Tfvars Environment-Profile Rules | High | Small | Per-scope env tfvars rules documented |
| TASK-017-02 | Scope Split for `integration-azure` and `e2e-aks` | High | Medium | Combined wrapper replaced with separate scope roots |
| TASK-017-02-01 | `integration-azure` Scope Root and Env Tfvars | High | Small | Azure-only scope root and env tfvars implemented |
| TASK-017-02-02 | `e2e-aks` Scope Root, K8s Assets, and Env Tfvars | High | Small | AKS scope root, manifests, and env tfvars implemented |
| TASK-017-03 | Workflow and Release-Check Alignment | High | Small | Workflow and release-check paths aligned to the new scopes |
| TASK-018 | Shared Tfvars Baseline and Scope-Aware Naming | High | Small | Shared baseline tfvars and scope-aware naming implemented |
| TASK-018-01 | Shared Tfvars Baseline for Validation Scopes | High | Small | Shared non-secret env baseline added for all test types |
| TASK-018-02 | Scope-Aware Naming and Workflow Alignment | High | Small | Scope-aware naming and workflow tfvars wiring aligned |
| TASK-019 | Local One-Command Azure-Backed Test Runners | High | Medium | Local apply-test-destroy runners implemented for integration-azure and e2e-aks |
| TASK-019-01 | Local `integration-azure` Runner | High | Small | One-command Azure-backed local runner implemented |
| TASK-019-01-01 | Azure CLI Context and Shared Tfvars Resolution | High | Small | Azure CLI context and shared tfvars baseline resolved automatically |
| TASK-019-01-02 | Apply-Test-Destroy Wrapper for `integration-azure` | High | Small | Guaranteed cleanup wrapper implemented for Azure-backed local runs |
| TASK-019-02 | Local `e2e-aks` Runner with Guaranteed Cleanup | High | Medium | One-command AKS local runner implemented with cleanup traps |
| TASK-019-02-01 | GHCR Image Build and AKS Deploy Contract | High | Small | Local GHCR build/push and AKS deploy contract implemented |
| TASK-019-02-02 | Trap-Based Cleanup and Diagnostics Collection | High | Small | Destroy and diagnostics collection implemented under shell traps |
| TASK-019-03 | Documentation, Makefile, and Operator Contract | High | Small | Stable commands and operator guidance added for local higher-level runs |
| TASK-020 | E2E AKS Live-Model Suite | High | Medium | Separate AKS suite validated end-to-end with real model responses and cleanup |
| TASK-020-01 | Live-Model AKS Scope and Azure OpenAI Infrastructure | High | Medium | AKS, Azure OpenAI deployments, and RBAC scope implemented |
| TASK-020-02 | Live-Model Runner and Router Configuration Generation | High | Small | Dedicated runner and Terraform-output-based runtime config implemented |
| TASK-020-03 | Live-Model E2E Test Suite and Operator Docs | High | Small | Real model-response validation and operator guidance completed |
| TASK-021 | MVP Closure, Runtime State Activation, and Contract Hardening | High | Large | Remaining application-side MVP gaps closed and documentation reconciled |
| TASK-021-01 | Supported Deployment Contracts, Endpoint Guards, and Shared-Service Registry | High | Medium | MVP contract validation and active shared-service registry implemented |
| TASK-021-02 | Half-Open Circuit Recovery and Health-State Transition Hardening | High | Medium | Real half-open probe semantics and hardened recovery transitions implemented |
| TASK-021-03 | Redis-Backed Runtime State Activation and Shared Coordination | High | Medium | Active runtime switch for Redis-backed health and limiter coordination implemented |
| TASK-021-04 | Explainable Routing Rejection Diagnostics and Status Reconciliation | High | Medium | Rejected-candidate diagnostics and final docs/status reconciliation completed |
| TASK-022 | Environment Example and Root README Reconciliation | High | Small | Root environment contract and repository README aligned to the active runtime |
| TASK-022-01 | Structured `.env.example` and Root README Refresh | High | Small | Categorized environment reference and root README status refresh completed |
| TASK-023 | Shared Services Access Model and Router Execution Surface | High | Large | Planning and architecture for shared-service execution completed and realized by TASK-024 |
| TASK-023-01 | Shared-Service Taxonomy, Routing Profiles, and Failover Policy Split | High | Medium | Shared-service policy split completed as the design baseline for implementation |
| TASK-023-02 | Configuration and Domain Model for Shared-Service Execution Policies | High | Medium | Shared-service execution contract planned and then implemented in TASK-024 |
| TASK-023-03 | First Backend-Facing Shared-Service Proxy Path for HTTP/JSON Services | High | Medium | Backend-facing shared-service proxy path planned and then implemented in TASK-024 |
| TASK-023-04 | Direct-Access Model for Provider-Managed Storage and Large Object Workloads | High | Medium | Direct-access boundary for storage-style workloads defined and carried into implementation |
| TASK-023-05 | Validation, Observability, and Official Documentation for Shared-Service Execution | High | Medium | Validation and docs plan completed and then executed in TASK-024 |
| TASK-024 | Shared Services Execution Model and Backend-Facing Proxy Surface | High | Large | Executable shared-service modes implemented without turning the router into a generic gateway |
| TASK-024-01 | Shared-Service Config and Domain Contract for Execution Modes | High | Medium | Typed execution-mode model for shared services implemented |
| TASK-024-02 | Backend-Facing Shared-Service Execution Use Case and API Route | High | Medium | First shared-service proxy route for backend callers implemented |
| TASK-024-03 | Tests, Official Docs, and Changelog Alignment for Shared-Service Execution | High | Medium | Proof and docs for the new execution surface completed |
| TASK-025 | Shared-Service Example YAML Catalog | High | Small | Real shared-service example router configs added and linked from official docs |
| TASK-025-01 | Official Shared-Service Example Router Configs | High | Small | Full example router YAMLs added for direct, single-endpoint, and failover service modes |
| TASK-026 | Deployment Example YAML Catalog | High | Small | Real deployment example router configs added for regional failover, model fallback, and embeddings |
| TASK-026-01 | Official Deployment Example Router Configs | High | Small | Full example router YAMLs added for chat regional failover, model fallback, and embeddings failover |
| TASK-027 | Auth and Identity Example YAML Catalog | High | Small | Real auth and identity example router configs added and linked from official docs |
| TASK-027-01 | Official Auth and Identity Example Router Configs | High | Small | Full example router YAMLs added for default MI, explicit client IDs, and mixed auth modes |
| TASK-027-02 | Official Auth and Identity Documentation Page | High | Small | Dedicated docs page added for auth-mode and identity-selection behavior |
| TASK-028 | Explicit Cooldown State Semantics and Observability | High | Small | Explicit cooldown state semantics implemented for clearer routing and diagnostics |
| TASK-028-01 | Cooldown State Transitions, Routing Reasons, and Docs Alignment | High | Small | Cooldown transitions and cooldown-specific rejection reasons implemented and documented |
| TASK-029 | Live Azure Validation Expansion for Router Surfaces | High | Large | Validation matrix and target live profiles defined for the next Azure-backed test expansion |
| TASK-029-01 | Live Azure Validation Matrix and Profile Taxonomy | High | Small | Validation matrix split across integration-azure, e2e-aks, live-model, shared services, and Redis |
| TASK-029-02 | `integration-azure` Outbound Provider Probes for Chat and Embeddings | High | Medium | Dedicated Azure-only chat and embeddings provider probes implemented with separate scopes and make commands |
| TASK-029-02-01 | `integration-azure-chat` Scope and Provider Probe | High | Medium | Azure-only chat provider probe implemented with its own infra scope and live test suite |
| TASK-029-02-02 | `integration-azure-embeddings` Scope and Provider Probe | High | Medium | Azure-only embeddings provider probe implemented with its own infra scope and live test suite |
| TASK-029-02-03 | Integration-Azure Profile Rollout and Docs Alignment | High | Small | Runner wiring, make targets, environment contract, and docs aligned for split integration-azure profiles |
| TASK-029-03 | `e2e-aks-live-embeddings` Profile | High | Medium | Real embeddings path through router on AKS implemented as a dedicated live profile |
| TASK-029-04 | `e2e-aks-live-model` Chat Failover and Health-State Scenarios | High | Medium | Live failover, cooldown, and circuit scenarios for chat implemented on the existing live-model suite |
| TASK-029-05 | Live Shared-Services Validation on Azure and AKS | High | Medium | Dedicated live profile added for shared-service direct-access and router-proxy execution modes |
| TASK-029-05-01 | Live Shared-Services AKS Scope and Azure Direct-Access Fixture | High | Medium | Dedicated AKS scope and real Azure Storage direct-access fixture implemented |
| TASK-029-05-02 | Live Shared-Services Router Config and Mock Downstreams | High | Medium | Dedicated shared-services config renderer and in-cluster mock downstreams implemented |
| TASK-029-05-03 | Live Shared-Services Suite, Runner, and Docs Rollout | High | Medium | Live shared-services suite, make target, env contract, and docs rollout implemented |
| TASK-029-06 | Redis-Backed Multi-Replica AKS Validation | High | Medium | Dedicated Redis-backed AKS profile added for shared cooldown, circuit, and limiter behavior across replicas |
| TASK-029-06-01 | Redis AKS Scope and Multi-Replica Router Profile | High | Medium | Dedicated AKS scope with two router replicas and in-cluster Redis implemented |
| TASK-029-06-02 | Redis Suite Runner and Replica Targeting | High | Medium | Runner extended with replica-specific port-forwards and make target for the Redis suite |
| TASK-029-06-03 | Redis Multi-Replica Live Suite and Docs Rollout | High | Medium | Live Redis suite and docs rollout implemented for shared-state validation |
| TASK-029-07 | Runner, Workflow, and Documentation Rollout for Expanded Live Suites | High | Medium | GitHub workflows and docs now align with the full expanded live validation matrix |
| TASK-029-07-01 | Workflow Suite-Input Rollout for Azure Profiles | High | Medium | Azure-backed workflows now select profiles through suite inputs and the shared runner |
| TASK-029-07-02 | Testing Docs and Environment Contract Reconciliation | High | Small | Official testing docs and local guidance now reflect the final expanded matrix |
| TASK-029-07-03 | Task Board and Changelog Reconciliation for Expanded Matrix | High | Small | Validation-expansion package closed cleanly in the task board and changelog |
| TASK-039 | Live Validation Stability Fixes for Auth, Context, and Quota Constraints | High | Medium | Auth roles, AKS context isolation, quota-aware VM sizing, and fixture compatibility were hardened after first live runs |
| TASK-040 | Post-MVP Operational Hardening and CI Reliability Program | High | Large | Post-MVP ops and CI hardening backlog defined with concrete subtask plans and pseudocode |
| TASK-040-04 | Retry and Resilience Policy for Runner-Side External Operations | High | Medium | Bounded retry and transient-failure matching are now implemented for runner-side external operations |
| TASK-040-04-01 | Retry Policy Catalog and Matchers | High | Medium | A central transient-failure matcher now classifies retry policies for runner-side operations |
| TASK-040-04-02 | Runner Integration for Bounded Retries | High | Medium | The shared Azure/AKS runner now applies bounded retries to selected transient operations |
| TASK-040-04-03 | Docs and Validation Alignment for Runner Retries | High | Small | Docs and validation now reflect the new bounded runner retry behavior |
| TASK-040-02 | Structured Artifact Bundle and Diagnostics Manifest | High | Medium | Standardized artifact bundles and manifests are now emitted for Azure-backed and AKS-backed suites |
| TASK-040-02-01 | Stable Artifact Directory and Manifest Generator | High | Medium | The runner now writes artifacts into a stable per-suite directory and emits a manifest |
| TASK-040-02-02 | Runner Artifact Capture for Integration and AKS Suites | High | Medium | The runner now captures Terraform outputs, rendered configs, kubectl diagnostics, logs, and port-forward traces |
| TASK-040-02-03 | Workflow Upload and Docs Alignment for Artifact Bundles | High | Small | Workflows upload the standardized artifact root and docs describe the bundle contract |
| TASK-040-03 | Resource Lifecycle, TTL, and Cleanup Hardening | High | Medium | Ownership tags, cleanup reporting, and janitor filters are now hardened for temporary validation scopes |
| TASK-040-03-01 | Unified Ownership Tags and TTL Metadata | High | Medium | Azure-backed scopes now share a stronger ownership and TTL tag contract |
| TASK-040-03-02 | Runner Cleanup Report and Resource Markers | High | Medium | The shared runner now emits cleanup state for namespaces, federated credentials, secrets, and port-forwards |
| TASK-040-03-03 | Janitor Filter Tightening and Ops Docs Alignment | High | Small | The janitor now targets repository-owned temporary scopes and docs explain the cleanup contract |
| TASK-040-01 | Aggregate Validation Orchestration and Unified Result Summary | High | Medium | Aggregate matrix execution and unified summary output are now implemented for local validation runs |
| TASK-040-01-01 | Matrix Runner and Summary Generation | High | Medium | The matrix runner now emits both JSON and human-readable summaries for sequential suite execution |
| TASK-040-01-02 | Make Targets and Operator Guidance for Matrix Runs | High | Small | Aggregate matrix runs are exposed through make and documented for operators |
| TASK-040-06 | CI Trigger Matrix, Cost Gating, and Scheduling Policy | High | Medium | Trigger and scheduling policy is now encoded through suite-registry flags plus nightly/release workflows |
| TASK-040-06-01 | Suite Trigger Policy in Registry and Workflows | High | Medium | Nightly and release eligibility is now encoded in the canonical suite registry |
| TASK-040-06-02 | Nightly and Release Validation Workflows | High | Medium | Curated nightly and release-validation workflows now execute suite matrices from the registry |
| TASK-040-06-03 | CI Trigger Matrix Docs and Policy Reconciliation | High | Small | Docs now explain the PR, manual, nightly, and release validation policy |
| TASK-040-08 | Operator Runbooks and Failure Triage Guides | High | Medium | Operator runbooks now cover the real auth, GHCR, AKS, quota, storage, and cleanup failures seen in live validation |
| TASK-040-08-01 | Auth and RBAC Runbooks for Live Validation | High | Medium | Azure OpenAI permission and RBAC propagation failures are documented for operators |
| TASK-040-08-02 | AKS Runtime and GHCR Runbooks | High | Medium | AKS rollout, port-forward, and GHCR/image-pull failure signatures are documented |
| TASK-040-08-03 | Quota, Storage, and Cleanup Runbooks | High | Medium | Quota, storage fixture, cleanup failures, and the runbook index are documented |
| TASK-040-05 | Quota-Aware Infrastructure Profile Selection and VM-Family Strategy | High | Medium | Per-suite AKS quota-aware placement is now encoded in env tfvars and documented for operators |
| TASK-040-05-01 | Environment-Specific AKS Validation Profile Matrix | High | Medium | The current suite-to-region and suite-to-VM-family matrix is encoded in per-scope env tfvars |
| TASK-040-05-02 | Operator Guidance for Quota-Aware Suite Placement | High | Small | Official docs now describe the active quota-aware placement matrix and override rules |
| TASK-040-07 | Workflow and Runner Contract Registry Normalization | High | Medium | Validation suite metadata is now centralized in one registry consumed by runner, make, workflows, and docs |
| TASK-040-07-01 | Suite Registry and Runner Consumption | High | Medium | The shared Azure/AKS runner now consumes canonical suite metadata from one registry |
| TASK-040-07-02 | Make, Workflow, and Docs Alignment to Suite Registry | High | Medium | Make, workflows, and docs now align to the canonical suite registry |
| TASK-030 | Model-Aware Load Balancing Within Tier | High | Large | Model-aware same-tier balancing implemented with examples, docs, and live validation |
| TASK-030-01 | Upstream Compatibility Metadata and Balancing Policy Contract | High | Medium | Compatibility metadata and balancing contract added to upstreams |
| TASK-030-02 | Selector Behavior for Compatible Pools Within a Tier | High | Medium | Same-tier selector behavior updated for compatibility-aware pools |
| TASK-030-03 | Chat-Specific Active-Active Balancing Patterns | High | Medium | Active-active and active-standby chat balancing patterns implemented |
| TASK-030-04 | Embeddings-Specific Safety Rules | High | Medium | Embeddings-safe balancing and config guards implemented |
| TASK-030-05 | Advanced Balancing Controls, Examples, and Documentation | High | Medium | First-stage advanced controls, docs, and validation implemented |
| TASK-030-05-01 | Balancing Policy Contract and Selector Semantics | High | Medium | `weighted_round_robin` and `active_standby` selector semantics implemented |
| TASK-030-05-02 | Warm-Standby and Drain Semantics | High | Medium | `warm_standby` and `drain` controls implemented |
| TASK-030-05-03 | Share Caps and Target-Share Controls | High | Medium | `target_share_percent` and `max_share_percent` guardrails implemented |
| TASK-030-05-04 | Commented YAML Examples and Official Docs | High | Medium | Commented YAML examples and official docs added for load balancing |
| TASK-030-05-05 | Live Validation Package for Advanced Balancing Behavior | High | Medium | Live AKS validation added for balancing behavior and operational controls |
| TASK-030-06 | Commented Example YAML Catalog for Load-Balancing Scenarios | High | Medium | YAML catalog added for active-active, active-standby, and embeddings-safe pools |
| TASK-030-07 | Live Azure Validation Package and Dedicated Runner for Load Balancing | High | Medium | Dedicated live infra scope, suite, and make runner added for load balancing |
| TASK-031 | Full Router Reference Config | High | Small | Commented full reference config added next to the minimal bootstrap example |
| TASK-031-01 | Full Capabilities Router YAML and Official Docs Alignment | High | Small | Full router reference config wired into docs and loader validation |
| TASK-032 | Live Load-Balancing Rendered Config Scalar Typing Fix | High | Small | Rendered live load-balancing config hardened against YAML date coercion |
| TASK-033 | Verbose Pytest Output for Make-Driven Test Runners | Medium | Small | All current make-driven pytest flows now print per-test names and fuller summaries |
| TASK-034 | AKS Runner Pod Readiness and Exec Target Hardening | High | Small | Azure/AKS runner waits for ready pods and execs against the resolved router container |
| TASK-035 | Live Port-Forward and Transport Retry Hardening | High | Small | Dynamic local ports, forwarded-health wait, and live transport retries harden AKS live runs |
| TASK-036 | Shell Runner Syntax Validation in Quality Gates | High | Small | Shell syntax is now checked in make and pre-commit quality gates before Azure/AKS runs |
| TASK-037 | Randomized OpenAI Account and Subdomain Suffixes for Live Scopes | High | Small | Live Azure OpenAI scopes now use random suffixes to avoid soft-delete naming collisions |
| TASK-038 | Live Load-Balancing Transport Flake Hardening | High | Small | Live load-balancing suite now retries transient transport failures and restarts dirty distribution windows |
