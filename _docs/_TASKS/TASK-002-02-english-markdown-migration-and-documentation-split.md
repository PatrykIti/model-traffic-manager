[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-002-02: English Markdown Migration and Documentation Split
# FileName: TASK-002-02-english-markdown-migration-and-documentation-split.md

**Priority:** High
**Category:** Documentation Governance
**Estimated Effort:** Medium
**Dependencies:** TASK-002
**Status:** **Done** (2026-03-13)

---

## Overview

Technical subtask that moves repository Markdown content to English and formalizes the split between official docs and internal docs.

Scope:
- translate all repository Markdown files to English
- update `AGENTS.md` to make English the required Markdown language
- align task board, changelog index, and existing task/changelog entries
- keep navigation links and documentation ownership rules intact

---

## Pseudocode

```text
for each markdown file in the repository:
    preserve structure and navigation
    translate repository prose to English
    keep internal docs in _docs and official docs in docs
    update indexes, boards, and changelog references
```

---

## Implementation Order

1. Translate root repository Markdown files.
2. Translate internal documentation indexes, task files, and changelog entries.
3. Translate MVP planning documents.
4. Re-run docs guardrail checks to confirm the structure still holds.

---

## Testing Requirements

- verify that changed Markdown files are in English
- verify that navigation links remain valid after translation
- verify that the official/internal documentation split is explained consistently in root docs and internal docs

---

## Documentation Updates Required

- `AGENTS.md`
- `_docs/README.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/README.md`
- `_docs/_MVP/*.md`
- existing task files and changelog entries
