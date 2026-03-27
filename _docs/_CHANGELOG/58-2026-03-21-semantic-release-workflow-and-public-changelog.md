[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 58: Semantic Release Workflow and Public Changelog

**Date:** 2026-03-21
**Version:** 0.1.0
**Tasks:**
- TASK-041
- TASK-041-01
- TASK-041-02
- TASK-041-03

---

## Key Changes

### Release Workflow

- added a manual `semantic-release` GitHub Actions workflow that authenticates through a GitHub App token, prepares release notes from merged pull requests, updates `pyproject.toml`, creates the release commit and tag, and publishes a GitHub Release

### Pull-Request Release Metadata

- extended the pull-request template with `Release Impact` and categorized `Release Notes` sections
- added a repository-local semantic release parser that reads merged pull-request bodies and maps them to semantic version bumps plus categorized public release notes

### Public Release Notes Split

- added the root `CHANGELOG.md` as the public release-notes surface for published versions
- documented the separation between public release history in `CHANGELOG.md` and internal delivery history in `_docs/_CHANGELOG/`
