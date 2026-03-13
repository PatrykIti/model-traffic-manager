from __future__ import annotations

import logging
import sys
from typing import Any

import structlog


def configure_logging(log_level: str) -> None:
    level = getattr(logging, log_level.upper(), logging.INFO)

    logging.basicConfig(
        format="%(message)s",
        level=level,
        stream=sys.stdout,
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.dev.ConsoleRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger(name: str | None = None) -> Any:
    return structlog.get_logger(name)
