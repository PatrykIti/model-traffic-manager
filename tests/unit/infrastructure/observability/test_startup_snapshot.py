from __future__ import annotations

from pathlib import Path

from app.infrastructure.bootstrap.container import build_container
from app.infrastructure.config.settings import AppSettings
from app.infrastructure.observability.startup_snapshot import build_startup_topology_snapshot
from app.infrastructure.observability.telemetry import ObservabilityRuntime


def test_startup_snapshot_includes_observability_and_upstream_metadata() -> None:
    container = build_container(
        AppSettings(
            config_path=Path("configs/example.router.yaml"),
            environment="test",
            log_level="WARNING",
        )
    )

    snapshot = build_startup_topology_snapshot(
        container=container,
        observability=ObservabilityRuntime(
            backend="local",
            trace_export_enabled=False,
            log_export_enabled=False,
        ),
    )

    assert snapshot["router_instance_name"] == "model-traffic-manager-local"
    assert snapshot["observability_backend"] == "local"
    assert snapshot["deployments"][0]["upstreams"][0]["id"] == "local-upstream"
    assert snapshot["deployments"][0]["upstreams"][0]["capacity_mode"] is None
