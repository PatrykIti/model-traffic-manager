from __future__ import annotations

import logging
import sys
from typing import Any

import structlog

_APP_LOG_EXPORT_HANDLER_NAME = "azure-monitor-app-export"


def configure_logging(
    log_level: str,
    *,
    app_log_export_handler: logging.Handler | None = None,
) -> None:
    level = getattr(logging, log_level.upper(), logging.INFO)

    root_logger = logging.getLogger()
    if not root_logger.handlers:
        logging.basicConfig(
            format="%(message)s",
            level=level,
            stream=sys.stdout,
        )
    else:
        root_logger.setLevel(level)

    if app_log_export_handler is not None:
        app_logger = logging.getLogger("app")
        app_logger.setLevel(level)
        if not any(
            getattr(handler, "name", None) == _APP_LOG_EXPORT_HANDLER_NAME
            for handler in app_logger.handlers
        ):
            app_log_export_handler.name = _APP_LOG_EXPORT_HANDLER_NAME
            app_logger.addHandler(app_log_export_handler)

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.dev.ConsoleRenderer(colors=sys.stdout.isatty()),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger(name: str | None = None) -> Any:
    return structlog.get_logger(name)
