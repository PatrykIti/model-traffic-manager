[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-053: Release Image Publishing and Automatic Semantic Release
# FileName: TASK-053-release-image-publishing-and-automatic-semantic-release.md

**Priority:** High
**Category:** Release Automation
**Estimated Effort:** Medium
**Dependencies:** TASK-041, TASK-051
**Status:** **Done** (2026-03-27)

---

## Overview

Finish the first practical release automation loop for the repository:

1. run `semantic-release` automatically when changes land on `main`
2. publish a real GHCR release image when a semantic version tag is created
3. keep `release-validation` manual because it is expensive and acts more like a deliberate gate than a good post-release default

This keeps release metadata and release artifacts aligned without turning every push into an Azure spend event.

---

## Testing Requirements

- `semantic-release` still supports manual `dry_run`
- push-based release execution does not assume workflow-dispatch inputs exist
- release image publishing resolves the tagged ref and pushes semver plus `latest` tags to GHCR

---

## Documentation Updates Required

- `.github/workflows/semantic-release.yml`
- `.github/workflows/release-image.yml`
- `CONTRIBUTING.md`
- `_docs/_TASKS/TASK-053-release-image-publishing-and-automatic-semantic-release.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/README.md`
