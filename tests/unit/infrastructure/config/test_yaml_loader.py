from __future__ import annotations

from pathlib import Path

import pytest

from app.domain.errors import ConfigValidationError
from app.infrastructure.config.deployment_repository import ConfigDeploymentRepository
from app.infrastructure.config.yaml_loader import load_router_config


def test_yaml_loader_reads_example_config() -> None:
    config = load_router_config(Path("configs/example.router.yaml"))

    assert config.router.instance_name == "model-traffic-manager-local"
    assert len(config.deployments) == 2

    repository = ConfigDeploymentRepository.from_router_config(config)
    assert repository.get_deployment("local-health-check") is not None
    assert repository.get_deployment("local-embeddings-check") is not None


def test_yaml_loader_rejects_invalid_yaml(tmp_path: Path) -> None:
    path = tmp_path / "broken.yaml"
    path.write_text("router: [", encoding="utf-8")

    with pytest.raises(ConfigValidationError):
        load_router_config(path)


def test_yaml_loader_rejects_empty_file(tmp_path: Path) -> None:
    path = tmp_path / "empty.yaml"
    path.write_text("", encoding="utf-8")

    with pytest.raises(ConfigValidationError):
        load_router_config(path)
