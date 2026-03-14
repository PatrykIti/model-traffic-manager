[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# Filename: 11-2026-03-14-phase-2-embeddings-proxy-path-and-surface-parity.md

# 11. Phase 2 Embeddings Proxy Path and Surface Parity

**Date:** 2026-03-14
**Version:** 0.1.0
**Tasks:** TASK-011, TASK-011-01, TASK-011-02, TASK-011-03

## Key Changes

### Proxy path
- Added the embeddings proxy route: `POST /v1/embeddings/{deployment_id}`.
- Added `RouteEmbeddings` with the same deterministic single-upstream bootstrap behavior used by chat completions.
- Wired the new route into the application container and FastAPI app.

### Testing and config
- Added unit coverage for the embeddings use case.
- Added `integration-local` coverage for the embeddings route, including success, not-found, upstream failure, and API key scenarios.
- Extended the example router config so the default local setup exposes both current Phase 2 proxy paths.

### Documentation
- Updated the repository root and official docs to describe both implemented proxy endpoints.
- Marked `TASK-011` and its subtasks as done and synchronized the task board and changelog index.
