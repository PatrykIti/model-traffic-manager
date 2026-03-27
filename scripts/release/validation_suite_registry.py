from __future__ import annotations

import json
import shlex
import sys
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ValidationSuite:
    suite_id: str
    scope_dir: str
    tests_path: str
    suite_kind: str
    has_scope_env_tfvars: bool
    requires_image: bool
    supports_kubernetes_version: bool
    manifest_root: str | None = None
    render_script: str | None = None
    render_requires_outputs: bool = False
    activation_env: str | None = None
    outputs_env: str | None = None
    mock_profile: str = "none"
    port_forward_mode: str = "service"
    nightly_enabled: bool = False
    release_enabled: bool = True


SUITES: dict[str, ValidationSuite] = {
    "integration-azure": ValidationSuite(
        suite_id="integration-azure",
        scope_dir="infra/integration-azure",
        tests_path="tests/integration_azure",
        suite_kind="integration",
        has_scope_env_tfvars=False,
        requires_image=False,
        supports_kubernetes_version=False,
        release_enabled=False,
    ),
    "integration-azure-chat": ValidationSuite(
        suite_id="integration-azure-chat",
        scope_dir="infra/integration-azure-chat",
        tests_path="tests/integration_azure_chat",
        suite_kind="integration",
        has_scope_env_tfvars=True,
        requires_image=False,
        supports_kubernetes_version=False,
        activation_env="RUN_INTEGRATION_AZURE_CHAT",
        outputs_env="INTEGRATION_AZURE_CHAT_OUTPUTS_JSON",
        nightly_enabled=True,
    ),
    "integration-azure-embeddings": ValidationSuite(
        suite_id="integration-azure-embeddings",
        scope_dir="infra/integration-azure-embeddings",
        tests_path="tests/integration_azure_embeddings",
        suite_kind="integration",
        has_scope_env_tfvars=True,
        requires_image=False,
        supports_kubernetes_version=False,
        activation_env="RUN_INTEGRATION_AZURE_EMBEDDINGS",
        outputs_env="INTEGRATION_AZURE_EMBEDDINGS_OUTPUTS_JSON",
        nightly_enabled=True,
    ),
    "e2e-aks": ValidationSuite(
        suite_id="e2e-aks",
        scope_dir="infra/e2e-aks",
        tests_path="tests/e2e_aks",
        suite_kind="aks",
        has_scope_env_tfvars=True,
        requires_image=True,
        supports_kubernetes_version=True,
        manifest_root="infra/e2e-aks",
        nightly_enabled=True,
    ),
    "e2e-aks-live-model": ValidationSuite(
        suite_id="e2e-aks-live-model",
        scope_dir="infra/e2e-aks-live-model",
        tests_path="tests/e2e_aks_live_model",
        suite_kind="aks",
        has_scope_env_tfvars=True,
        requires_image=True,
        supports_kubernetes_version=True,
        manifest_root="infra/e2e-aks-live-model",
        render_script="scripts/release/render_live_model_router_config.py",
        render_requires_outputs=True,
        activation_env="RUN_E2E_AKS_LIVE_MODEL",
        outputs_env="E2E_LIVE_MODEL_OUTPUTS_JSON",
        mock_profile="failover",
        nightly_enabled=True,
    ),
    "e2e-aks-live-embeddings": ValidationSuite(
        suite_id="e2e-aks-live-embeddings",
        scope_dir="infra/e2e-aks-live-embeddings",
        tests_path="tests/e2e_aks_live_embeddings",
        suite_kind="aks",
        has_scope_env_tfvars=True,
        requires_image=True,
        supports_kubernetes_version=True,
        manifest_root="infra/e2e-aks-live-embeddings",
        render_script="scripts/release/render_live_embeddings_router_config.py",
        render_requires_outputs=True,
        activation_env="RUN_E2E_AKS_LIVE_EMBEDDINGS",
        outputs_env="E2E_LIVE_EMBEDDINGS_OUTPUTS_JSON",
        nightly_enabled=True,
    ),
    "e2e-aks-live-load-balancing": ValidationSuite(
        suite_id="e2e-aks-live-load-balancing",
        scope_dir="infra/e2e-aks-live-load-balancing",
        tests_path="tests/e2e_aks_live_load_balancing",
        suite_kind="aks",
        has_scope_env_tfvars=True,
        requires_image=True,
        supports_kubernetes_version=True,
        manifest_root="infra/e2e-aks-live-load-balancing",
        render_script="scripts/release/render_live_load_balancing_router_config.py",
        render_requires_outputs=False,
        activation_env="RUN_E2E_AKS_LIVE_LOAD_BALANCING",
        mock_profile="load_balancing",
    ),
    "e2e-aks-live-shared-services": ValidationSuite(
        suite_id="e2e-aks-live-shared-services",
        scope_dir="infra/e2e-aks-live-shared-services",
        tests_path="tests/e2e_aks_live_shared_services",
        suite_kind="aks",
        has_scope_env_tfvars=True,
        requires_image=True,
        supports_kubernetes_version=True,
        manifest_root="infra/e2e-aks-live-shared-services",
        render_script="scripts/release/render_live_shared_services_router_config.py",
        render_requires_outputs=True,
        activation_env="RUN_E2E_AKS_LIVE_SHARED_SERVICES",
        outputs_env="E2E_LIVE_SHARED_SERVICES_OUTPUTS_JSON",
        mock_profile="shared_services",
    ),
    "e2e-aks-live-inbound-auth": ValidationSuite(
        suite_id="e2e-aks-live-inbound-auth",
        scope_dir="infra/e2e-aks-live-inbound-auth",
        tests_path="tests/e2e_aks_live_inbound_auth",
        suite_kind="aks",
        has_scope_env_tfvars=True,
        requires_image=True,
        supports_kubernetes_version=True,
        manifest_root="infra/e2e-aks-live-inbound-auth",
        render_script="scripts/release/render_live_inbound_auth_router_config.py",
        render_requires_outputs=True,
        activation_env="RUN_E2E_AKS_LIVE_INBOUND_AUTH",
        outputs_env="E2E_LIVE_INBOUND_AUTH_OUTPUTS_JSON",
        release_enabled=False,
    ),
    "e2e-aks-live-observability": ValidationSuite(
        suite_id="e2e-aks-live-observability",
        scope_dir="infra/e2e-aks-live-observability",
        tests_path="tests/e2e_aks_live_observability",
        suite_kind="aks",
        has_scope_env_tfvars=True,
        requires_image=True,
        supports_kubernetes_version=True,
        manifest_root="infra/e2e-aks-live-observability",
        render_script="scripts/release/render_live_observability_router_config.py",
        render_requires_outputs=True,
        activation_env="RUN_E2E_AKS_LIVE_OBSERVABILITY",
        outputs_env="E2E_LIVE_OBSERVABILITY_OUTPUTS_JSON",
        release_enabled=False,
    ),
    "e2e-aks-redis": ValidationSuite(
        suite_id="e2e-aks-redis",
        scope_dir="infra/e2e-aks-redis",
        tests_path="tests/e2e_aks_redis",
        suite_kind="aks",
        has_scope_env_tfvars=True,
        requires_image=True,
        supports_kubernetes_version=True,
        manifest_root="infra/e2e-aks-redis",
        render_script="scripts/release/render_live_redis_router_config.py",
        render_requires_outputs=True,
        activation_env="RUN_E2E_AKS_REDIS",
        mock_profile="redis",
        port_forward_mode="replicas",
    ),
}


