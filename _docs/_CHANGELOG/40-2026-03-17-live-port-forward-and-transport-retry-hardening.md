[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 40: Live Port-Forward and Transport Retry Hardening

**Date:** 2026-03-17
**Version:** 0.1.0
**Tasks:**
- TASK-035

---

## Key Changes

### Port-forward stability

- switched local AKS test port-forwarding to a dynamically allocated local port
- waited for the forwarded `GET /health/ready` endpoint before starting pytest
- included the port-forward log in diagnostics to make local transport failures explicit

### Live-model suite resilience

- added retry handling for transient `httpx.TransportError` failures in the live-model suite
- kept the existing assertions for status codes, message content, cooldown, and circuit behavior
