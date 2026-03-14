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
