from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.infrastructure.config.settings import AppSettings


def test_settings_accept_local_observability_without_connection_string() -> None:
    settings = AppSettings()

    assert settings.observability_backend == "local"
    assert settings.resolved_azure_monitor_connection_string is None


def test_settings_require_connection_string_for_azure_monitor_backend() -> None:
    with pytest.raises(ValidationError):
        AppSettings(observability_backend="azure_monitor")


def test_settings_accept_standard_application_insights_env(monkeypatch) -> None:
    monkeypatch.setenv(
        "APPLICATIONINSIGHTS_CONNECTION_STRING",
        "InstrumentationKey=00000000-0000-0000-0000-000000000000",
    )

    settings = AppSettings(observability_backend="azure_monitor")

    assert (
        settings.resolved_azure_monitor_connection_string
        == "InstrumentationKey=00000000-0000-0000-0000-000000000000"
    )
