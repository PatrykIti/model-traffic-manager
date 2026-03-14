from __future__ import annotations

from collections.abc import Callable, Mapping
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from typing import Any

from app.domain.errors import OutboundConnectionError, OutboundTimeoutError
from app.domain.value_objects.failure_classification import FailureClassification, FailureReason


class UpstreamFailureClassifier:
    def __init__(self, now_provider: Callable[[], datetime] | None = None) -> None:
        self._now_provider = now_provider or (lambda: datetime.now(UTC))

    def classify_transport_error(
        self,
        error: OutboundTimeoutError | OutboundConnectionError,
    ) -> FailureClassification:
        if isinstance(error, OutboundTimeoutError):
            return FailureClassification(reason=FailureReason.TIMEOUT, retriable=True)
        return FailureClassification(reason=FailureReason.NETWORK_ERROR, retriable=True)

    def classify_response(
        self,
        *,
        status_code: int,
        headers: Mapping[str, str],
        json_body: Any | None,
        text_body: str | None,
    ) -> FailureClassification:
        if self._contains_quota_exhausted_marker(json_body=json_body, text_body=text_body):
            return FailureClassification(reason=FailureReason.QUOTA_EXHAUSTED, retriable=True)

        if status_code == 429:
            return FailureClassification(
                reason=FailureReason.RATE_LIMITED,
                retriable=True,
                retry_after_seconds=self._parse_retry_after(headers),
            )

        if status_code in {500, 502, 503, 504}:
            return FailureClassification(reason=FailureReason.UNHEALTHY, retriable=True)

        return FailureClassification(reason=FailureReason.NON_RETRIABLE, retriable=False)

    def _parse_retry_after(self, headers: Mapping[str, str]) -> int | None:
        value = headers.get("retry-after")
        if value is None:
            return None

        stripped = value.strip()
        if stripped.isdigit():
            return int(stripped)

        try:
            retry_after_date = parsedate_to_datetime(stripped)
        except (TypeError, ValueError, IndexError):
            return None

        if retry_after_date.tzinfo is None:
            retry_after_date = retry_after_date.replace(tzinfo=UTC)

        delta_seconds = int((retry_after_date - self._now_provider()).total_seconds())
        return max(delta_seconds, 0)

    @staticmethod
    def _contains_quota_exhausted_marker(json_body: Any | None, text_body: str | None) -> bool:
        body_text = _flatten_body(json_body) or (text_body or "")
        lowered = body_text.lower()
        return "quota" in lowered and any(marker in lowered for marker in ("exceeded", "exhausted"))


def _flatten_body(json_body: Any | None) -> str:
    if json_body is None:
        return ""

    if isinstance(json_body, dict):
        return " ".join(_flatten_body(value) for value in json_body.values())
    if isinstance(json_body, list):
        return " ".join(_flatten_body(value) for value in json_body)
    return str(json_body)
