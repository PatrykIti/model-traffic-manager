[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 70: Release Image Publishing and Automatic Semantic Release

**Date:** 2026-03-27
**Version:** 0.1.0
**Tasks:**
- TASK-053

---

## Key Changes

### Release Automation

- updated `semantic-release` so it now runs automatically on pushes to `main` while preserving manual `dry_run` support
- added a dedicated `release-image` workflow that publishes a real GHCR release image when a `v*` tag is created
- kept Azure-backed `release-validation` manual so it remains a deliberate release gate instead of an expensive post-release side effect
