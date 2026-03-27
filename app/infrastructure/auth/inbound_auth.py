from __future__ import annotations

import hmac
import json
import time
from dataclasses import dataclass
from typing import Any

import httpx
import jwt
from jwt.algorithms import RSAAlgorithm

from app.application.dto.request_principal import RequestPrincipal
from app.domain.errors import InboundAuthenticationError, InboundAuthorizationError
from app.infrastructure.auth.env_secret_provider import EnvSecretProvider
from app.infrastructure.config.models import (
    ApiBearerTokenConfigModel,
    InboundAuthConfigModel,
)


@dataclass(frozen=True, slots=True)
class ApiBearerTokenProvider:
    token_id: str
    secret_ref: str
    display_name: str
    client_consumer_role: str | None


@dataclass(frozen=True, slots=True)
class EntraApplicationBinding:
    client_app_id: str
    display_name: str
    client_consumer_role: str | None
    required_app_roles: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class EntraIdProvider:
    tenant_id: str
    authority_host: str
    audiences: tuple[str, ...]
    applications: tuple[EntraApplicationBinding, ...]

    @property
    def openid_configuration_url(self) -> str:
        return f"{self.authority_host}/{self.tenant_id}/v2.0/.well-known/openid-configuration"


@dataclass(frozen=True, slots=True)
class InboundAuthPolicy:
    api_bearer_tokens: tuple[ApiBearerTokenProvider, ...] = ()
    entra_id: EntraIdProvider | None = None

    @property
    def enabled(self) -> bool:
        return bool(self.api_bearer_tokens or self.entra_id is not None)


