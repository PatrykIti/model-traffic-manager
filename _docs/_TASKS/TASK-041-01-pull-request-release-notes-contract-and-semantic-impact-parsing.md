[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-041](./TASK-041-semantic-release-workflow-and-public-changelog-automation.md)

# TASK-041-01: Pull-Request Release-Notes Contract and Semantic Impact Parsing
# FileName: TASK-041-01-pull-request-release-notes-contract-and-semantic-impact-parsing.md

**Priority:** High
**Category:** Release Workflow
**Estimated Effort:** Medium
**Dependencies:** TASK-041
**Status:** **Done** (2026-03-21)

---

## Overview

Define a pull-request template contract that captures semantic release impact and categorized release notes, then implement parser logic that converts merged pull requests into version-bump and changelog inputs.

## Documentation Updates Required

- `.github/PULL_REQUEST_TEMPLATE.md`
- `scripts/release/semantic_release.py`
- `tests/unit/release/test_semantic_release.py`
