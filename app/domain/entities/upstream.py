from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from app.domain.errors import DomainInvariantError
from app.domain.value_objects.auth_policy import AuthPolicy


class BalancingPolicy(StrEnum):
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    ACTIVE_STANDBY = "active_standby"


class CapacityMode(StrEnum):
    PAYG = "payg"
    PTU = "ptu"


@dataclass(frozen=True, slots=True)
class Upstream:
    id: str
    provider: str
    account: str
    region: str
    tier: int
    weight: int
    endpoint: str
    auth: AuthPolicy
    model_name: str | None = None
    model_version: str | None = None
    deployment_name: str | None = None
    capacity_mode: CapacityMode | None = None
    compatibility_group: str | None = None
    balancing_policy: BalancingPolicy = BalancingPolicy.WEIGHTED_ROUND_ROBIN
    warm_standby: bool = False
    drain: bool = False
    target_share_percent: int | None = None
    max_share_percent: int | None = None

    def __post_init__(self) -> None:
        if not self.id:
            raise DomainInvariantError("Upstream ID must not be empty.")
        if not self.provider:
            raise DomainInvariantError("Upstream provider must not be empty.")
        if not self.account:
            raise DomainInvariantError("Upstream account must not be empty.")
        if not self.region:
            raise DomainInvariantError("Upstream region must not be empty.")
        if not self.endpoint:
            raise DomainInvariantError("Upstream endpoint must not be empty.")
        if self.tier < 0:
            raise DomainInvariantError("Upstream tier must be greater than or equal to zero.")
        if self.weight <= 0:
            raise DomainInvariantError("Upstream weight must be greater than zero.")
        object.__setattr__(self, "balancing_policy", BalancingPolicy(self.balancing_policy))
        if self.capacity_mode is not None:
            object.__setattr__(self, "capacity_mode", CapacityMode(self.capacity_mode))
        if self.target_share_percent is not None and not 0 < self.target_share_percent <= 100:
            raise DomainInvariantError("target_share_percent must be between 1 and 100.")
        if self.max_share_percent is not None and not 0 < self.max_share_percent <= 100:
            raise DomainInvariantError("max_share_percent must be between 1 and 100.")
        if (
            self.target_share_percent is not None
            and self.max_share_percent is not None
            and self.target_share_percent > self.max_share_percent
        ):
            raise DomainInvariantError(
                "target_share_percent must be lower than or equal to max_share_percent."
            )

    @property
    def effective_weight(self) -> int:
        return self.target_share_percent or self.weight
