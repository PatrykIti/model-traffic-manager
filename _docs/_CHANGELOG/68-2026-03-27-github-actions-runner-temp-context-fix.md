[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 68: GitHub Actions `runner.temp` Context Fix

**Date:** 2026-03-27
**Version:** 0.1.0
**Tasks:**
- TASK-051

---

## Key Changes

### Workflow Parser Compatibility

- removed invalid job-level `runner.temp` expressions from the nightly and release validation workflows
- kept artifact handling behavior unchanged by relying on the existing shell-runner fallback to `RUNNER_TEMP` on GitHub-hosted runners
