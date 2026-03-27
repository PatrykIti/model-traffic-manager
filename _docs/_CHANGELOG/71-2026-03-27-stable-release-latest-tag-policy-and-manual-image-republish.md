[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 71: Stable Release `latest` Tag Policy and Manual Image Republish

**Date:** 2026-03-27
**Version:** 0.1.0
**Tasks:**
- TASK-054

---

## Key Changes

### Release Image Policy

- updated the release-image workflow so `latest` is only published for stable semantic version tags in the form `vX.Y.Z`
- clarified that the release-image workflow can be triggered manually to publish or republish an existing release tag when GHCR state needs to be recovered
