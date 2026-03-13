[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# Filename: 9-2026-03-13-phase-2-single-upstream-routing-and-first-proxy-path.md

# 9. Phase 2 Single-Upstream Routing and First Proxy Path

**Date:** 2026-03-13
**Version:** 0.1.0
**Tasks:** TASK-009, TASK-009-01, TASK-009-01-01, TASK-009-01-02, TASK-009-02, TASK-009-02-01, TASK-009-02-02, TASK-009-02-03, TASK-009-03, TASK-009-03-01, TASK-009-03-02, TASK-009-04, TASK-009-04-01, TASK-009-04-02, TASK-009-05

## Key Changes

### Proxy path
- Added the first real request proxy route: `POST /v1/chat/completions/{deployment_id}`.
- Added `RouteChatCompletion` with deterministic single-upstream selection.

### Outbound and auth plumbing
- Added outbound invoker contracts and an `httpx` implementation.
- Added bootstrap secret resolution from `env://...` references.
- Added auth header building for `none` and `api_key`.

### Testing
- Added unit coverage for auth, secret resolution, outbound invocation, and use case orchestration.
- Added `integration-local` coverage for the full chat proxy path, including success, not-found, upstream failure, and API key scenarios.

### Documentation
- Updated official docs to reflect the first real proxy path and the current bootstrap auth support.
