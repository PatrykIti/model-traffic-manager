from __future__ import annotations


class DomainError(Exception):
    """Base class for domain and application-facing errors."""


class DomainInvariantError(DomainError):
    """Raised when a domain invariant is violated."""


class ConfigValidationError(DomainError):
    """Raised when router configuration is invalid."""


class DeploymentNotFound(DomainError):
    """Raised when a deployment cannot be found in the registry."""
