[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 44: Integration-Azure Chat and Embeddings Provider Probes

**Date:** 2026-03-18
**Version:** 0.1.0
**Tasks:**
- TASK-029-02
- TASK-029-02-01
- TASK-029-02-02
- TASK-029-02-03

---

## Key Changes

### Azure-Only Provider Probes

- added a dedicated `integration-azure-chat` scope with live Azure OpenAI chat deployment provisioning
- added a dedicated `integration-azure-embeddings` scope with live Azure OpenAI embeddings deployment provisioning
- added separate live test suites that call Azure OpenAI directly through the repository auth and outbound adapters

### Local Runner Surface

- added separate `make integration-azure-chat-local` and `make integration-azure-embeddings-local` commands
- extended the shared Azure test runner to export profile-specific outputs JSON paths and activation flags

### Documentation

- documented the new split integration-azure profiles in local-development and testing-level docs
- extended `.env.example` with the new runner-managed markers and outputs-path variables
