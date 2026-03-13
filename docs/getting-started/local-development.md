[Repository README](../../README.md) | [docs](../README.md) | [Getting Started](./README.md)

# Local Development

Use the canonical local command path:

```text
make bootstrap
make check
make run
```

What each command does:

- `make bootstrap` syncs the locked environment with `uv`
- `make check` runs lint, type-check, and tests
- `make run` starts the bootstrap FastAPI app

Environment defaults are documented in [`.env.example`](../../.env.example), and the example runtime config lives in [`configs/example.router.yaml`](../../configs/example.router.yaml).

Useful first endpoints after startup:

- `GET /health/live`
- `GET /health/ready`
- `GET /deployments`
