[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-011-03: `integration-local` Coverage, Docs, and Example Config Alignment
# FileName: TASK-011-03-integration-local-coverage-docs-and-example-config-alignment.md

**Priority:** High
**Category:** Documentation and Validation
**Estimated Effort:** Medium
**Dependencies:** TASK-011
**Status:** **Done** (2026-03-14)

---

## Overview

Prove the embeddings proxy path locally and update the public-facing explanation of the current feature surface.

Detailed work:
1. Add `integration-local` coverage with mocked upstream behavior.
2. Update the relevant official docs and implementation status pages.
3. Extend example configuration or examples only as far as the new endpoint requires.

---

## Testing Requirements

- integration tests cover success, not-found, and a representative upstream failure
- the official docs reflect both currently implemented proxy paths
- example configuration remains valid after documentation updates

---

## Documentation Updates Required

- `docs/getting-started/implementation-status.md`
- `docs/getting-started/overview.md`
- `docs/getting-started/local-development.md`
- `docs/architecture/system-overview.md`
- `docs/architecture/request-lifecycle.md`
- `docs/configuration/deployment-and-upstreams.md`
- `README.md`
- `configs/example.router.yaml`
- `_docs/_TASKS/TASK-011-03-integration-local-coverage-docs-and-example-config-alignment.md`
