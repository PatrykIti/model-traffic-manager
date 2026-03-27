from __future__ import annotations

from typing import Protocol

from app.domain.entities.deployment import Deployment


class DeploymentRepository(Protocol):
    def list_deployments(self) -> tuple[Deployment, ...]:
        """Return all known deployments."""

    def get_deployment(self, deployment_id: str) -> Deployment | None:
        """Return a single deployment if it exists."""
