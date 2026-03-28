[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-056: Release Image Trigger and Revision Reliability Fix
# FileName: TASK-056-release-image-trigger-and-revision-reliability-fix.md

**Priority:** High
**Category:** Release Reliability
**Estimated Effort:** Small
**Dependencies:** TASK-053, TASK-054
**Status:** **Done** (2026-03-28)

---

## Overview

Fix two reliability issues in the release-image workflow:

1. avoid relying on tag-push triggers that may be skipped when semantic release creates commits with CI-skip directives
2. derive the OCI revision label from the checked-out release tag instead of the event commit SHA

The release-image workflow now reacts to GitHub Release publication events and uses the tagged revision for image metadata.

As part of the same cleanup, the local lockfile version metadata is reconciled with the released project version.

---

## Testing Requirements

- release-image remains triggerable manually for an existing tag
- published release events resolve the correct tag automatically
- OCI revision metadata matches the checked-out tagged revision
- `uv.lock` version metadata matches `pyproject.toml`

---

## Documentation Updates Required

- `.github/workflows/release-image.yml`
- `_docs/_TASKS/TASK-056-release-image-trigger-and-revision-reliability-fix.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/README.md`
