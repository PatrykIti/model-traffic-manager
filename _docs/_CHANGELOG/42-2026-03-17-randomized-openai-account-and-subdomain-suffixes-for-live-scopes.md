[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 42: Randomized OpenAI Account and Subdomain Suffixes for Live Scopes

**Date:** 2026-03-17
**Version:** 0.1.0
**Tasks:**
- TASK-037

---

## Key Changes

### Live Azure OpenAI Naming

- added random suffix generation for live-model and live-embeddings Azure OpenAI account names
- applied the same randomized value to the default custom subdomain name
- ensured the uniqueness-carrying suffix is preserved inside the 24-character Cognitive Services account-name limit

### Operator Guidance

- documented that repeated live Azure OpenAI validation runs now avoid soft-delete naming conflicts by default
