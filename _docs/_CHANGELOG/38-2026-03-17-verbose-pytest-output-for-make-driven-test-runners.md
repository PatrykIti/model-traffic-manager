[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 38: Verbose Pytest Output for Make-Driven Test Runners

**Date:** 2026-03-17
**Version:** 0.1.0
**Tasks:**
- TASK-033

---

## Key Changes

### Local Make Targets

- added shared verbose pytest flags for direct `make test` and `make smoke` execution
- ensured local test runs show each test name instead of only a compact green summary

### Azure and AKS Runners

- updated the Azure-backed runner wrapper to use the same verbose pytest behavior
- printed the active pytest flags before executing the suite to make the runner output self-describing

### Documentation

- documented the new reporting behavior in local-development guidance
