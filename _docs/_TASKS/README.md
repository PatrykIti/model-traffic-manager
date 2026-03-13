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
- **Done:** 65 work items

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
