[README repo](../../README.md) | [_docs](../README.md)

# Changelog

Projektowy changelog wykonanej pracy.

Tabela **Index** ponizej pelni role boardu changelogu i pokazuje, co zostalo zrobione oraz kiedy.

## Workflow

1. Po zakonczeniu taska lub zestawu taskow z jednej sesji pracy utworz nowy plik w `_docs/_CHANGELOG/`.
2. Uzyj nazewnictwa z sekcji ponizej i wpisz wszystkie zamkniete ID taskow/subtaskow.
3. Dodaj wiersz do tabeli **Index** z numerem, data, tytulem i typem zmiany.
4. Zsynchronizuj ten indeks z boardem w `_docs/_TASKS/README.md`.

## File naming

- Format: `{N}-{YYYY-MM-DD}-short-title.md`
- Example: `1-2025-11-22-project-init-and-rpc.md`
- `N` rosnie sekwencyjnie i nigdy nie jest uzywany ponownie.

## Entry format (minimum)

- Title line with No. and short title.
- `Date`, `Version`, `Tasks`.
- Sekcje `Key Changes` pogrupowane po obszarach.
- Wpis ma byc zwiezly, ale ma jasno tlumaczyc co zostalo zrobione.
- Wzor: [EXAMPLE_CHANGELOG.md](./EXAMPLE_CHANGELOG.md).

## Index

| No. | Date | Title | Type |
|-----|------|-------|------|
| 1 | 2026-03-13 | Repo governance, task workflow and AGENTS rules | docs/process |
