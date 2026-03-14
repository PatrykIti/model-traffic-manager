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


class OutboundTimeoutError(DomainError):
    """Raised when the upstream call times out."""


class OutboundConnectionError(DomainError):
    """Raised when the upstream connection cannot be established."""


class UpstreamSelectionError(DomainError):
    """Raised when no upstream can be selected."""
