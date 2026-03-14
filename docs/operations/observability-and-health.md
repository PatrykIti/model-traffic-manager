[Repository README](../../README.md) | [docs](../README.md) | [Operations](./README.md)

# Observability and Health

The current runtime includes:

- structured logging setup
- health endpoints
- smoke tests for startup and health checks
- in-memory health-state persistence for upstreams
- cooldown and circuit-open transitions that affect routing eligibility
- a Redis-backed health-state adapter implementation behind the repository port

Future iterations will extend this into:

- metrics
- traces
- route decision logs
- operational troubleshooting flows
