[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 43: Live Load-Balancing Transport Flake Hardening

**Date:** 2026-03-18
**Version:** 0.1.0
**Tasks:**
- TASK-038

---

## Key Changes

### Live Load-Balancing Suite

- added transient transport retry handling for the dedicated live load-balancing AKS suite
- restarted active-active distribution measurement windows whenever retries occurred so deterministic 8/2 assertions still reflect a clean observation window
- kept active-standby and failover expectations intact while reducing infra-driven flakiness
