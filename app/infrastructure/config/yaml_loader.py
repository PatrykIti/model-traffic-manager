from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from app.domain.errors import ConfigValidationError
from app.infrastructure.config.models import RouterConfigModel


def load_router_config(path: Path) -> RouterConfigModel:
    try:
        raw_text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ConfigValidationError(f"Could not read config file '{path}': {exc}") from exc

    try:
        raw_config: Any = yaml.safe_load(raw_text)
    except yaml.YAMLError as exc:
        raise ConfigValidationError(f"Invalid YAML in config file '{path}': {exc}") from exc

    if raw_config is None:
        raise ConfigValidationError(f"Config file '{path}' is empty.")

    if not isinstance(raw_config, dict):
        raise ConfigValidationError(f"Config file '{path}' must contain a mapping at the root.")

    try:
        return RouterConfigModel.model_validate(raw_config)
    except ValidationError as exc:
        raise ConfigValidationError(f"Invalid router configuration: {exc}") from exc
