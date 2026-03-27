[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 46: Redis-Backed Multi-Replica AKS Validation

**Date:** 2026-03-18
**Version:** 0.1.0
**Tasks:**
- TASK-029-06
- TASK-029-06-01
- TASK-029-06-02
- TASK-029-06-03

---

## Key Changes

### Redis-Backed AKS Profile

- added a dedicated `e2e-aks-redis` scope with two router replicas and an in-cluster Redis backend
- rendered a dedicated router config for shared cooldown, circuit, request-rate, and concurrency scenarios
- added deterministic in-cluster mock upstreams for Redis-backed multi-replica validation

### Runner and Test Surface

- added `make e2e-aks-redis-local`
- extended the shared Azure/AKS runner with per-replica pod port-forwards for the Redis suite
- added a live suite that validates shared request-rate, concurrency, cooldown, and circuit-open behavior across replicas

### Documentation

- documented the new Redis-backed validation profile in testing-level, local-development, and implementation-status docs
