[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-041: Semantic Release Workflow and Public Changelog Automation
# FileName: TASK-041-semantic-release-workflow-and-public-changelog-automation.md

**Priority:** High
**Category:** Release Automation
**Estimated Effort:** Medium
**Dependencies:** TASK-040-06, TASK-040-07
**Status:** **Done** (2026-03-21)

---

## Overview

Add a repository-level semantic release workflow that publishes versioned releases with a public root `CHANGELOG.md`, while keeping `_docs/_CHANGELOG/` dedicated to internal task-level delivery history.

---

## Sub-Tasks

### TASK-041-01: Pull-request release-notes contract and semantic impact parsing

**Status:** Done (2026-03-21)

Add a structured `Release Impact` and `Release Notes` contract to the pull-request template and implement a parser that can infer semantic version bumps plus categorized release notes from merged pull-request bodies.

### TASK-041-02: GitHub App-backed semantic release workflow and tag publication

**Status:** Done (2026-03-21)

Add a manual GitHub Actions release workflow that authenticates with the repository GitHub App, updates versioned files, creates the release commit and tag, and publishes a GitHub Release.

### TASK-041-03: Public changelog and contributor documentation alignment

**Status:** Done (2026-03-21)

Add the root `CHANGELOG.md`, explain the split between public release notes and internal delivery changelogs, and document the required GitHub App permissions and branch-bypass expectations for release automation.

---

## Security Contract

- The release workflow must authenticate with a repository-installed GitHub App rather than a user PAT as the default path.
- The GitHub App must have only the repository permissions required for release publication and changelog/tag updates.
- Branch-protection or ruleset bypass should be granted to the GitHub App, not to an over-privileged personal token.

---

## Testing Requirements

- validate the new workflow with the repository workflow validator
- add unit tests for release-note parsing and semantic version bump logic
- run the release script in dry-run mode to confirm output generation without mutating tags or repository state

---

## Documentation Updates Required

- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/workflows/semantic-release.yml`
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `README.md`
- `_docs/_TASKS/TASK-041-semantic-release-workflow-and-public-changelog-automation.md`
- `_docs/_TASKS/TASK-041-01-pull-request-release-notes-contract-and-semantic-impact-parsing.md`
- `_docs/_TASKS/TASK-041-02-github-app-backed-semantic-release-workflow-and-tag-publication.md`
- `_docs/_TASKS/TASK-041-03-public-changelog-and-contributor-documentation-alignment.md`
