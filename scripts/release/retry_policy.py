from __future__ import annotations

import sys
from pathlib import Path

RETRY_POLICIES: dict[str, tuple[str, ...]] = {
    "azure_control_plane": (
        "too many requests",
        "toomanyrequests",
        "timed out",
        "timeout",
        "context deadline exceeded",
        "connection reset",
        "connection refused",
        "service unavailable",
        "temporarily unavailable",
        "client connection lost",
        "tls handshake timeout",
        "i/o timeout",
        "eof",
    ),
    "ghcr_auth": (
        "too many requests",
        "toomanyrequests",
        "timed out",
        "connection reset",
        "tls handshake timeout",
        "service unavailable",
        "temporarily unavailable",
    ),
    "ghcr_build_push": (
        "too many requests",
        "toomanyrequests",
        "timed out",
        "connection reset",
        "tls handshake timeout",
        "service unavailable",
        "temporarily unavailable",
        "unexpected eof",
    ),
    "terraform_apply": (
        "too many requests",
        "toomanyrequests",
        "timed out",
        "context deadline exceeded",
        "connection reset",
        "connection refused",
        "tls handshake timeout",
        "service unavailable",
        "temporarily unavailable",
        "client connection lost",
        "i/o timeout",
        "eof",
    ),
    "terraform_destroy": (
        "too many requests",
        "toomanyrequests",
        "timed out",
        "context deadline exceeded",
        "connection reset",
        "connection refused",
        "tls handshake timeout",
        "service unavailable",
        "temporarily unavailable",
        "client connection lost",
        "i/o timeout",
        "eof",
    ),
    "kubernetes_watch": (
        "unable to decode an event from the watch stream",
        "client connection lost",
        "timed out",
        "timeout",
        "context deadline exceeded",
        "connection reset",
        "i/o timeout",
        "eof",
    ),
    "port_forward_start": (
        "timed out",
        "timeout",
        "context deadline exceeded",
        "connection reset",
        "connection refused",
        "address already in use",
        "client connection lost",
        "eof",
    ),
}


def should_retry(policy: str, text: str) -> bool:
    patterns = RETRY_POLICIES.get(policy)
    if patterns is None:
        raise ValueError(f"Unknown retry policy '{policy}'.")
    lowered = text.lower()
    return any(pattern in lowered for pattern in patterns)


def main() -> None:
    if len(sys.argv) != 4 or sys.argv[1] != "should-retry":
        raise SystemExit("Usage: retry_policy.py should-retry <policy> <log-path>")

    policy = sys.argv[2]
    log_path = Path(sys.argv[3])
    text = log_path.read_text(encoding="utf-8") if log_path.exists() else ""
    raise SystemExit(0 if should_retry(policy, text) else 1)


if __name__ == "__main__":
    main()
