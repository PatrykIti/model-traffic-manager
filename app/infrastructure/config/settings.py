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

    model_config = SettingsConfigDict(
        env_prefix="MODEL_TRAFFIC_MANAGER_",
        env_file=".env",
        extra="ignore",
    )


def load_settings() -> AppSettings:
    return AppSettings()
