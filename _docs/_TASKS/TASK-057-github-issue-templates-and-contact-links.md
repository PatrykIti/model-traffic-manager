[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-057: GitHub Issue Templates and Contact Links
# FileName: TASK-057-github-issue-templates-and-contact-links.md

**Priority:** Medium
**Category:** Repository UX and Community Support
**Estimated Effort:** Small
**Dependencies:** TASK-048
**Status:** **Done** (2026-03-28)

---

## Overview

Add first-class GitHub issue templates so public users have a cleaner entrypoint for bug reports and feature requests, while support and security traffic are redirected to the appropriate repository guidance.

Goals:

1. capture higher-signal bug reports
2. steer feature requests toward the actual router product boundary
3. redirect support and security cases away from the wrong public forms

---

## Testing Requirements

- issue template files are valid YAML and docs-guardrail compliant
- support and security contact links point to the correct repository guidance

---

## Documentation Updates Required

- `.github/ISSUE_TEMPLATE/bug-report.yml`
- `.github/ISSUE_TEMPLATE/feature-request.yml`
- `.github/ISSUE_TEMPLATE/config.yml`
- `_docs/_TASKS/TASK-057-github-issue-templates-and-contact-links.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/README.md`
