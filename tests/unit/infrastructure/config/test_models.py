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
        "shared_services": {
            "conversation_archive": {
                "transport": "http_json",
                "access_mode": "direct_backend_access",
                "provider_managed_availability": True,
                "provider": "azure_storage",
                "account": "archive",
                "region": "westeurope",
                "endpoint": "https://archive.example.invalid",
                "auth": {
                    "mode": "managed_identity",
                    "scope": "https://storage.azure.com/.default",
                },
            }
        },
    }


def test_router_config_model_accepts_valid_config() -> None:
    config = RouterConfigModel.model_validate(build_valid_config())

    assert config.router.instance_name == "ai-router-prod"
    assert config.deployments[0].id == "gpt-4o-chat"
    assert (
        config.shared_services["conversation_archive"].access_mode.value
        == "direct_backend_access"
    )


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


def test_router_config_model_rejects_shared_service_routing_on_direct_access() -> None:
    config = build_valid_config()
    config["shared_services"]["conversation_archive"]["routing_strategy"] = "single_endpoint"

    with pytest.raises(ValidationError):
        RouterConfigModel.model_validate(config)


def test_router_config_model_rejects_provider_managed_tiered_failover_shared_service() -> None:
    config = build_valid_config()
    config["shared_services"]["conversation_archive"] = {
        "transport": "http_json",
        "access_mode": "router_proxy",
        "provider_managed_availability": True,
        "routing_strategy": "tiered_failover",
        "limits": {
            "max_concurrency": 10,
            "request_rate_per_second": 5,
        },
        "upstreams": [
            {
                "id": "primary",
                "provider": "internal_api",
                "account": "platform",
                "region": "westeurope",
                "tier": 0,
                "weight": 100,
                "endpoint": "https://example.invalid/shared",
                "auth": {"mode": "none"},
            }
        ],
    }

    with pytest.raises(ValidationError):
        RouterConfigModel.model_validate(config)


def test_router_config_model_rejects_mixed_compatibility_groups_in_same_tier() -> None:
    config = build_valid_config()
    config["deployments"][0]["upstreams"] = [
        {
            "id": "primary-a",
            "provider": "azure_openai",
            "account": "aoai-prod-01",
            "region": "westeurope",
            "tier": 0,
            "weight": 100,
            "endpoint": "https://example.invalid/chat-a",
            "model_name": "gpt-4o",
            "model_version": "2024-08-06",
            "compatibility_group": "pool-a",
            "auth": {
                "mode": "managed_identity",
                "scope": "https://cognitiveservices.azure.com/.default",
            },
        },
        {
            "id": "primary-b",
            "provider": "azure_openai",
            "account": "aoai-prod-02",
            "region": "northeurope",
            "tier": 0,
            "weight": 100,
            "endpoint": "https://example.invalid/chat-b",
            "model_name": "gpt-4o",
            "model_version": "2024-08-06",
            "compatibility_group": "pool-b",
            "auth": {
                "mode": "managed_identity",
                "scope": "https://cognitiveservices.azure.com/.default",
            },
        },
    ]

    with pytest.raises(ValidationError):
        RouterConfigModel.model_validate(config)


def test_router_config_model_rejects_embeddings_mixing_models_in_same_tier() -> None:
    config = build_valid_config()
    config["deployments"][0]["kind"] = "embeddings"
    config["deployments"][0]["protocol"] = "openai_embeddings"
    config["deployments"][0]["upstreams"] = [
        {
            "id": "primary-a",
            "provider": "azure_openai",
            "account": "aoai-prod-01",
            "region": "westeurope",
            "tier": 0,
            "weight": 100,
            "endpoint": "https://example.invalid/emb-a",
            "model_name": "text-embedding-3-small",
            "model_version": "1",
            "compatibility_group": "embeddings",
            "auth": {
                "mode": "managed_identity",
                "scope": "https://cognitiveservices.azure.com/.default",
            },
        },
        {
            "id": "primary-b",
            "provider": "azure_openai",
            "account": "aoai-prod-02",
            "region": "northeurope",
            "tier": 0,
            "weight": 100,
            "endpoint": "https://example.invalid/emb-b",
            "model_name": "text-embedding-3-large",
            "model_version": "1",
            "compatibility_group": "embeddings",
            "auth": {
                "mode": "managed_identity",
                "scope": "https://cognitiveservices.azure.com/.default",
            },
        },
    ]

    with pytest.raises(ValidationError):
        RouterConfigModel.model_validate(config)


def test_router_config_model_rejects_multiple_active_upstreams_for_active_standby() -> None:
    config = build_valid_config()
    config["deployments"][0]["upstreams"] = [
        {
            "id": "primary-a",
            "provider": "azure_openai",
            "account": "aoai-prod-01",
            "region": "westeurope",
            "tier": 0,
            "weight": 100,
            "endpoint": "https://example.invalid/chat-a",
            "compatibility_group": "chat-primary",
            "balancing_policy": "active_standby",
            "auth": {
                "mode": "managed_identity",
                "scope": "https://cognitiveservices.azure.com/.default",
            },
        },
        {
            "id": "primary-b",
            "provider": "azure_openai",
            "account": "aoai-prod-02",
            "region": "northeurope",
            "tier": 0,
            "weight": 100,
            "endpoint": "https://example.invalid/chat-b",
            "compatibility_group": "chat-primary",
            "balancing_policy": "active_standby",
            "auth": {
                "mode": "managed_identity",
                "scope": "https://cognitiveservices.azure.com/.default",
            },
        },
    ]

    with pytest.raises(ValidationError):
        RouterConfigModel.model_validate(config)


def test_router_config_model_rejects_effective_share_above_max_share_percent() -> None:
    config = build_valid_config()
    config["deployments"][0]["upstreams"] = [
        {
            "id": "primary-a",
            "provider": "azure_openai",
            "account": "aoai-prod-01",
            "region": "westeurope",
            "tier": 0,
            "weight": 80,
            "endpoint": "https://example.invalid/chat-a",
            "compatibility_group": "chat-primary",
            "max_share_percent": 50,
            "auth": {
                "mode": "managed_identity",
                "scope": "https://cognitiveservices.azure.com/.default",
            },
        },
        {
            "id": "primary-b",
            "provider": "azure_openai",
            "account": "aoai-prod-02",
            "region": "northeurope",
            "tier": 0,
            "weight": 20,
            "endpoint": "https://example.invalid/chat-b",
            "compatibility_group": "chat-primary",
            "auth": {
                "mode": "managed_identity",
                "scope": "https://cognitiveservices.azure.com/.default",
            },
        },
    ]

    with pytest.raises(ValidationError):
        RouterConfigModel.model_validate(config)