class InboundAuthenticator:
    def __init__(
        self,
        *,
        policy: InboundAuthPolicy,
        secret_provider: EnvSecretProvider,
        metadata_client: httpx.Client | None = None,
        cache_ttl_seconds: int = 300,
    ) -> None:
        self._policy = policy
        self._secret_provider = secret_provider
        self._metadata_client = metadata_client or httpx.Client(timeout=10.0)
        self._cache_ttl_seconds = cache_ttl_seconds
        self._metadata_cache: tuple[float, dict[str, Any]] | None = None
        self._jwks_cache: tuple[float, dict[str, Any]] | None = None

    @classmethod
    def from_config(
        cls,
        inbound_auth_config: InboundAuthConfigModel | None,
        *,
        secret_provider: EnvSecretProvider,
        metadata_client: httpx.Client | None = None,
    ) -> InboundAuthenticator:
        if inbound_auth_config is None:
            return cls(
                policy=InboundAuthPolicy(),
                secret_provider=secret_provider,
                metadata_client=metadata_client,
            )

        api_bearer_tokens: list[ApiBearerTokenProvider] = []
        entra_provider: EntraIdProvider | None = None

        for provider in inbound_auth_config.providers:
            if isinstance(provider, ApiBearerTokenConfigModel):
                api_bearer_tokens.append(
                    ApiBearerTokenProvider(
                        token_id=provider.token_id,
                        secret_ref=provider.secret_ref,
                        display_name=provider.display_name or provider.token_id,
                        client_consumer_role=provider.consumer_role,
                    )
                )
                continue

            entra_provider = EntraIdProvider(
                tenant_id=provider.tenant_id,
                authority_host=provider.authority_host.rstrip("/"),
                audiences=tuple(provider.audiences),
                applications=tuple(
                    EntraApplicationBinding(
                        client_app_id=application.client_app_id,
                        display_name=application.display_name or application.client_app_id,
                        client_consumer_role=application.consumer_role,
                        required_app_roles=tuple(application.required_app_roles),
                    )
                    for application in provider.applications
                ),
            )

        return cls(
            policy=InboundAuthPolicy(
                api_bearer_tokens=tuple(api_bearer_tokens),
                entra_id=entra_provider,
            ),
            secret_provider=secret_provider,
            metadata_client=metadata_client,
        )

    @property
    def enabled(self) -> bool:
        return self._policy.enabled

    def close(self) -> None:
        self._metadata_client.close()

    def authenticate(self, authorization_header: str | None) -> RequestPrincipal:
        if not self._policy.enabled:
            raise InboundAuthenticationError("Inbound authentication is not configured.")
        if authorization_header is None:
            raise InboundAuthenticationError("Authorization header is required.")

        scheme, _, token = authorization_header.partition(" ")
        if scheme.lower() != "bearer" or not token:
            raise InboundAuthenticationError("Authorization header must use the Bearer scheme.")

        principal = self._authenticate_api_bearer_token(token)
        if principal is not None:
            return principal

        if self._policy.entra_id is None:
            raise InboundAuthenticationError("The provided bearer token is not recognized.")

        return self._authenticate_entra_id_token(token)

    def _authenticate_api_bearer_token(self, token: str) -> RequestPrincipal | None:
        for provider in self._policy.api_bearer_tokens:
            expected_token = self._secret_provider.get_secret(provider.secret_ref)
            if hmac.compare_digest(expected_token, token):
                return RequestPrincipal(
                    auth_mode="api_bearer_token",
                    principal_type="api_token",
                    principal_id=provider.token_id,
                    display_name=provider.display_name,
                    client_consumer_role=provider.client_consumer_role,
                    token_id=provider.token_id,
                )
        return None

    def _authenticate_entra_id_token(self, token: str) -> RequestPrincipal:
        provider = self._policy.entra_id
        assert provider is not None

        try:
            header = jwt.get_unverified_header(token)
        except jwt.PyJWTError as exc:
            raise InboundAuthenticationError("The bearer token is not a valid JWT.") from exc

        metadata = self._openid_metadata(provider)
        jwks = self._jwks(metadata["jwks_uri"])
        key = self._find_signing_key(jwks, header.get("kid"))

        try:
            claims = jwt.decode(
                token,
                key=key,
                algorithms=["RS256"],
                audience=list(provider.audiences),
                issuer=metadata["issuer"],
                options={"require": ["exp", "iat", "nbf", "iss", "aud"]},
            )
        except jwt.PyJWTError as exc:
            raise InboundAuthenticationError("The Entra access token failed validation.") from exc

        client_app_id = self._resolve_client_app_id(claims)
        application = next(
            (
                candidate
                for candidate in provider.applications
                if candidate.client_app_id == client_app_id
            ),
            None,
        )
        if application is None:
            raise InboundAuthorizationError("The Entra client application is not allowed.")

        roles = tuple(claim for claim in claims.get("roles", []) if isinstance(claim, str))
        if not roles:
            raise InboundAuthorizationError("The Entra token does not contain an allowed app role.")
        if not any(role in roles for role in application.required_app_roles):
            raise InboundAuthorizationError("The Entra token does not include a required app role.")

        return RequestPrincipal(
            auth_mode="entra_id",
            principal_type="service_principal",
            principal_id=client_app_id,
            display_name=application.display_name,
            client_consumer_role=application.client_consumer_role,
            entra_client_app_id=client_app_id,
            entra_tenant_id=provider.tenant_id,
            entra_roles=roles,
        )

    @staticmethod
    def _resolve_client_app_id(claims: dict[str, Any]) -> str:
        client_app_id = claims.get("azp") or claims.get("appid")
        if not isinstance(client_app_id, str) or not client_app_id:
            raise InboundAuthorizationError("The Entra token does not identify an app-only caller.")
        return client_app_id

    def _openid_metadata(self, provider: EntraIdProvider) -> dict[str, Any]:
        cache = self._metadata_cache
        now = time.time()
        if cache is not None and cache[0] > now:
            return cache[1]

        response = self._metadata_client.get(provider.openid_configuration_url)
        response.raise_for_status()
        metadata = response.json()
        if not isinstance(metadata, dict):
            raise InboundAuthenticationError("Invalid Entra OpenID configuration response.")
        self._metadata_cache = (now + self._cache_ttl_seconds, metadata)
        return metadata

    def _jwks(self, jwks_uri: str) -> dict[str, Any]:
        cache = self._jwks_cache
        now = time.time()
        if cache is not None and cache[0] > now:
            return cache[1]

        response = self._metadata_client.get(jwks_uri)
        response.raise_for_status()
        jwks = response.json()
        if not isinstance(jwks, dict):
            raise InboundAuthenticationError("Invalid Entra JWKS response.")
        self._jwks_cache = (now + self._cache_ttl_seconds, jwks)
        return jwks

    @staticmethod
    def _find_signing_key(jwks: dict[str, Any], key_id: Any) -> Any:
        if not isinstance(key_id, str) or not key_id:
            raise InboundAuthenticationError("The Entra token does not include a signing key ID.")

        keys = jwks.get("keys")
        if not isinstance(keys, list):
            raise InboundAuthenticationError("The Entra JWKS payload is missing signing keys.")

        for jwk in keys:
            if not isinstance(jwk, dict) or jwk.get("kid") != key_id:
                continue
            return RSAAlgorithm.from_jwk(json.dumps(jwk))

        raise InboundAuthenticationError("No matching Entra signing key was found for the token.")
