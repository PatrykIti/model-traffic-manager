from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    app_name: str = "model-traffic-manager"
    app_version: str = "0.1.0"
    environment: str = "local"
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False
    config_path: Path = Field(default=Path("configs/example.router.yaml"))
    log_level: str = "INFO"
    observability_backend: Literal["local", "azure_monitor"] = "local"
    azure_monitor_connection_string: str | None = None
    azure_monitor_log_export_enabled: bool = False
    azure_monitor_sampling_ratio: float = Field(default=1.0, ge=0.0, le=1.0)
    azure_monitor_disable_offline_storage: bool = False
    outbound_connect_timeout_ms: int = 5000
    outbound_write_timeout_ms: int = 30000
    outbound_pool_timeout_ms: int = 5000
    outbound_max_connections: int = 100
    outbound_max_keepalive_connections: int = 20
    runtime_state_backend: Literal["in_memory", "redis"] = "in_memory"
    redis_url: str | None = None
    redis_key_prefix: str = "router"

    model_config = SettingsConfigDict(
        env_prefix="MODEL_TRAFFIC_MANAGER_",
        env_file=".env",
        extra="ignore",
    )

    @model_validator(mode="after")
    def validate_runtime_state(self) -> AppSettings:
        if self.runtime_state_backend == "redis" and not self.redis_url:
            raise ValueError("redis_url must be configured when runtime_state_backend='redis'")
        if (
            self.observability_backend == "azure_monitor"
            and not self.resolved_azure_monitor_connection_string
        ):
            raise ValueError(
                "azure_monitor_connection_string or APPLICATIONINSIGHTS_CONNECTION_STRING "
                "must be configured when observability_backend='azure_monitor'"
            )
        return self

    @property
    def resolved_azure_monitor_connection_string(self) -> str | None:
        return self.azure_monitor_connection_string or os.getenv(
            "APPLICATIONINSIGHTS_CONNECTION_STRING"
        )


def load_settings() -> AppSettings:
    return AppSettings()
