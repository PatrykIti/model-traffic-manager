[README repo](../../README.md) | [_docs](../README.md) | [_TASKS](./README.md)

# TASK-001: Repo Governance i Workflow Dokumentacji
# FileName: TASK-001-repo-governance-i-workflow-dokumentacji.md

**Priority:** High
**Category:** Repository Governance
**Estimated Effort:** Medium
**Dependencies:** Brak
**Status:** **Done** (2026-03-13)

---

## Overview

Zdefiniowanie zasad pracy dla glownego repo, tak aby kazda kolejna implementacja byla prowadzona wedlug jednego, jawnego workflow.

Cel biznesowy:
- miec jedno zrodlo prawdy dla zasad pracy w repo
- uporzadkowac workflow taskow, dokumentacji i changelogu
- zapewnic, ze przyszla implementacja routera bedzie zgodna z zalozeniami `_docs/_MVP/`

---

## Sub-Tasks

### TASK-001-01: AGENTS.md i zasady taskow/changelogow

**Status:** Done

Techniczne zlozenie zasad z `_docs/_MVP/`, reguly task hierarchy, README-ow, nawigacji i aktualizacji dokumentacji.

---

## Implementation Order

1. Przeanalizowac cale `_docs/`, w szczegolnosci `_MVP`, `_TASKS` i `_CHANGELOG`.
2. Zapisac zasady repo i workflow w glownym `AGENTS.md`.
3. Dodac brakujace indeksy dokumentacji (`README.md` w root i `_docs/`).
4. Zsynchronizowac README taskow i changelogu z nowym workflow.
5. Udokumentowac wykonana prace w changelogu i tablicy kanban.

---

## Testing Requirements

- sprawdzenie spojnosci zasad z dokumentami `_docs/_MVP/`
- sprawdzenie, ze task board i changelog index odzwierciedlaja wykonana prace
- sprawdzenie, ze nowe i zmienione pliki Markdown maja kontrolki nawigacyjne

---

## Documentation Updates Required

- utworzenie glownego `AGENTS.md`
- dodanie root `README.md`
- dodanie `_docs/README.md`
- aktualizacja `_docs/_TASKS/README.md`
- aktualizacja `_docs/_CHANGELOG/README.md`
- dodanie wpisu do `_docs/_CHANGELOG/`
