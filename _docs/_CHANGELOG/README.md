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
