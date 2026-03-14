from __future__ import annotations

from datetime import UTC, datetime

from app.domain.errors import OutboundConnectionError, OutboundTimeoutError
from app.domain.services.upstream_failure_classifier import UpstreamFailureClassifier
from app.domain.value_objects.failure_classification import FailureReason


def test_classifier_marks_timeout_as_retriable() -> None:
    classifier = UpstreamFailureClassifier()

    failure = classifier.classify_transport_error(OutboundTimeoutError("timeout"))

    assert failure.reason is FailureReason.TIMEOUT
    assert failure.retriable is True


def test_classifier_marks_connection_error_as_retriable() -> None:
    classifier = UpstreamFailureClassifier()

    failure = classifier.classify_transport_error(OutboundConnectionError("network"))

    assert failure.reason is FailureReason.NETWORK_ERROR
    assert failure.retriable is True


def test_classifier_parses_retry_after_delta_seconds() -> None:
    classifier = UpstreamFailureClassifier()

    failure = classifier.classify_response(
        status_code=429,
        headers={"retry-after": "42"},
        json_body={"error": {"message": "too many requests"}},
        text_body=None,
    )

    assert failure.reason is FailureReason.RATE_LIMITED
    assert failure.retriable is True
    assert failure.retry_after_seconds == 42


def test_classifier_parses_retry_after_http_date() -> None:
    classifier = UpstreamFailureClassifier(
        now_provider=lambda: datetime(2026, 3, 14, 12, 0, 0, tzinfo=UTC)
    )

    failure = classifier.classify_response(
        status_code=429,
        headers={"retry-after": "Sat, 14 Mar 2026 12:00:30 GMT"},
        json_body=None,
        text_body="too many requests",
    )

    assert failure.reason is FailureReason.RATE_LIMITED
    assert failure.retry_after_seconds == 30


def test_classifier_detects_quota_exhaustion() -> None:
    classifier = UpstreamFailureClassifier()

    failure = classifier.classify_response(
        status_code=403,
        headers={},
        json_body={"error": {"message": "quota exceeded for this deployment"}},
        text_body=None,
    )

    assert failure.reason is FailureReason.QUOTA_EXHAUSTED
    assert failure.retriable is True


def test_classifier_marks_other_4xx_as_non_retriable() -> None:
    classifier = UpstreamFailureClassifier()

    failure = classifier.classify_response(
        status_code=400,
        headers={},
        json_body={"error": {"message": "bad request"}},
        text_body=None,
    )

    assert failure.reason is FailureReason.NON_RETRIABLE
    assert failure.retriable is False
