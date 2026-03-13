from __future__ import annotations

from dataclasses import dataclass

from app.infrastructure.config.settings import AppSettings


@dataclass(slots=True)
class BootstrapContainer:
    settings: AppSettings


def build_container(settings: AppSettings) -> BootstrapContainer:
    return BootstrapContainer(settings=settings)
