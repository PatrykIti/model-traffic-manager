from __future__ import annotations

from app.application.dto.chat_completion_request import ChatCompletionRequest
from app.application.dto.outbound_response import OutboundResponse
from app.application.ports.auth_header_builder import AuthHeaderBuilderPort
from app.application.ports.deployment_repository import DeploymentRepository
from app.application.ports.outbound_invoker import OutboundInvoker
from app.domain.entities.upstream import Upstream
from app.domain.errors import DeploymentNotFound, UpstreamSelectionError


class RouteChatCompletion:
    def __init__(
        self,
        deployment_repository: DeploymentRepository,
        auth_header_builder: AuthHeaderBuilderPort,
        outbound_invoker: OutboundInvoker,
        timeout_ms: int,
    ) -> None:
        self._deployment_repository = deployment_repository
        self._auth_header_builder = auth_header_builder
        self._outbound_invoker = outbound_invoker
        self._timeout_ms = timeout_ms

    def execute(self, request: ChatCompletionRequest) -> OutboundResponse:
        deployment = self._deployment_repository.get_deployment(request.deployment_id)
        if deployment is None:
            raise DeploymentNotFound(
                f"Deployment '{request.deployment_id}' was not found in the registry."
            )

        upstream = self._select_upstream(deployment.upstreams)
        headers = self._auth_header_builder.build(upstream.auth)
        return self._outbound_invoker.post_json(
            endpoint=upstream.endpoint,
            body=request.payload,
            headers=headers,
            timeout_ms=self._timeout_ms,
        )

    @staticmethod
    def _select_upstream(upstreams: tuple[Upstream, ...]) -> Upstream:
        if not upstreams:
            raise UpstreamSelectionError("Deployment does not define any upstreams.")
        return upstreams[0]
