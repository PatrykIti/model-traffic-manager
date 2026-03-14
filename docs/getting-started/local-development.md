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
- `POST /v1/chat/completions/{deployment_id}`
- `POST /v1/embeddings/{deployment_id}`

If you test the `api_key` path locally, expose secret material through environment variables referenced by `env://...` secret refs.

If you test the `managed_identity` path locally, rely on the Azure credential chain available to the router process. The default repository config still uses `none`, so local startup does not require Azure auth by default.
