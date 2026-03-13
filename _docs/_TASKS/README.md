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
- **Done:** 5 work items

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
