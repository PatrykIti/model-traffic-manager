from __future__ import annotations

from dataclasses import dataclass

from app.domain.entities.upstream import Upstream
from app.domain.errors import DomainInvariantError


@dataclass(frozen=True, slots=True)
class Deployment:
    id: str
    kind: str
    protocol: str
    routing_strategy: str
    max_concurrency: int
    request_rate_per_second: int
    upstreams: tuple[Upstream, ...]

    def __post_init__(self) -> None:
        if not self.id:
            raise DomainInvariantError("Deployment ID must not be empty.")
        if not self.kind:
            raise DomainInvariantError("Deployment kind must not be empty.")
        if not self.protocol:
            raise DomainInvariantError("Deployment protocol must not be empty.")
        if not self.routing_strategy:
            raise DomainInvariantError("Deployment routing strategy must not be empty.")
        if self.max_concurrency <= 0:
            raise DomainInvariantError("Deployment max concurrency must be greater than zero.")
        if self.request_rate_per_second <= 0:
            raise DomainInvariantError("Deployment request rate must be greater than zero.")
        if not self.upstreams:
            raise DomainInvariantError("Deployment must define at least one upstream.")

    @property
    def upstream_count(self) -> int:
        return len(self.upstreams)

    @property
    def providers(self) -> tuple[str, ...]:
        return tuple(sorted({upstream.provider for upstream in self.upstreams}))

    @property
    def regions(self) -> tuple[str, ...]:
        return tuple(sorted({upstream.region for upstream in self.upstreams}))
