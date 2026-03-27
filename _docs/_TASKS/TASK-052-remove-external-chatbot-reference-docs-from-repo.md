[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-052: Remove External Chatbot Reference Docs from the Repository
# FileName: TASK-052-remove-external-chatbot-reference-docs-from-repo.md

**Priority:** Medium
**Category:** Internal Documentation Cleanup
**Estimated Effort:** Small
**Dependencies:** TASK-048
**Status:** **Done** (2026-03-27)

---

## Overview

Remove the higher-level chatbot platform and SaaS orchestration reference documents from this repository now that they live elsewhere.

The goal is to keep `_docs/` focused on delivery and implementation guidance for `model-traffic-manager` itself instead of carrying external product documentation that belongs in another location.

---

## Testing Requirements

- active internal documentation indexes no longer point to deleted files
- repository Markdown guardrails still pass after the deletion

---

## Documentation Updates Required

- `_docs/README.md`
- `_docs/_TASKS/TASK-052-remove-external-chatbot-reference-docs-from-repo.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/README.md`