def _shell_line(key: str, value: str | None) -> str:
    if value is None:
        return f"{key}=''"
    return f"{key}={shlex.quote(value)}"


def _bool_line(key: str, value: bool) -> str:
    return f"{key}={'1' if value else '0'}"


def _suite_or_die(suite_id: str) -> ValidationSuite:
    suite = SUITES.get(suite_id)
    if suite is None:
        known = ", ".join(sorted(SUITES))
        raise SystemExit(f"Unknown suite '{suite_id}'. Known suites: {known}")
    return suite


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit(
            "Usage: validation_suite_registry.py "
            "<list|list-scope-dirs|list-by-flag|matrix|shell> [arg]"
        )

    command = sys.argv[1]

    if command == "list":
        for suite_id in sorted(SUITES):
            print(suite_id)
        return

    if command == "list-scope-dirs":
        for scope_dir in sorted({suite.scope_dir for suite in SUITES.values()}):
            print(scope_dir)
        return

    if command == "list-by-flag":
        if len(sys.argv) != 3:
            raise SystemExit("Usage: validation_suite_registry.py list-by-flag <nightly|release>")
        flag_name = sys.argv[2]
        if flag_name == "nightly":
            selected = [suite.suite_id for suite in SUITES.values() if suite.nightly_enabled]
        elif flag_name == "release":
            selected = [suite.suite_id for suite in SUITES.values() if suite.release_enabled]
        else:
            raise SystemExit(f"Unknown flag '{flag_name}'.")
        for suite_id in sorted(selected):
            print(suite_id)
        return

    if command == "matrix":
        if len(sys.argv) != 3:
            raise SystemExit("Usage: validation_suite_registry.py matrix <nightly|release>")
        flag_name = sys.argv[2]
        if flag_name == "nightly":
            selected = [suite for suite in SUITES.values() if suite.nightly_enabled]
        elif flag_name == "release":
            selected = [suite for suite in SUITES.values() if suite.release_enabled]
        else:
            raise SystemExit(f"Unknown flag '{flag_name}'.")
        payload = {
            "include": [
                {
                    "suite": suite.suite_id,
                    "requires_image": suite.requires_image,
                }
                for suite in sorted(selected, key=lambda item: item.suite_id)
            ]
        }
        sys.stdout.write(json.dumps(payload))
        return

    if command == "shell":
        if len(sys.argv) != 3:
            raise SystemExit("Usage: validation_suite_registry.py shell <suite>")
        suite = _suite_or_die(sys.argv[2])
        lines = [
            _shell_line("suite_scope_dir", suite.scope_dir),
            _shell_line("suite_tests_path", suite.tests_path),
            _shell_line("suite_kind", suite.suite_kind),
            _bool_line("suite_has_scope_env_tfvars", suite.has_scope_env_tfvars),
            _bool_line("suite_requires_image", suite.requires_image),
            _bool_line(
                "suite_supports_kubernetes_version",
                suite.supports_kubernetes_version,
            ),
            _shell_line("suite_manifest_root", suite.manifest_root),
            _shell_line("suite_render_script", suite.render_script),
            _bool_line("suite_render_requires_outputs", suite.render_requires_outputs),
            _shell_line("suite_activation_env", suite.activation_env),
            _shell_line("suite_outputs_env", suite.outputs_env),
            _shell_line("suite_mock_profile", suite.mock_profile),
            _shell_line("suite_port_forward_mode", suite.port_forward_mode),
            _bool_line("suite_nightly_enabled", suite.nightly_enabled),
            _bool_line("suite_release_enabled", suite.release_enabled),
        ]
        sys.stdout.write("\n".join(lines))
        return

    raise SystemExit(f"Unsupported command '{command}'.")


if __name__ == "__main__":
    main()
