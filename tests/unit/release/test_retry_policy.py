from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def _load_module():
    module_path = Path("scripts/release/retry_policy.py")
    spec = importlib.util.spec_from_file_location("retry_policy", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_retry_policy_matches_transient_terraform_apply_errors() -> None:
    module = _load_module()

    assert module.should_retry("terraform_apply", "context deadline exceeded") is True
    assert module.should_retry("terraform_apply", "TLS handshake timeout") is True


def test_retry_policy_matches_transient_kubernetes_watch_errors() -> None:
    module = _load_module()

    assert (
        module.should_retry(
            "kubernetes_watch",
            "unable to decode an event from the watch stream: http2: client connection lost",
        )
        is True
    )


def test_retry_policy_does_not_retry_quota_or_principal_type_errors() -> None:
    module = _load_module()

    assert module.should_retry("terraform_apply", "QuotaExceeded") is False
    assert module.should_retry("terraform_apply", "UnmatchedPrincipalType") is False


def test_retry_policy_rejects_unknown_policy() -> None:
    module = _load_module()

    with pytest.raises(ValueError):
        module.should_retry("missing-policy", "timeout")
