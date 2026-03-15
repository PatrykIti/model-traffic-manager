[Repository README](../../README.md) | [docs](../README.md) | [Configuration](./README.md)

# Shared Services

`shared_services` describe non-LLM dependencies that matter to backend or platform workflows.

They are intentionally separate from `deployments`:

- `deployments` expose chat and embeddings traffic to clients
- `shared_services` describe backend-facing dependencies and their execution mode

## Current Execution Modes

### `direct_backend_access`

Use this when the backend should call the service directly.

Current behavior:

- the service is visible in `GET /shared-services`
- `POST /v1/shared-services/{service_id}` is rejected for this mode
- the router acts as a semantic registry, not as the execution surface

Typical fit:

- Azure Storage
- large object and blob workloads
- services where provider-managed availability already covers the main failover concern

### `router_proxy`

Use this when the backend should call the service through the router.

Current behavior:

- the service is visible in `GET /shared-services`
- `POST /v1/shared-services/{service_id}` is accepted
- the request body must be JSON
- router-managed auth, observability, and limiter behavior apply

## Routing Strategies for `router_proxy`

### `single_endpoint`

Use exactly one upstream when the router should execute the call but should not apply router-managed failover.

This is a good fit when:

- the service has one semantic endpoint
- provider-managed availability already exists
- or explicit multi-upstream failover would add cost without operational value

### `tiered_failover`

Use multiple upstreams and the same health-aware failover model used by model traffic.

This is a good fit when:

- the service is stateless HTTP/JSON
- explicit multi-upstream failover is needed
- operator-visible routing decisions are valuable

## Important Boundary

The router is not intended to become a generic data-plane gateway.

That means:

- no generic blob upload/download proxy by default
- no automatic assumption that every shared service should inherit LLM-style failover
- no expansion into a catch-all backend integration layer

For provider-managed storage and large object traffic, the preferred model remains:

- backend direct access with Managed Identity
- router-held registry metadata where useful

## Current API Surface

- `GET /shared-services`
  returns the validated shared-service registry
- `POST /v1/shared-services/{service_id}`
  executes router-proxied HTTP/JSON shared services only

## Full Example Files

Ready-to-copy example router configs:

- [shared-services-direct-backend-access.router.yaml](../../configs/examples/shared-services-direct-backend-access.router.yaml)
- [shared-services-router-proxy-single-endpoint.router.yaml](../../configs/examples/shared-services-router-proxy-single-endpoint.router.yaml)
- [shared-services-router-proxy-tiered-failover.router.yaml](../../configs/examples/shared-services-router-proxy-tiered-failover.router.yaml)

These files show the full router config shape, not only the `shared_services` fragment.

## Example Shapes

Direct backend access:

```yaml
shared_services:
  conversation_archive:
    transport: http_json
    access_mode: direct_backend_access
    provider_managed_availability: true
    provider: azure_storage
    account: conversation-archive
    region: westeurope
    endpoint: https://conversation-archive.blob.core.windows.net
    auth:
      mode: managed_identity
      scope: https://storage.azure.com/.default
```

Router-proxied single endpoint:

```yaml
shared_services:
  transcript_registry:
    transport: http_json
    access_mode: router_proxy
    provider_managed_availability: true
    routing_strategy: single_endpoint
    limits:
      max_concurrency: 10
      request_rate_per_second: 5
    upstreams:
      - id: transcript-registry-primary
        provider: internal_api
        account: platform
        region: local
        tier: 0
        weight: 100
        endpoint: https://example.invalid/shared/transcript-registry
        auth:
          mode: none
```

Router-proxied tiered failover:

```yaml
shared_services:
  transcript_search:
    transport: http_json
    access_mode: router_proxy
    provider_managed_availability: false
    routing_strategy: tiered_failover
    limits:
      max_concurrency: 10
      request_rate_per_second: 5
    upstreams:
      - id: primary
        provider: internal_api
        account: platform
        region: westeurope
        tier: 0
        weight: 100
        endpoint: https://example.invalid/shared-primary
        auth:
          mode: none
      - id: secondary
        provider: internal_api
        account: platform
        region: northeurope
        tier: 1
        weight: 100
        endpoint: https://example.invalid/shared-secondary
        auth:
          mode: none
```
