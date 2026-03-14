[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-014-01-02: `Retry-After` Parsing and Cooldown Semantics
# FileName: TASK-014-01-02-retry-after-parsing-and-cooldown-semantics.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Small
**Dependencies:** TASK-014-01
**Status:** **To Do**

---

## Overview

Define how `Retry-After` headers translate into bounded cooldown state.

Detailed work:
1. Parse supported `Retry-After` formats defensively.
2. Fall back to a repository-owned default cooldown when the header is missing or unusable.
3. Keep the stored cooldown value explicit in the health repository.

---

## Testing Requirements

- both delta-seconds and HTTP-date variants are covered
- invalid values fall back safely without crashing request handling
- cooldown windows remain deterministic in tests

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-014-01-02-retry-after-parsing-and-cooldown-semantics.md`
