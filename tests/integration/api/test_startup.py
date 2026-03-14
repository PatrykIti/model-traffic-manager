from __future__ import annotations

from typing import cast

from fastapi.testclient import TestClient

from app.entrypoints.api.main import app
from app.infrastructure.bootstrap.container import BootstrapContainer


def test_startup_initializes_container() -> None:
    with TestClient(app) as client:
        container = cast(BootstrapContainer, client.app.state.container)
        response = client.get("/health/ready")

    assert response.status_code == 200
    assert container.settings.app_name == "model-traffic-manager"
    assert container.settings.environment == "local"
    assert container.router_config.router.instance_name == "model-traffic-manager-local"
    assert container.deployment_repository.get_deployment("local-health-check") is not None
    assert container.deployment_repository.get_deployment("local-embeddings-check") is not None
    assert container.route_chat_completion_use_case is not None
    assert container.route_embeddings_use_case is not None
    assert container.token_provider is not None
    assert container.health_state_repository is not None
    assert container.request_rate_limiter is not None
    assert container.concurrency_limiter is not None
    assert container.deployment_limit_guard is not None
    assert container.failure_classifier is not None
    assert container.health_state_policy is not None
    assert container.routing_selector is not None
