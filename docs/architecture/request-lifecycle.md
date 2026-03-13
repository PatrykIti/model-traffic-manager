[Repository README](../../README.md) | [docs](../README.md) | [Architecture](./README.md)

# Request Lifecycle

Target request flow:

1. client calls a deployment endpoint
2. the API entrypoint maps the request into a use case
3. the use case loads deployment and health state
4. routing policy selects an upstream
5. outbound auth is prepared
6. request is sent
7. health/metrics are updated
8. response is returned

During bootstrap, only the health route path is implemented, but the repository structure is already shaped for the full lifecycle above.
