from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from app.domain.entities.upstream import Upstream
from app.domain.errors import DomainInvariantError


class DeploymentKind(StrEnum):
    LLM = "llm"
    EMBEDDINGS = "embeddings"


class DeploymentProtocol(StrEnum):
    OPENAI_CHAT = "openai_chat"
    OPENAI_EMBEDDINGS = "openai_embeddings"


@dataclass(frozen=True, slots=True)
class Deployment:
    id: str
    kind: DeploymentKind
    protocol: DeploymentProtocol
    routing_strategy: str
    max_concurrency: int
    request_rate_per_second: int
    upstreams: tuple[Upstream, ...]
    consumer_role: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "kind", DeploymentKind(self.kind))
        object.__setattr__(self, "protocol", DeploymentProtocol(self.protocol))
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
        if self.consumer_role is not None and not self.consumer_role:
            raise DomainInvariantError("Deployment consumer_role must not be empty.")
        if not self.upstreams:
            raise DomainInvariantError("Deployment must define at least one upstream.")

    def supports_chat_completions(self) -> bool:
        return (
            self.kind is DeploymentKind.LLM
            and self.protocol is DeploymentProtocol.OPENAI_CHAT
        )

    def supports_embeddings(self) -> bool:
        return (
            self.kind is DeploymentKind.EMBEDDINGS
            and self.protocol is DeploymentProtocol.OPENAI_EMBEDDINGS
        )

    @property
    def upstream_count(self) -> int:
        return len(self.upstreams)

    @property
    def providers(self) -> tuple[str, ...]:
        return tuple(sorted({upstream.provider for upstream in self.upstreams}))

    @property
    def regions(self) -> tuple[str, ...]:
        return tuple(sorted({upstream.region for upstream in self.upstreams}))
