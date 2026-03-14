[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# Filename: 12-2026-03-14-phase-3-managed-identity-outbound-auth-and-token-cache.md

# 12. Phase 3 Managed Identity Outbound Auth and Token Cache

**Date:** 2026-03-14
**Version:** 0.1.0
**Tasks:** TASK-012, TASK-012-01, TASK-012-01-01, TASK-012-01-02, TASK-012-02, TASK-012-02-01, TASK-012-02-02, TASK-012-03

## Key Changes

### Managed Identity auth
- Added a repository-owned token provider port and a Managed Identity adapter based on `DefaultAzureCredential`.
- Added in-memory token caching keyed by `(auth_mode, client_id, scope)` with refresh buffering before expiry.
- Extended the auth header builder so chat and embeddings can send bearer tokens for `managed_identity`.

### Runtime wiring and error handling
- Registered the Managed Identity token provider in the bootstrap container.
- Added outbound auth error translation so token acquisition failures surface through the API without leaking Azure SDK exceptions.
- Kept the existing `none` and `api_key` auth paths intact.

### Testing and documentation
- Added unit coverage for Managed Identity token caching and auth header generation.
- Added `integration-local` coverage for both proxy routes using stub token providers.
- Updated official docs and tracking to reflect that Managed Identity is now implemented.
