from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.infrastructure.config.models import RouterConfigModel


def build_valid_config() -> dict[str, object]:
    return {
        "router": {
            "instance_name": "ai-router-prod",
            "timeout_ms": 30000,
            "max_attempts": 3,
            "retryable_status_codes": [429, 500, 502, 503, 504],
            "health": {
                "failure_threshold": 3,
                "cooldown_seconds": 30,
                "half_open_after_seconds": 60,
            },
        },
        "deployments": [
            {
                "id": "gpt-4o-chat",
                "kind": "llm",
                "protocol": "openai_chat",
                "routing": {"strategy": "tiered_failover"},
                "limits": {
                    "max_concurrency": 200,
                    "request_rate_per_second": 50,
                },
                "upstreams": [
                    {
                        "id": "aoai-weu-primary",
                        "provider": "azure_openai",
                        "account": "aoai-prod-01",
                        "region": "westeurope",
                        "tier": 0,
                        "weight": 100,
                        "endpoint": (
                            "https://aoai-prod-01.openai.azure.com/openai/deployments/"
                            "gpt-4o/chat/completions"
                        ),
                        "auth": {
                            "mode": "managed_identity",
                            "scope": "https://cognitiveservices.azure.com/.default",
                        },
                    }
                ],
            }
        ],
        "shared_services": {},
    }


def test_router_config_model_accepts_valid_config() -> None:
    config = RouterConfigModel.model_validate(build_valid_config())

    assert config.router.instance_name == "ai-router-prod"
    assert config.deployments[0].id == "gpt-4o-chat"


def test_router_config_model_rejects_duplicate_deployment_ids() -> None:
    config = build_valid_config()
    config["deployments"] = [config["deployments"][0], config["deployments"][0]]

    with pytest.raises(ValidationError):
        RouterConfigModel.model_validate(config)


def test_router_config_model_rejects_duplicate_upstream_ids() -> None:
    config = build_valid_config()
    deployment = config["deployments"][0]
    deployment["upstreams"] = [deployment["upstreams"][0], deployment["upstreams"][0]]

    with pytest.raises(ValidationError):
        RouterConfigModel.model_validate(config)


def test_router_config_model_rejects_missing_scope_for_managed_identity() -> None:
    config = build_valid_config()
    config["deployments"][0]["upstreams"][0]["auth"] = {"mode": "managed_identity"}

    with pytest.raises(ValidationError):
        RouterConfigModel.model_validate(config)


def test_router_config_model_rejects_missing_api_key_fields() -> None:
    config = build_valid_config()
    config["deployments"][0]["upstreams"][0]["auth"] = {
        "mode": "api_key",
        "header_name": "api-key",
    }

    with pytest.raises(ValidationError):
        RouterConfigModel.model_validate(config)


def test_router_config_model_rejects_unsupported_deployment_kind() -> None:
    config = build_valid_config()
    config["deployments"][0]["kind"] = "audio"

    with pytest.raises(ValidationError):
        RouterConfigModel.model_validate(config)


def test_router_config_model_rejects_unsupported_deployment_protocol() -> None:
    config = build_valid_config()
    config["deployments"][0]["protocol"] = "openai_audio"

    with pytest.raises(ValidationError):
        RouterConfigModel.model_validate(config)
