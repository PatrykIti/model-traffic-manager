from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    app_name: str = "model-traffic-manager"
    environment: str = "local"
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False
    config_path: Path = Field(default=Path("configs/example.router.yaml"))
    log_level: str = "INFO"
    outbound_connect_timeout_ms: int = 5000
    outbound_write_timeout_ms: int = 30000
    outbound_pool_timeout_ms: int = 5000
    outbound_max_connections: int = 100
    outbound_max_keepalive_connections: int = 20

    model_config = SettingsConfigDict(
        env_prefix="MODEL_TRAFFIC_MANAGER_",
        env_file=".env",
        extra="ignore",
    )


def load_settings() -> AppSettings:
    return AppSettings()
