[Repository README](../../README.md) | [docs](../README.md) | [Routing](./README.md)

# Failover and Health

The router is expected to distinguish:

- healthy
- rate limited
- quota exhausted
- cooldown
- unhealthy
- circuit open

The MVP health model includes:

- cooldown after `429`
- circuit breaker per upstream
- retry only for retriable failures
- observable decision reasons for failover

Current implementation status:

- these health and failover behaviors are planned but not implemented yet
- the repository currently proxies chat completions through a single selected upstream without health-state persistence
