from __future__ import annotations

from azure.core.credentials import AccessToken

from app.domain.errors import TokenAcquisitionError
from app.infrastructure.auth.managed_identity_token_provider import ManagedIdentityTokenProvider


class FakeCredential:
    def __init__(self, tokens: list[AccessToken]) -> None:
        self._tokens = tokens
        self.calls: list[str] = []

    def get_token(self, scope: str) -> AccessToken:
        self.calls.append(scope)
        return self._tokens.pop(0)


def test_managed_identity_token_provider_caches_valid_tokens() -> None:
    credential = FakeCredential([AccessToken("token-1", expires_on=1_000)])
    provider = ManagedIdentityTokenProvider(
        credential_factory=lambda client_id: credential,
        refresh_buffer_seconds=60,
        now_provider=lambda: 100,
    )

    first = provider.get_token("https://cognitiveservices.azure.com/.default")
    second = provider.get_token("https://cognitiveservices.azure.com/.default")

    assert first == "token-1"
    assert second == "token-1"
    assert credential.calls == ["https://cognitiveservices.azure.com/.default"]


def test_managed_identity_token_provider_refreshes_near_expiry() -> None:
    credential = FakeCredential(
        [
            AccessToken("token-1", expires_on=120),
            AccessToken("token-2", expires_on=1_000),
        ]
    )
    current_time = 100
    provider = ManagedIdentityTokenProvider(
        credential_factory=lambda client_id: credential,
        refresh_buffer_seconds=30,
        now_provider=lambda: current_time,
    )

    first = provider.get_token("https://cognitiveservices.azure.com/.default")
    second = provider.get_token("https://cognitiveservices.azure.com/.default")

    assert first == "token-1"
    assert second == "token-2"
    assert credential.calls == [
        "https://cognitiveservices.azure.com/.default",
        "https://cognitiveservices.azure.com/.default",
    ]


def test_managed_identity_token_provider_uses_client_id_in_cache_key() -> None:
    shared_credential = FakeCredential(
        [
            AccessToken("token-a", expires_on=1_000),
            AccessToken("token-b", expires_on=1_000),
        ]
    )
    provider = ManagedIdentityTokenProvider(
        credential_factory=lambda client_id: shared_credential,
        refresh_buffer_seconds=60,
        now_provider=lambda: 100,
    )

    first = provider.get_token(
        "https://cognitiveservices.azure.com/.default",
        client_id="client-a",
    )
    second = provider.get_token(
        "https://cognitiveservices.azure.com/.default",
        client_id="client-b",
    )

    assert first == "token-a"
    assert second == "token-b"
    assert shared_credential.calls == [
        "https://cognitiveservices.azure.com/.default",
        "https://cognitiveservices.azure.com/.default",
    ]


def test_managed_identity_token_provider_wraps_credential_failures() -> None:
    class FailingCredential:
        def get_token(self, scope: str) -> AccessToken:
            raise RuntimeError("credential failure")

    provider = ManagedIdentityTokenProvider(
        credential_factory=lambda client_id: FailingCredential(),
        now_provider=lambda: 100,
    )

    try:
        provider.get_token("https://cognitiveservices.azure.com/.default")
    except TokenAcquisitionError as exc:
        assert "https://cognitiveservices.azure.com/.default" in str(exc)
    else:  # pragma: no cover - defensive assertion
        raise AssertionError("TokenAcquisitionError was not raised")
