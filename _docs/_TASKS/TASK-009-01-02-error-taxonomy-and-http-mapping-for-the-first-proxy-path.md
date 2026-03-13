[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-009-01-02: Error Taxonomy and HTTP Mapping for the First Proxy Path
# FileName: TASK-009-01-02-error-taxonomy-and-http-mapping-for-the-first-proxy-path.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Small
**Dependencies:** TASK-009-01
**Status:** To Do

---

## Overview

Define the minimum error surface for the first routing path.

---

## Target Error Classes

- `DeploymentNotFound`
- config/secret resolution error for `api_key`
- upstream timeout
- upstream connection error
- generic upstream error passthrough or mapped 5xx

---

## HTTP Mapping Target

- deployment missing -> `404`
- invalid secret reference or missing secret material -> `500` for now
- timeout / connection error -> `502` or `504` depending on chosen policy
- successful upstream response -> preserve upstream status

---

## Testing Requirements

- each mapped error path has unit or integration coverage
- mapping remains simple enough to evolve later when full failure classification is introduced

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-009-01-02-error-taxonomy-and-http-mapping-for-the-first-proxy-path.md`
