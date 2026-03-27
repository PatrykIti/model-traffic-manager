[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-054: Stable Release `latest` Tag Policy and Manual Image Republish
# FileName: TASK-054-stable-release-latest-tag-policy-and-manual-image-republish.md

**Priority:** Medium
**Category:** Release Automation
**Estimated Effort:** Small
**Dependencies:** TASK-053
**Status:** **Done** (2026-03-27)

---

## Overview

Refine release-image publishing so the mutable `latest` tag is only assigned for stable release tags and the workflow is explicitly usable as a manual republish path for an existing release tag.

Goals:

1. avoid moving `latest` on prerelease or non-stable tags
2. keep the workflow usable for backlog recovery when a release tag already exists but its package publish must be rerun
3. document the policy in contributor-facing release guidance

---

## Testing Requirements

- stable tags in the form `vX.Y.Z` publish both the exact release tag and `latest`
- non-stable tags publish only the exact tag
- workflow dispatch remains usable for existing tags

---

## Documentation Updates Required

- `.github/workflows/release-image.yml`
- `CONTRIBUTING.md`
- `_docs/_TASKS/TASK-054-stable-release-latest-tag-policy-and-manual-image-republish.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/README.md`
