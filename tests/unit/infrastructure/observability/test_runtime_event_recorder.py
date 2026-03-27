from __future__ import annotations

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from app.application.dto.runtime_event import RuntimeEvent
from app.infrastructure.observability.runtime_event_recorder import StructuredRuntimeEventRecorder


def test_runtime_event_recorder_enriches_current_span_with_final_upstream_metadata() -> None:
    exporter = InMemorySpanExporter()
    tracer_provider = TracerProvider()
    tracer_provider.add_span_processor(SimpleSpanProcessor(exporter))
    tracer = tracer_provider.get_tracer(__name__)
    recorder = StructuredRuntimeEventRecorder()

    with tracer.start_as_current_span("request-flow"):
        recorder.record(
            RuntimeEvent(
                event_type="route_selected",
                endpoint_kind="chat_completions",
                deployment_id="gpt-4o-chat",
                consumer_role="bot-system-be",
                request_id="req-123",
                attempt=1,
                upstream_id="aoai-weu-ptu",
                provider="azure_openai",
                account="aoai-prod-01",
                region="westeurope",
                model_name="gpt-4o",
                model_version="2024-08-06",
                deployment_name="gpt-4o",
                capacity_mode="ptu",
                auth_mode="managed_identity",
                selected_tier=0,
                decision_reason="selected_healthy",
            )
        )
        recorder.record(
            RuntimeEvent(
                event_type="request_completed",
                endpoint_kind="chat_completions",
                deployment_id="gpt-4o-chat",
                consumer_role="bot-system-be",
                request_id="req-123",
                attempt=1,
                upstream_id="aoai-weu-ptu",
                provider="azure_openai",
                account="aoai-prod-01",
                region="westeurope",
                model_name="gpt-4o",
                model_version="2024-08-06",
                deployment_name="gpt-4o",
                capacity_mode="ptu",
                auth_mode="managed_identity",
                selected_tier=0,
                outcome="success",
                status_code=200,
            )
        )

    finished_span = exporter.get_finished_spans()[0]

    assert finished_span.attributes["router.selected_upstream_id"] == "aoai-weu-ptu"
    assert finished_span.attributes["router.consumer_role"] == "bot-system-be"
    assert finished_span.attributes["router.final_upstream_id"] == "aoai-weu-ptu"
    assert finished_span.attributes["router.final_consumer_role"] == "bot-system-be"
    assert finished_span.attributes["router.final_provider"] == "azure_openai"
    assert finished_span.attributes["router.final_account"] == "aoai-prod-01"
    assert finished_span.attributes["router.final_region"] == "westeurope"
    assert finished_span.attributes["router.final_capacity_mode"] == "ptu"
    assert finished_span.attributes["router.outcome"] == "success"
    assert finished_span.attributes["http.status_code"] == 200
    assert [event.name for event in finished_span.events] == [
        "route_selected",
        "request_completed",
    ]
    assert finished_span.events[0].attributes["router.capacity_mode"] == "ptu"
