from __future__ import annotations

import logging
import socket
from dataclasses import dataclass

from azure.monitor.opentelemetry.exporter import (
    ApplicationInsightsSampler,
    AzureMonitorLogExporter,
    AzureMonitorTraceExporter,
)
from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from app.infrastructure.config.settings import AppSettings
from app.infrastructure.observability.logging import configure_logging


@dataclass(slots=True)
class ObservabilityRuntime:
    backend: str
    trace_export_enabled: bool
    log_export_enabled: bool
    app_log_export_handler: logging.Handler | None = None
    tracer_provider: TracerProvider | None = None
    logger_provider: LoggerProvider | None = None

    def shutdown(self) -> None:
        if self.backend != "azure_monitor":
            return
        if self.logger_provider is not None:
            self.logger_provider.force_flush()
            self.logger_provider.shutdown()
        if self.tracer_provider is not None:
            self.tracer_provider.force_flush()
            self.tracer_provider.shutdown()


def configure_observability(settings: AppSettings) -> ObservabilityRuntime:
    runtime = (
        _configure_azure_monitor(settings)
        if settings.observability_backend == "azure_monitor"
        else _configure_local_tracing(settings)
    )
    configure_logging(
        settings.log_level,
        app_log_export_handler=runtime.app_log_export_handler,
    )
    return runtime


def _configure_local_tracing(settings: AppSettings) -> ObservabilityRuntime:
    resource = _build_resource(settings)
    provider = trace.get_tracer_provider()
    tracer_provider = provider if isinstance(provider, TracerProvider) else None
    if tracer_provider is None:
        tracer_provider = TracerProvider(resource=resource)
        trace.set_tracer_provider(tracer_provider)
    return ObservabilityRuntime(
        backend="local",
        trace_export_enabled=False,
        log_export_enabled=False,
        tracer_provider=tracer_provider,
    )


def _configure_azure_monitor(settings: AppSettings) -> ObservabilityRuntime:
    connection_string = settings.resolved_azure_monitor_connection_string
    if connection_string is None:  # pragma: no cover - guarded by settings validation
        raise ValueError("Azure Monitor backend requires a connection string.")

    tracer_provider = TracerProvider(
        resource=_build_resource(settings),
        sampler=ApplicationInsightsSampler(settings.azure_monitor_sampling_ratio),
    )
    tracer_provider.add_span_processor(
        BatchSpanProcessor(
            AzureMonitorTraceExporter(
                connection_string=connection_string,
                disable_offline_storage=settings.azure_monitor_disable_offline_storage,
            )
        )
    )
    trace.set_tracer_provider(tracer_provider)

    logger_provider: LoggerProvider | None = None
    app_log_export_handler: logging.Handler | None = None
    if settings.azure_monitor_log_export_enabled:
        logger_provider = LoggerProvider(resource=_build_resource(settings))
        logger_provider.add_log_record_processor(
            BatchLogRecordProcessor(
                AzureMonitorLogExporter(
                    connection_string=connection_string,
                    disable_offline_storage=settings.azure_monitor_disable_offline_storage,
                )
            )
        )
        set_logger_provider(logger_provider)
        app_log_export_handler = LoggingHandler(logger_provider=logger_provider)

    return ObservabilityRuntime(
        backend="azure_monitor",
        trace_export_enabled=True,
        log_export_enabled=settings.azure_monitor_log_export_enabled,
        app_log_export_handler=app_log_export_handler,
        tracer_provider=tracer_provider,
        logger_provider=logger_provider,
    )


def _build_resource(settings: AppSettings) -> Resource:
    return Resource.create(
        {
            "service.name": settings.app_name,
            "service.version": settings.app_version,
            "deployment.environment": settings.environment,
            "service.instance.id": socket.gethostname(),
        }
    )
