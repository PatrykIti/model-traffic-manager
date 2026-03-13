[README repo](../../README.md) | [_docs](../README.md)

# Kanban Tasks

Task board dla wszystkich work itemow w repo. Board obejmuje taski glowne, subtaski i dalsze rozbicia.

## Workflow

1. Dla kazdego zadania wykonywanego w repo utworz glowny task w `_docs/_TASKS/`.
2. Opis biznesowy zapisuj w pliku glownym: `TASK-001-slug.md`.
3. Techniczny plan, pseudokod i docelowa strukture repo zapisuj w subtasku: `TASK-001-01-slug.md`.
4. Jesli subtask jest zbyt duzy lub zbyt szeroki, rozbij go dalej, np. `TASK-001-01-01-slug.md`.
5. Dodaj work item do odpowiedniej tabeli na tym boardzie i zaktualizuj statystyki.
6. Po zakonczeniu pracy dodaj wpis do `_docs/_CHANGELOG/`, zaktualizuj indeks changelogu i przenies work item do **Done**.
7. Po kazdym tasku zaktualizuj dokumentacje, ktorej dotyka zmiana.

## Naming rules

- Glowny task: `TASK-001-slug.md`
- Subtask: `TASK-001-01-slug.md`
- Subtask subtaska: `TASK-001-01-01-slug.md`
- Uzywaj slugow ASCII z malych liter i lacznikow.

## Task file format

- Header lines:
  - `# TASK-XXX: Title`
  - `# FileName: TASK-XXX-slug.md`
- Required fields: `Priority`, `Category`, `Estimated Effort`, `Dependencies`, `Status`.
- Required sections: `Overview`, `Sub-Tasks`, `Testing Requirements`, `Documentation Updates Required`.
- Glowny task opisuje przede wszystkim sens biznesowy, scope i wynik.
- Subtaski opisuje sie technicznie: pseudokod, target structure, implementation order, ryzyka i decyzje.
- Jesli obszar dotyczy API lub security, dodaj sekcje `Security Contract`.
- Kazdy plik Markdown w dokumentacji musi miec kontrolki nawigacyjne.
- Wzor zawartosci: [EXAMPLE_TASK.md](./EXAMPLE_TASK.md).

## Status rules

- Dozwolone statusy: `To Do`, `In Progress`, `Done`.
- `In Progress` i `Done` musza miec date w pliku taska.
- Statystyki i tabela musza byc aktualizowane przy kazdej zmianie statusu.

## Changelog link

- Kazdy zakonczony work item musi byc uwzgledniony we wpisie w `_docs/_CHANGELOG/`.
- Jeden wpis changelogu moze obejmowac kilka zamknietych ID, ale musi wymieniac je jawnie.

## Statistics

- **To Do:** 0 work items
- **In Progress:** 0 work items
- **Done:** 2 work items

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
| TASK-001 | Repo Governance i Workflow Dokumentacji | High | Medium | Zasady pracy w repo, indeksy i AGENTS.md |
| TASK-001-01 | AGENTS.md i Zasady Taskow oraz Changelogow | High | Medium | Techniczne doprecyzowanie workflow i dokumentacji |
