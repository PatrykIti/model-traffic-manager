from __future__ import annotations

from app.application.dto.embeddings_request import EmbeddingsRequest
from app.application.dto.outbound_response import OutboundResponse
from app.application.ports.auth_header_builder import AuthHeaderBuilderPort
from app.application.ports.deployment_repository import DeploymentRepository
from app.application.ports.outbound_invoker import OutboundInvoker
from app.domain.errors import (
    DeploymentNotFound,
    OutboundConnectionError,
    OutboundTimeoutError,
    UpstreamSelectionError,
)
from app.domain.services.tiered_failover_selector import TieredFailoverSelector


class RouteEmbeddings:
    def __init__(
        self,
        deployment_repository: DeploymentRepository,
        auth_header_builder: AuthHeaderBuilderPort,
        outbound_invoker: OutboundInvoker,
        routing_selector: TieredFailoverSelector,
        timeout_ms: int,
        max_attempts: int,
        retryable_status_codes: tuple[int, ...],
    ) -> None:
        self._deployment_repository = deployment_repository
        self._auth_header_builder = auth_header_builder
        self._outbound_invoker = outbound_invoker
        self._routing_selector = routing_selector
        self._timeout_ms = timeout_ms
        self._max_attempts = max_attempts
        self._retryable_status_codes = retryable_status_codes

    def execute(self, request: EmbeddingsRequest) -> OutboundResponse:
        deployment = self._deployment_repository.get_deployment(request.deployment_id)
        if deployment is None:
            raise DeploymentNotFound(
                f"Deployment '{request.deployment_id}' was not found in the registry."
            )

        if not deployment.upstreams:
            raise UpstreamSelectionError("Deployment does not define any upstreams.")

        attempted_upstream_ids: set[str] = set()
        last_response: OutboundResponse | None = None
        last_transport_error: OutboundTimeoutError | OutboundConnectionError | None = None

        for _ in range(self._max_attempts):
            selection = self._routing_selector.select(
                deployment_id=deployment.id,
                upstreams=deployment.upstreams,
                excluded_upstream_ids=frozenset(attempted_upstream_ids),
            )
            if selection is None:
                break

            attempted_upstream_ids.add(selection.upstream.id)
            headers = self._auth_header_builder.build(selection.upstream.auth)

            try:
                response = self._outbound_invoker.post_json(
                    endpoint=selection.upstream.endpoint,
                    body=request.payload,
                    headers=headers,
                    timeout_ms=self._timeout_ms,
                )
            except (OutboundTimeoutError, OutboundConnectionError) as exc:
                last_transport_error = exc
                if not self._can_retry_transport_failure(
                    attempted_upstream_ids=attempted_upstream_ids,
                    upstream_count=len(deployment.upstreams),
                ):
                    raise
                continue

            last_response = response
            if not self._is_retriable_response(response):
                return response
            if not self._can_retry_response(
                attempted_upstream_ids=attempted_upstream_ids,
                upstream_count=len(deployment.upstreams),
            ):
                return response

        if last_response is not None:
            return last_response
        if last_transport_error is not None:
            raise last_transport_error
        raise UpstreamSelectionError("No upstream could be selected for the request.")

    def _is_retriable_response(self, response: OutboundResponse) -> bool:
        return response.status_code in self._retryable_status_codes

    def _can_retry_response(self, attempted_upstream_ids: set[str], upstream_count: int) -> bool:
        return len(attempted_upstream_ids) < upstream_count

    def _can_retry_transport_failure(
        self,
        attempted_upstream_ids: set[str],
        upstream_count: int,
    ) -> bool:
        return len(attempted_upstream_ids) < upstream_count
