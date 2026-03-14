from __future__ import annotations


class DomainError(Exception):
    """Base class for domain and application-facing errors."""


class DomainInvariantError(DomainError):
    """Raised when a domain invariant is violated."""


class ConfigValidationError(DomainError):
    """Raised when router configuration is invalid."""


class DeploymentNotFound(DomainError):
    """Raised when a deployment cannot be found in the registry."""


class SecretResolutionError(DomainError):
    """Raised when secret material cannot be resolved."""


class UnsupportedAuthModeError(DomainError):
    """Raised when the current phase does not support an auth mode."""


class TokenAcquisitionError(DomainError):
    """Raised when the router cannot acquire a token for outbound auth."""


class RequestRateLimitExceededError(DomainError):
    """Raised when a deployment exceeds its allowed request rate."""

    def __init__(self, deployment_id: str, retry_after_seconds: int | None = None) -> None:
        self.deployment_id = deployment_id
        self.retry_after_seconds = retry_after_seconds
        detail = f"Deployment '{deployment_id}' exceeded its request rate limit."
        super().__init__(detail)


class ConcurrencyLimitExceededError(DomainError):
    """Raised when a deployment exceeds its allowed concurrency."""

    def __init__(self, deployment_id: str) -> None:
        self.deployment_id = deployment_id
        super().__init__(f"Deployment '{deployment_id}' exceeded its concurrency limit.")


class OutboundTimeoutError(DomainError):
    """Raised when the upstream call times out."""


class OutboundConnectionError(DomainError):
    """Raised when the upstream connection cannot be established."""


class UpstreamSelectionError(DomainError):
    """Raised when no upstream can be selected."""
