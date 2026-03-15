from __future__ import annotations

from math import ceil

from app.application.deployment_limit_guard import DeploymentLimitGuard
from app.application.dto.chat_completion_request import ChatCompletionRequest
from app.application.dto.outbound_response import OutboundResponse
from app.application.dto.runtime_event import RuntimeEvent
from app.application.ports.auth_header_builder import AuthHeaderBuilderPort
from app.application.ports.deployment_repository import DeploymentRepository
from app.application.ports.health_state_repository import HealthStateRepository
from app.application.ports.outbound_invoker import OutboundInvoker
from app.application.ports.runtime_event_recorder import RuntimeEventRecorder
from app.domain.entities.upstream import Upstream
from app.domain.errors import (
    DeploymentContractMismatchError,
    DeploymentNotFound,
    OutboundConnectionError,
    OutboundTimeoutError,
    UpstreamSelectionError,
)
from app.domain.services.health_state_policy import HealthStatePolicy
from app.domain.services.tiered_failover_selector import RouteSelection, TieredFailoverSelector
from app.domain.services.upstream_failure_classifier import UpstreamFailureClassifier
from app.domain.value_objects.failure_classification import FailureClassification, FailureReason
from app.domain.value_objects.health_state import HealthState, HealthStatus


class RouteChatCompletion:
    def __init__(
        self,
        deployment_repository: DeploymentRepository,
        auth_header_builder: AuthHeaderBuilderPort,
        outbound_invoker: OutboundInvoker,
        deployment_limit_guard: DeploymentLimitGuard,
        health_state_repository: HealthStateRepository,
        failure_classifier: UpstreamFailureClassifier,
        health_state_policy: HealthStatePolicy,
        routing_selector: TieredFailoverSelector,
        timeout_ms: int,
        max_attempts: int,
        retryable_status_codes: tuple[int, ...],
        runtime_event_recorder: RuntimeEventRecorder | None = None,
    ) -> None:
        self._deployment_repository = deployment_repository
        self._auth_header_builder = auth_header_builder
        self._outbound_invoker = outbound_invoker
        self._deployment_limit_guard = deployment_limit_guard
        self._health_state_repository = health_state_repository
        self._failure_classifier = failure_classifier
        self._health_state_policy = health_state_policy
        self._routing_selector = routing_selector
        self._runtime_event_recorder = runtime_event_recorder
        self._timeout_ms = timeout_ms
        self._max_attempts = max_attempts
        self._retryable_status_codes = retryable_status_codes

    def execute(self, request: ChatCompletionRequest) -> OutboundResponse:
        deployment = self._deployment_repository.get_deployment(request.deployment_id)
        if deployment is None:
            raise DeploymentNotFound(
                f"Deployment '{request.deployment_id}' was not found in the registry."
            )
        if not deployment.supports_chat_completions():
            raise DeploymentContractMismatchError(
                f"Deployment '{request.deployment_id}' does not support chat completions."
            )

        if not deployment.upstreams:
            raise UpstreamSelectionError("Deployment does not define any upstreams.")

        lease_id = self._deployment_limit_guard.acquire(
            deployment,
            request_id=request.request_id,
            endpoint_kind="chat_completions",
        )
        try:
            states = self._load_states(deployment.id, deployment.upstreams)
            attempted_upstream_ids: set[str] = set()
            probe_blocked_upstream_ids: set[str] = set()
            last_response: OutboundResponse | None = None
            last_transport_error: OutboundTimeoutError | OutboundConnectionError | None = None
            next_failover_reason: str | None = None

            for attempt in range(1, self._max_attempts + 1):
                selection_result = self._select_candidate(
                    deployment_id=deployment.id,
                    upstreams=deployment.upstreams,
                    states=states,
                    attempted_upstream_ids=attempted_upstream_ids,
                    probe_blocked_upstream_ids=probe_blocked_upstream_ids,
                )
                if selection_result is None:
                    break
                selection, has_half_open_probe = selection_result

                attempted_upstream_ids.add(selection.upstream.id)
                probe_blocked_upstream_ids.clear()
                headers = self._auth_header_builder.build(selection.upstream.auth)
                self._record_event(
                    RuntimeEvent(
                        event_type="route_selected",
                        endpoint_kind="chat_completions",
                        deployment_id=deployment.id,
                        request_id=request.request_id,
                        attempt=attempt,
                        upstream_id=selection.upstream.id,
                        provider=selection.upstream.provider,
                        account=selection.upstream.account,
                        region=selection.upstream.region,
                        selected_tier=selection.selected_tier,
                        decision_reason=selection.reason,
                        failover_reason=next_failover_reason or selection.failover_reason,
                        rejected_candidates=selection.rejected_candidates,
                    )
                )

                try:
                    response = self._outbound_invoker.post_json(
                        endpoint=selection.upstream.endpoint,
                        body=request.payload,
                        headers=headers,
                        timeout_ms=self._timeout_ms,
                    )
                except (OutboundTimeoutError, OutboundConnectionError) as exc:
                    if has_half_open_probe:
                        self._health_state_repository.clear_half_open_probe(
                            deployment.id,
                            selection.upstream.id,
                        )
                    failure = self._failure_classifier.classify_transport_error(exc)
                    states[selection.upstream.id] = self._health_state_policy.record_failure(
                        states.get(selection.upstream.id, HealthState()),
                        failure,
                    )
                    self._health_state_repository.set_state(
                        deployment.id,
                        selection.upstream.id,
                        states[selection.upstream.id],
                    )
                    self._record_event(
                        RuntimeEvent(
                            event_type="health_state_updated",
                            endpoint_kind="chat_completions",
                            deployment_id=deployment.id,
                            request_id=request.request_id,
                            attempt=attempt,
                            upstream_id=selection.upstream.id,
                            selected_tier=selection.selected_tier,
                            decision_reason=selection.reason,
                            failover_reason=next_failover_reason or selection.failover_reason,
                            failure_reason=failure.reason.value,
                            health_status=states[selection.upstream.id].status.value,
                            outcome="retryable_transport_failure",
                        )
                    )
                    last_transport_error = exc
                    next_failover_reason = failure.reason.value
                    if not self._can_retry_failure(
                        failure=failure,
                        attempted_upstream_ids=attempted_upstream_ids,
                        upstream_count=len(deployment.upstreams),
                    ):
                        raise
                    continue

                if response.status_code < 400:
                    if has_half_open_probe:
                        self._health_state_repository.clear_half_open_probe(
                            deployment.id,
                            selection.upstream.id,
                        )
                    states[selection.upstream.id] = self._health_state_policy.record_success(
                        states.get(selection.upstream.id, HealthState())
                    )
                    self._health_state_repository.set_state(
                        deployment.id,
                        selection.upstream.id,
                        states[selection.upstream.id],
                    )
                    self._record_event(
                        RuntimeEvent(
                            event_type="request_completed",
                            endpoint_kind="chat_completions",
                            deployment_id=deployment.id,
                            request_id=request.request_id,
                            attempt=attempt,
                            upstream_id=selection.upstream.id,
                            selected_tier=selection.selected_tier,
                            decision_reason=selection.reason,
                            failover_reason=next_failover_reason or selection.failover_reason,
                            outcome="success",
                            status_code=response.status_code,
                        )
                    )
                    return response

                last_response = response
                failure = self._failure_classifier.classify_response(
                    status_code=response.status_code,
                    headers=response.headers,
                    json_body=response.json_body,
                    text_body=response.text_body,
                )
                if not self._is_retriable_failure(failure, response):
                    if has_half_open_probe:
                        self._health_state_repository.clear_half_open_probe(
                            deployment.id,
                            selection.upstream.id,
                        )
                    self._record_event(
                        RuntimeEvent(
                            event_type="request_completed",
                            endpoint_kind="chat_completions",
                            deployment_id=deployment.id,
                            request_id=request.request_id,
                            attempt=attempt,
                            upstream_id=selection.upstream.id,
                            selected_tier=selection.selected_tier,
                            decision_reason=selection.reason,
                            failover_reason=next_failover_reason or selection.failover_reason,
                            outcome="non_retriable_response",
                            failure_reason=failure.reason.value,
                            status_code=response.status_code,
                        )
                    )
                    return response

                if has_half_open_probe:
                    self._health_state_repository.clear_half_open_probe(
                        deployment.id,
                        selection.upstream.id,
                    )
                states[selection.upstream.id] = self._health_state_policy.record_failure(
                    states.get(selection.upstream.id, HealthState()),
                    failure,
                )
                self._health_state_repository.set_state(
                    deployment.id,
                    selection.upstream.id,
                    states[selection.upstream.id],
                )
                self._record_event(
                    RuntimeEvent(
                        event_type="health_state_updated",
                        endpoint_kind="chat_completions",
                        deployment_id=deployment.id,
                        request_id=request.request_id,
                        attempt=attempt,
                        upstream_id=selection.upstream.id,
                        selected_tier=selection.selected_tier,
                        decision_reason=selection.reason,
                        failover_reason=next_failover_reason or selection.failover_reason,
                        failure_reason=failure.reason.value,
                        health_status=states[selection.upstream.id].status.value,
                        retry_after_seconds=failure.retry_after_seconds,
                        outcome="retryable_response",
                        status_code=response.status_code,
                    )
                )
                next_failover_reason = failure.reason.value
                if not self._can_retry_failure(
                    failure=failure,
                    attempted_upstream_ids=attempted_upstream_ids,
                    upstream_count=len(deployment.upstreams),
                ):
                    self._record_event(
                        RuntimeEvent(
                            event_type="request_completed",
                            endpoint_kind="chat_completions",
                            deployment_id=deployment.id,
                            request_id=request.request_id,
                            attempt=attempt,
                            upstream_id=selection.upstream.id,
                            selected_tier=selection.selected_tier,
                            decision_reason=selection.reason,
                            failover_reason=next_failover_reason or selection.failover_reason,
                            outcome="retriable_response_exhausted",
                            failure_reason=failure.reason.value,
                            status_code=response.status_code,
                        )
                    )
                    return response

            if last_response is not None:
                return last_response
            if last_transport_error is not None:
                raise last_transport_error
            raise UpstreamSelectionError(
                "No healthy upstream is currently available for the request."
            )
        finally:
            self._deployment_limit_guard.release(deployment.id, lease_id)

    def _is_retriable_failure(
        self,
        failure: FailureClassification,
        response: OutboundResponse | None = None,
    ) -> bool:
        if not failure.retriable:
            return False
        if failure.reason in {
            FailureReason.TIMEOUT,
            FailureReason.NETWORK_ERROR,
            FailureReason.QUOTA_EXHAUSTED,
        }:
            return True
        return response is not None and response.status_code in self._retryable_status_codes

    def _can_retry_failure(
        self,
        failure: FailureClassification,
        attempted_upstream_ids: set[str],
        upstream_count: int,
    ) -> bool:
        return failure.retriable and len(attempted_upstream_ids) < upstream_count

    def _load_states(
        self,
        deployment_id: str,
        upstreams: tuple[Upstream, ...],
    ) -> dict[str, HealthState]:
        upstream_ids = tuple(upstream.id for upstream in upstreams)
        states = self._health_state_repository.get_states(deployment_id, upstream_ids)
        normalized_states: dict[str, HealthState] = {}

        for upstream in upstreams:
            state = states.get(upstream.id, HealthState())
            normalized_state = self._health_state_policy.normalize(state)
            normalized_states[upstream.id] = normalized_state
            if normalized_state != state:
                self._health_state_repository.set_state(
                    deployment_id,
                    upstream.id,
                    normalized_state,
                )

        return normalized_states

    def _select_candidate(
        self,
        deployment_id: str,
        upstreams: tuple[Upstream, ...],
        states: dict[str, HealthState],
        attempted_upstream_ids: set[str],
        probe_blocked_upstream_ids: set[str],
    ) -> tuple[RouteSelection, bool] | None:
        while True:
            selection = self._routing_selector.select(
                deployment_id=deployment_id,
                upstreams=upstreams,
                states=states,
                excluded_upstream_ids=frozenset(attempted_upstream_ids),
                temporarily_blocked_upstream_ids=frozenset(probe_blocked_upstream_ids),
            )
            if selection is None:
                return None

            state = states.get(selection.upstream.id, HealthState())
            if state.status is not HealthStatus.HALF_OPEN:
                return selection, False

            acquired = self._health_state_repository.try_acquire_half_open_probe(
                deployment_id,
                selection.upstream.id,
                self._half_open_probe_ttl_seconds(),
            )
            if acquired:
                return selection, True

            probe_blocked_upstream_ids.add(selection.upstream.id)

    def _half_open_probe_ttl_seconds(self) -> int:
        return max(ceil(self._timeout_ms / 1000) + 1, 1)

    def _record_event(self, event: RuntimeEvent) -> None:
        if self._runtime_event_recorder is not None:
            self._runtime_event_recorder.record(event)
