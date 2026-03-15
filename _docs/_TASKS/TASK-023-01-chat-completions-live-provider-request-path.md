[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-023-01: Chat Completions Live Provider Request Path
# FileName: TASK-023-01-chat-completions-live-provider-request-path.md

**Priority:** High
**Category:** Higher-Level Validation
**Estimated Effort:** Small
**Dependencies:** TASK-023
**Status:** **To Do**

---

## Overview

Add a real Azure-backed chat completions request path to `integration-azure`
without involving AKS deployment behavior.

## Testing Requirements

- the suite proves a real provider chat response through the repository runtime
- the Azure-backed test stays cheaper and faster than the AKS live suite

## Documentation Updates Required

- `_docs/_TASKS/TASK-023-01-chat-completions-live-provider-request-path.md`
