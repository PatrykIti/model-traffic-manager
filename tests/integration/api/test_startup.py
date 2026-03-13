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
