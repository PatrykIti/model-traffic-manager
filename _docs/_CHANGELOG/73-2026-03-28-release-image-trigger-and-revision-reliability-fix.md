[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 73: Release Image Trigger and Revision Reliability Fix

**Date:** 2026-03-28
**Version:** 0.1.1
**Tasks:**
- TASK-056

---

## Key Changes

### Release Image Workflow

- changed the release-image workflow to react to published GitHub Releases instead of relying on tag-push events that may be skipped by CI-skip directives
- updated OCI revision metadata so release images now record the actual tagged revision being published

### Version Metadata

- reconciled the lockfile package-version metadata with the current released project version
