from __future__ import annotations

import os

from app.domain.errors import SecretResolutionError


class EnvSecretProvider:
    ENV_PREFIX = "env://"

    def get_secret(self, secret_ref: str) -> str:
        if not secret_ref.startswith(self.ENV_PREFIX):
            raise SecretResolutionError(
                "Only env:// secret references are supported in Phase 2."
            )

        env_var_name = secret_ref.removeprefix(self.ENV_PREFIX)
        if not env_var_name:
            raise SecretResolutionError(
                "Secret reference must include an environment variable name."
            )

        value = os.getenv(env_var_name)
        if value is None:
            raise SecretResolutionError(
                f"Environment variable '{env_var_name}' is not set for secret resolution."
            )

        return value
