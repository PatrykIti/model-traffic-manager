[README repo](../../README.md) | [_docs](../README.md) | [_TASKS](./README.md)

# TASK-001-01: AGENTS.md i Zasady Taskow oraz Changelogow
# FileName: TASK-001-01-agents-md-i-zasady-taskow-oraz-changelogow.md

**Priority:** High
**Category:** Documentation Process
**Estimated Effort:** Medium
**Dependencies:** TASK-001
**Status:** **Done** (2026-03-13)

---

## Overview

Subtask techniczny porzadkujacy zasady pracy agentow i ludzi w repo.

Zakres:
- wyciagniecie zasad produktu i implementacji z `_docs/_MVP/`
- zapisanie ich w `AGENTS.md`
- ustalenie hierarchii taskow i naming convention
- dodanie zasad nawigacji po dokumentacji
- zsynchronizowanie indeksow `_TASKS` i `_CHANGELOG` z nowym workflow

---

## Architecture

Docelowy stan po wykonaniu subtaska:

```text
model-traffic-manager/
|-- README.md
|-- AGENTS.md
`-- _docs/
    |-- README.md
    |-- _MVP/
    |   `-- README.md
    |-- _TASKS/
    |   |-- README.md
    |   |-- EXAMPLE_TASK.md
    |   |-- TASK-001-repo-governance-i-workflow-dokumentacji.md
    |   `-- TASK-001-01-agents-md-i-zasady-taskow-oraz-changelogow.md
    `-- _CHANGELOG/
        |-- README.md
        |-- EXAMPLE_CHANGELOG.md
        `-- 1-2026-03-13-repo-governance-task-workflow-and-agents-rules.md
```

---

## Pseudocode

```text
on_every_repo_task():
    create main task file TASK-XXX-slug.md
    create technical subtask TASK-XXX-01-slug.md
    if subtask becomes too large:
        split into TASK-XXX-01-01-slug.md or deeper
    write Documentation Updates Required in every work item
    execute work
    create changelog entry with all completed IDs
    update _docs/_TASKS/README.md board
    update _docs/_CHANGELOG/README.md index
```

---

## Implementation Order

1. Zidentyfikowac reguly wynikajace z `_docs/_MVP/`.
2. Zamienic je na instrukcje operacyjne w `AGENTS.md`.
3. Dolozyc zasady task hierarchy i changelog workflow.
4. Dodac indeksy i kontrolki nawigacyjne dla dokumentacji.
5. Zaktualizowac board oraz indeks changelogu.

---

## Testing Requirements

- sprawdzenie, ze `AGENTS.md` obejmuje zakres produktu, architekture, stack, routing, auth i testy
- sprawdzenie, ze README taskow opisuje glowny task, subtask i dalsze rozbicia
- sprawdzenie, ze changelog index zawiera nowy wpis
- sprawdzenie, ze dokumenty zmienione w tym tasku maja linki nawigacyjne

---

## Documentation Updates Required

- `README.md`
- `AGENTS.md`
- `_docs/README.md`
- `_docs/_TASKS/README.md`
- `_docs/_TASKS/EXAMPLE_TASK.md`
- `_docs/_CHANGELOG/README.md`
- `_docs/_CHANGELOG/EXAMPLE_CHANGELOG.md`
- `_docs/_CHANGELOG/1-2026-03-13-repo-governance-task-workflow-and-agents-rules.md`
