from __future__ import annotations

from typing import Protocol

from app.application.dto.runtime_event import RuntimeEvent


class RuntimeEventRecorder(Protocol):
    def record(self, event: RuntimeEvent) -> None:
        """Record a runtime event for logs, metrics, traces, or diagnostics."""
