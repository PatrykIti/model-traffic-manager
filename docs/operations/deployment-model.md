[Repository README](../../README.md) | [docs](../README.md) | [Operations](./README.md)

# Deployment Model

The current repository supports:

- local execution through `make run`
- quality validation through `make check`
- container build through `make docker-build`

Current outbound auth posture:

- `managed_identity` is the preferred secretless mode for Azure-native upstreams
- `api_key` remains available as a fallback where needed
- Managed Identity tokens are cached in-memory per router instance
As implementation grows further, this section should expand into AKS deployment guidance, workload identity expectations, and production runtime operations.

For AKS-specific configuration delivery options, see [aks-configuration-delivery.md](./aks-configuration-delivery.md).
