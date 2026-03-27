[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# Filename: 15-2026-03-14-basic-rate-limiting-and-concurrency-limiting.md

# 15. Basic Rate Limiting and Concurrency Limiting

**Date:** 2026-03-14
**Version:** 0.1.0
**Tasks:** TASK-015, TASK-015-01, TASK-015-02, TASK-015-03

## Key Changes

### Limiter contracts and adapters
- Added repository-owned request-rate and concurrency limiter ports plus a deployment-level limit guard.
- Added in-memory limiter adapters for the default runtime path.
- Added Redis-backed limiter adapters behind the same application ports.

### Runtime integration
- Integrated limiter enforcement into both proxy use cases before outbound dispatch.
- Added explicit rejection outcomes for request-rate saturation and concurrency saturation.
- Mapped limiter rejections to HTTP `429` and `503` responses at the API surface.

### Testing and documentation
- Added unit coverage for the limit guard and the local and Redis-backed limiter adapters.
- Added `integration-local` coverage for HTTP limiter rejection behavior.
- Updated official docs and tracking to reflect that deployment-level limiting is now implemented.
