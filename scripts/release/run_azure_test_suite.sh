#!/usr/bin/env bash
set -Eeuo pipefail

SUITE="${1:-}"
ENVIRONMENT="${2:-dev1}"

if [[ -z "$SUITE" ]]; then
  echo "Usage: bash scripts/release/run_azure_test_suite.sh <integration-azure|integration-azure-chat|integration-azure-embeddings|e2e-aks|e2e-aks-live-model|e2e-aks-live-embeddings|e2e-aks-live-load-balancing|e2e-aks-live-shared-services|e2e-aks-live-observability|e2e-aks-redis> [environment]" >&2
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

select_running_pod() {
  local namespace="$1"
  local label_selector="$2"

  kubectl get pods -n "$namespace" -l "$label_selector" \
    -o jsonpath='{range .items[?(@.status.phase=="Running")]}{.metadata.name}{"\n"}{end}' \
    | head -n 1
}

select_running_pods() {
  local namespace="$1"
  local label_selector="$2"
  local count="${3:-0}"

  if [[ "$count" == "0" ]]; then
    kubectl get pods -n "$namespace" -l "$label_selector" \
      -o jsonpath='{range .items[?(@.status.phase=="Running")]}{.metadata.name}{"\n"}{end}'
    return
  fi

  kubectl get pods -n "$namespace" -l "$label_selector" \
    -o jsonpath='{range .items[?(@.status.phase=="Running")]}{.metadata.name}{"\n"}{end}' \
    | head -n "$count"
}

allocate_local_port() {
  python3 -c 'import socket; sock = socket.socket(); sock.bind(("127.0.0.1", 0)); print(sock.getsockname()[1]); sock.close()'
}

slugify_label() {
  printf '%s' "$1" | tr -cs '[:alnum:]._-' '-'
}

resolve_executor_principal_id() {
  local access_token
  access_token="$(az account get-access-token --resource-type arm --query accessToken -o tsv)"
  python3 -c '
import base64
import json
import sys

token = sys.stdin.read().strip()
payload = token.split(".")[1]
payload += "=" * (-len(payload) % 4)
claims = json.loads(base64.urlsafe_b64decode(payload))
print(claims.get("oid", ""))
' <<<"$access_token"
}

json_output_value() {
  local outputs_path="$1"
  local output_name="$2"

  python3 - "$outputs_path" "$output_name" <<'PY'
import json
import sys
from pathlib import Path

outputs = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
entry = outputs.get(sys.argv[2], {})
value = entry.get("value", "")
if value is None:
    value = ""
print(value)
PY
}

retry_command_with_policy() {
  local policy="$1"
  local label="$2"
  local attempts="$3"
  local base_delay_seconds="$4"
  shift 4

  local attempt exit_code delay_seconds log_file label_slug
  label_slug="$(slugify_label "$label")"

  for ((attempt = 1; attempt <= attempts; attempt++)); do
    log_file="${artifacts_dir}/retry-${label_slug}-${attempt}.log"
    echo "Running ${label} (attempt ${attempt}/${attempts})"
    if "$@" > >(tee "$log_file") 2> >(tee -a "$log_file" >&2); then
      return 0
    fi
    exit_code=$?
    if (( attempt == attempts )); then
      return "$exit_code"
    fi
    if ! python3 scripts/release/retry_policy.py should-retry "$policy" "$log_file"; then
      return "$exit_code"
    fi
    delay_seconds=$((base_delay_seconds * attempt))
    echo "Retrying ${label} in ${delay_seconds}s because retry policy '${policy}' matched." >&2
    sleep "$delay_seconds"
  done

  return 1
}

retry_shell_with_policy() {
  local policy="$1"
  local label="$2"
  local attempts="$3"
  local base_delay_seconds="$4"
  local command_string="$5"

  retry_command_with_policy "$policy" "$label" "$attempts" "$base_delay_seconds" \
    bash -lc "$command_string"
}

wait_for_http_endpoint() {
  local url="$1"
  local timeout_seconds="${2:-60}"
  local watched_pid="${3:-}"
  local log_path="${4:-}"
  local elapsed=0

  while (( elapsed < timeout_seconds )); do
    if [[ -n "$watched_pid" ]] && ! kill -0 "$watched_pid" >/dev/null 2>&1; then
      echo "Port-forward process exited before ${url} became reachable." >&2
      if [[ -n "$log_path" && -f "$log_path" ]]; then
        echo "----- port-forward log -----" >&2
        cat "$log_path" >&2 || true
      fi
      return 1
    fi

    if python3 -c 'import sys, urllib.request; urllib.request.urlopen(sys.argv[1], timeout=2)' "$url" >/dev/null 2>&1; then
      return 0
    fi

    sleep 1
    elapsed=$((elapsed + 1))
  done

  echo "Timed out waiting for ${url}." >&2
  if [[ -n "$log_path" && -f "$log_path" ]]; then
    echo "----- port-forward log -----" >&2
    cat "$log_path" >&2 || true
  fi
  return 1
}

for cmd in az terraform uv python3; do
  require_cmd "$cmd"
done

subscription_id="$(az account show --query id -o tsv)"
tenant_id="$(az account show --query tenantId -o tsv)"
account_name="$(az account show --query name -o tsv)"
run_id="local-$(date -u +%Y%m%d%H%M%S)-$RANDOM"
tmp_dir="$(mktemp -d "${TMPDIR:-/tmp}/mtm-${SUITE}-XXXXXX")"
artifacts_root="${VALIDATION_ARTIFACTS_ROOT:-${RUNNER_TEMP:-${TMPDIR:-/tmp}}/mtm-artifacts}"
artifacts_dir="${artifacts_root}/${SUITE}-${run_id}"
mkdir -p "$artifacts_dir"
suite_log_path="${artifacts_dir}/suite-run.log"
pytest_flags=(-vv -rA)
executor_principal_id=""

exec > >(tee -a "$suite_log_path") 2>&1

eval "$(python3 scripts/release/validation_suite_registry.py shell "$SUITE")"
scope_dir="$suite_scope_dir"
tests_path="$suite_tests_path"

tf_args=(
  "-var-file=../_shared/env/${ENVIRONMENT}.tfvars"
  "-var=subscription_id=${subscription_id}"
  "-var=run_id=${run_id}"
)

if [[ "$suite_has_scope_env_tfvars" == "1" ]]; then
  tf_args+=("-var-file=env/${ENVIRONMENT}.tfvars")
fi

if [[ "$suite_supports_kubernetes_version" == "1" && -n "${KUBERNETES_VERSION:-}" ]]; then
  tf_args+=("-var=kubernetes_version=${KUBERNETES_VERSION}")
fi

if [[ "$suite_kind" == "aks" ]]; then
  for cmd in docker gh kubectl; do
    require_cmd "$cmd"
  done
fi

if [[ "$SUITE" == "integration-azure-chat" || "$SUITE" == "integration-azure-embeddings" ]]; then
  executor_principal_id="$(resolve_executor_principal_id)"
  if [[ -n "$executor_principal_id" ]]; then
    tf_args+=("-var=executor_principal_id=${executor_principal_id}")
  fi
fi

apply_started="0"
port_forward_pids=()
resource_group=""
aks_cluster_name=""
e2e_namespace="${E2E_NAMESPACE:-e2e-router}"
e2e_image="${E2E_IMAGE:-}"
federated_credential_created="0"
e2e_image_pull_secret_name="${E2E_IMAGE_PULL_SECRET_NAME:-ghcr-pull}"
cleanup_status="not_started"
rendered_router_config=""
namespace_create_status="not_created"
namespace_delete_status="not_created"
federated_credential_create_status="not_created"
federated_credential_delete_status="not_created"
image_pull_secret_create_status="not_created"
port_forward_teardown_status="not_created"

write_run_metadata() {
  cat >"${artifacts_dir}/run-metadata.json" <<EOF
{
  "suite": "${SUITE}",
  "environment": "${ENVIRONMENT}",
  "run_id": "${run_id}",
  "scope_dir": "${scope_dir}",
  "tests_path": "${tests_path}",
  "suite_kind": "${suite_kind}"
}
EOF
}

write_run_metadata

write_cleanup_report() {
  cat >"${artifacts_dir}/cleanup-report.json" <<EOF
{
  "suite": "${SUITE}",
  "cleanup_status": "${cleanup_status}",
  "namespace_create_status": "${namespace_create_status}",
  "namespace_delete_status": "${namespace_delete_status}",
  "federated_credential_create_status": "${federated_credential_create_status}",
  "federated_credential_delete_status": "${federated_credential_delete_status}",
  "image_pull_secret_create_status": "${image_pull_secret_create_status}",
  "port_forward_teardown_status": "${port_forward_teardown_status}"
}
EOF
}

print_e2e_diagnostics() {
  if [[ "$suite_kind" != "aks" || -z "$aks_cluster_name" ]]; then
    return
  fi

  echo "----- e2e-aks diagnostics: kubectl get all -----" >&2
  kubectl get all -n "$e2e_namespace" >&2 || true

  echo "----- e2e-aks diagnostics: deployment describe -----" >&2
  kubectl describe deployment/router-app -n "$e2e_namespace" >&2 || true

  while IFS= read -r pod_name; do
    [[ -z "$pod_name" ]] && continue
    echo "----- e2e-aks diagnostics: describe ${pod_name} -----" >&2
    kubectl describe -n "$e2e_namespace" "pod/${pod_name}" >&2 || true
    echo "----- e2e-aks diagnostics: logs ${pod_name} -----" >&2
    kubectl logs -n "$e2e_namespace" "pod/${pod_name}" --all-containers=true --tail=200 >&2 || true
  done < <(kubectl get pods -n "$e2e_namespace" -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}' 2>/dev/null || true)

  echo "----- e2e-aks diagnostics: events -----" >&2
  kubectl get events -n "$e2e_namespace" --sort-by=.metadata.creationTimestamp >&2 || true

  for pf_log in "${tmp_dir}"/port-forward*.log; do
    [[ -e "$pf_log" ]] || continue
    echo "----- e2e-aks diagnostics: $(basename "$pf_log") -----" >&2
    cat "$pf_log" >&2 || true
  done
}

collect_suite_artifacts() {
  if [[ -f "${tmp_dir}/terraform-outputs.json" ]]; then
    cp "${tmp_dir}/terraform-outputs.json" "${artifacts_dir}/terraform-outputs.json" || true
  fi

  if [[ -n "$rendered_router_config" && -f "$rendered_router_config" ]]; then
    cp "$rendered_router_config" "${artifacts_dir}/router-config.yaml" || true
  fi

  for pf_log in "${tmp_dir}"/port-forward*.log; do
    [[ -e "$pf_log" ]] || continue
    cp "$pf_log" "${artifacts_dir}/$(basename "$pf_log")" || true
  done

  if [[ "$suite_kind" != "aks" || -z "$aks_cluster_name" ]]; then
    return
  fi

  kubectl get all -n "$e2e_namespace" > "${artifacts_dir}/kubectl-get-all.txt" 2>&1 || true
  kubectl describe deployment/router-app -n "$e2e_namespace" > "${artifacts_dir}/router-app-deployment.txt" 2>&1 || true
  kubectl get events -n "$e2e_namespace" --sort-by=.metadata.creationTimestamp > "${artifacts_dir}/kubectl-events.txt" 2>&1 || true

  while IFS= read -r pod_name; do
    [[ -z "$pod_name" ]] && continue
    kubectl describe -n "$e2e_namespace" "pod/${pod_name}" > "${artifacts_dir}/pod-${pod_name}-describe.txt" 2>&1 || true
    kubectl logs -n "$e2e_namespace" "pod/${pod_name}" --all-containers=true --tail=200 > "${artifacts_dir}/pod-${pod_name}-logs.txt" 2>&1 || true
  done < <(kubectl get pods -n "$e2e_namespace" -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}' 2>/dev/null || true)
}

on_error() {
  local line_no="$1"
  local failed_command="$2"
  local exit_code="$3"

  echo "Error: command failed at line ${line_no}: ${failed_command}" >&2
  print_e2e_diagnostics
  exit "$exit_code"
}

cleanup() {
  exit_code=$?
  destroy_exit_code=0

  if (( ${#port_forward_pids[@]} > 0 )); then
    port_forward_teardown_status="deleted"
    for pf_pid in "${port_forward_pids[@]}"; do
      echo "Cleaning up: stopping port-forward process ${pf_pid}"
      if kill -0 "$pf_pid" >/dev/null 2>&1; then
        if ! kill "$pf_pid" >/dev/null 2>&1; then
          port_forward_teardown_status="cleanup_failed"
        fi
      elif [[ "$port_forward_teardown_status" != "cleanup_failed" ]]; then
        port_forward_teardown_status="already_gone"
      fi
    done
  else
    port_forward_teardown_status="not_created"
  fi

  collect_suite_artifacts

  if [[ "$suite_kind" == "aks" && "$federated_credential_created" == "1" && -n "$resource_group" && -n "${UAI_NAME:-}" ]]; then
    echo "Cleaning up: deleting federated credential router-e2e-${run_id}"
    if az identity federated-credential show \
      --resource-group "$resource_group" \
      --identity-name "$UAI_NAME" \
      --name "router-e2e-${run_id}" >/dev/null 2>&1; then
      if az identity federated-credential delete \
        --resource-group "$resource_group" \
        --identity-name "$UAI_NAME" \
        --name "router-e2e-${run_id}" \
        --yes >/dev/null 2>&1; then
        federated_credential_delete_status="deleted"
      else
        federated_credential_delete_status="cleanup_failed"
      fi
    else
      federated_credential_delete_status="already_gone"
    fi
  elif [[ "$suite_kind" == "aks" ]]; then
    federated_credential_delete_status="not_created"
  else
    federated_credential_delete_status="not_created"
  fi

  if [[ "$suite_kind" == "aks" ]]; then
    echo "Cleaning up: deleting namespace ${e2e_namespace}"
    if kubectl get namespace "$e2e_namespace" >/dev/null 2>&1; then
      if kubectl delete namespace "$e2e_namespace" --wait=false >/dev/null 2>&1; then
        namespace_delete_status="deleted"
      else
        namespace_delete_status="cleanup_failed"
      fi
    else
      namespace_delete_status="already_gone"
    fi
  fi

  if [[ "$apply_started" == "1" ]]; then
    echo "Cleaning up: running terraform destroy for ${SUITE}"
    if ! terraform -chdir="$scope_dir" destroy -auto-approve -input=false "${tf_args[@]}"; then
      destroy_exit_code=$?
      echo "Cleanup warning: terraform destroy failed for ${SUITE}" >&2
    fi
  fi

  if [[ "$exit_code" -eq 0 && "$destroy_exit_code" -eq 0 ]]; then
    cleanup_status="clean"
  elif [[ "$destroy_exit_code" -ne 0 ]]; then
    cleanup_status="cleanup_failed"
  else
    cleanup_status="suite_failed_but_cleanup_succeeded"
  fi

  write_cleanup_report

  python3 scripts/release/write_validation_artifact_manifest.py \
    "$artifacts_dir" \
    "$SUITE" \
    "$ENVIRONMENT" \
    "$run_id" \
    "$scope_dir" \
    "$tests_path" \
    "$suite_kind" \
    "$exit_code" \
    "$cleanup_status"

  rm -rf "$tmp_dir"

  if [[ "$exit_code" -eq 0 && "$destroy_exit_code" -ne 0 ]]; then
    exit "$destroy_exit_code"
  fi

  exit "$exit_code"
}

trap cleanup EXIT INT TERM
trap 'on_error "$LINENO" "$BASH_COMMAND" "$?"' ERR

echo "Azure account: ${account_name}"
echo "Subscription: ${subscription_id}"
echo "Tenant: ${tenant_id}"
echo "Suite: ${SUITE}"
echo "Environment: ${ENVIRONMENT}"
echo "Run ID: ${run_id}"

if [[ "$suite_requires_image" == "1" && -z "$e2e_image" ]]; then
  require_cmd docker
  require_cmd gh

  if ! docker info >/dev/null 2>&1; then
    echo "Docker daemon is not available. Start Docker or set E2E_IMAGE to a prebuilt image." >&2
    exit 1
  fi

  if ! docker buildx version >/dev/null 2>&1; then
    echo "Docker buildx is required for e2e-aks image builds." >&2
    exit 1
  fi

  ghcr_owner="${GHCR_OWNER:-$(gh api user -q .login)}"
  ghcr_username="${GHCR_USERNAME:-$ghcr_owner}"
  ghcr_token="${GHCR_TOKEN:-$(gh auth token)}"
  e2e_image="ghcr.io/${ghcr_owner,,}/model-traffic-manager:e2e-local-${run_id}"
  e2e_image_platform="${E2E_IMAGE_PLATFORM:-linux/amd64}"

  export GHCR_LOGIN_USERNAME="$ghcr_username"
  export GHCR_LOGIN_TOKEN="$ghcr_token"
  retry_shell_with_policy \
    "ghcr_auth" \
    "docker login ghcr.io" \
    3 \
    2 \
    'printf "%s" "$GHCR_LOGIN_TOKEN" | docker login ghcr.io -u "$GHCR_LOGIN_USERNAME" --password-stdin'
  retry_command_with_policy \
    "ghcr_build_push" \
    "docker buildx build --push" \
    3 \
    5 \
    docker buildx build \
      --platform "$e2e_image_platform" \
      -f docker/Dockerfile \
      -t "$e2e_image" \
      --push \
      .
fi

terraform -chdir="$scope_dir" init -backend=false
apply_started="1"
retry_command_with_policy \
  "terraform_apply" \
  "terraform apply for ${SUITE}" \
  2 \
  10 \
  terraform -chdir="$scope_dir" apply -auto-approve -input=false "${tf_args[@]}"
terraform -chdir="$scope_dir" output -json > "${tmp_dir}/terraform-outputs.json"
cp "${tmp_dir}/terraform-outputs.json" "${artifacts_dir}/terraform-outputs.json"

if [[ "$suite_kind" == "integration" ]]; then
  export RUN_INTEGRATION_AZURE="1"
  export INTEGRATION_AZURE_SCOPE="${INTEGRATION_AZURE_SCOPE:-https://management.azure.com/.default}"
  if [[ -n "$suite_activation_env" ]]; then
    export "${suite_activation_env}=1"
  fi
  if [[ -n "$suite_outputs_env" ]]; then
    export "${suite_outputs_env}=${tmp_dir}/terraform-outputs.json"
  fi
  export VALIDATION_ARTIFACTS_DIR="$artifacts_dir"

  echo "Running pytest with flags: ${pytest_flags[*]}"
  uv run pytest "$tests_path" "${pytest_flags[@]}" 2>&1 | tee "${artifacts_dir}/pytest.log"
  exit 0
fi

resource_group="$(terraform -chdir="$scope_dir" output -raw resource_group_name)"
aks_cluster_name="$(terraform -chdir="$scope_dir" output -raw aks_cluster_name)"
aks_oidc_issuer_url="$(terraform -chdir="$scope_dir" output -raw aks_oidc_issuer_url)"
UAI_NAME="$(terraform -chdir="$scope_dir" output -raw user_assigned_identity_name)"
uai_client_id="$(terraform -chdir="$scope_dir" output -raw user_assigned_identity_client_id)"

kubeconfig_path="${tmp_dir}/kubeconfig"
retry_command_with_policy \
  "azure_control_plane" \
  "az aks get-credentials for ${SUITE}" \
  3 \
  3 \
  az aks get-credentials \
  --resource-group "$resource_group" \
  --name "$aks_cluster_name" \
  --file "$kubeconfig_path" \
  --overwrite-existing
export KUBECONFIG="$kubeconfig_path"
retry_command_with_policy \
  "azure_control_plane" \
  "az identity federated-credential create" \
  3 \
  3 \
  az identity federated-credential create \
  --resource-group "$resource_group" \
  --identity-name "$UAI_NAME" \
  --name "router-e2e-${run_id}" \
  --issuer "$aks_oidc_issuer_url" \
  --subject "system:serviceaccount:${e2e_namespace}:router-app" \
  --audiences "api://AzureADTokenExchange"
federated_credential_created="1"
federated_credential_create_status="created"

if kubectl get namespace "$e2e_namespace" >/dev/null 2>&1; then
  namespace_create_status="already_exists"
else
  namespace_create_status="created"
fi
kubectl create namespace "$e2e_namespace" --dry-run=client -o yaml | kubectl apply -f -

if [[ -n "$suite_render_script" ]]; then
  rendered_router_config="${tmp_dir}/router-${SUITE}.yaml"
  if [[ "$suite_render_requires_outputs" == "1" ]]; then
    python3 "$suite_render_script" "${tmp_dir}/terraform-outputs.json" > "$rendered_router_config"
  else
    python3 "$suite_render_script" > "$rendered_router_config"
  fi
  cp "$rendered_router_config" "${artifacts_dir}/router-config.yaml"
  kubectl create configmap router-config \
    --from-file=router.yaml="$rendered_router_config" \
    --namespace "$e2e_namespace" \
    --dry-run=client -o yaml | kubectl apply -f -
else
  kubectl create configmap router-config \
    --from-file=router.yaml=configs/example.router.yaml \
    --namespace "$e2e_namespace" \
    --dry-run=client -o yaml | kubectl apply -f -
fi

export E2E_NAMESPACE="$e2e_namespace"
export E2E_IMAGE="$e2e_image"
export E2E_UAI_CLIENT_ID="$uai_client_id"
export VALIDATION_ARTIFACTS_DIR="$artifacts_dir"

application_insights_name="$(json_output_value "${tmp_dir}/terraform-outputs.json" "application_insights_name")"
if [[ -n "$application_insights_name" ]]; then
  az extension add --name application-insights --upgrade --only-show-errors >/dev/null
  app_insights_connection_string="$(
    az monitor app-insights component show \
      --app "$application_insights_name" \
      --resource-group "$resource_group" \
      --query connectionString \
      -o tsv
  )"
  kubectl create secret generic router-observability \
    --from-literal=connection-string="$app_insights_connection_string" \
    --namespace "$e2e_namespace" \
    --dry-run=client -o yaml | kubectl apply -f -
fi

if [[ "$e2e_image" == ghcr.io/* ]]; then
  ghcr_username="${GHCR_USERNAME:-}"
  if [[ -z "$ghcr_username" ]]; then
    ghcr_username="${GHCR_OWNER:-}"
  fi
  if [[ -z "$ghcr_username" ]]; then
    ghcr_username="$(gh api user -q .login 2>/dev/null || true)"
  fi

  ghcr_token="${GHCR_TOKEN:-}"
  if [[ -z "$ghcr_token" ]]; then
    ghcr_token="$(gh auth token 2>/dev/null || true)"
  fi

  if [[ -z "$ghcr_username" || -z "$ghcr_token" ]]; then
    echo "Private GHCR image pull requires GHCR_TOKEN and GHCR_USERNAME (or an authenticated gh cli session)." >&2
    exit 1
  fi

  echo "Configuring image pull secret ${e2e_image_pull_secret_name} for ${e2e_namespace}"
  if kubectl get secret "$e2e_image_pull_secret_name" -n "$e2e_namespace" >/dev/null 2>&1; then
    image_pull_secret_create_status="already_exists"
  else
    image_pull_secret_create_status="created"
  fi
  kubectl create secret docker-registry "$e2e_image_pull_secret_name" \
    --docker-server=ghcr.io \
    --docker-username="$ghcr_username" \
    --docker-password="$ghcr_token" \
    --namespace "$e2e_namespace" \
    --dry-run=client -o yaml | kubectl apply -f -
fi

manifest_root="$suite_manifest_root"

python3 scripts/release/render_template.py "${manifest_root}/k8s/router-serviceaccount.yaml.tmpl" | kubectl apply -f -
if [[ "$e2e_image" == ghcr.io/* ]]; then
  kubectl patch serviceaccount/router-app \
    -n "$e2e_namespace" \
    --type merge \
    -p "{\"imagePullSecrets\":[{\"name\":\"${e2e_image_pull_secret_name}\"}]}"
fi
python3 scripts/release/render_template.py "${manifest_root}/k8s/router-deployment.yaml.tmpl" | kubectl apply -f -
kubectl apply -n "$e2e_namespace" -f "${manifest_root}/k8s/router-service.yaml"
if [[ "$suite_mock_profile" == "failover" ]]; then
  python3 scripts/release/render_template.py "${manifest_root}/k8s/router-failover-mock-deployment.yaml.tmpl" | kubectl apply -f -
  kubectl apply -n "$e2e_namespace" -f "${manifest_root}/k8s/router-failover-mock-service.yaml"
  retry_command_with_policy "kubernetes_watch" "router-failover-mock rollout" 3 2 \
    kubectl rollout status deployment/router-failover-mock -n "$e2e_namespace" --timeout=5m
  retry_command_with_policy "kubernetes_watch" "router-failover-mock pod wait" 3 2 \
    kubectl wait --for=condition=Ready pod -l app=router-failover-mock -n "$e2e_namespace" --timeout=5m
elif [[ "$suite_mock_profile" == "load_balancing" ]]; then
  python3 scripts/release/render_template.py "${manifest_root}/k8s/router-lb-mock-deployment.yaml.tmpl" | kubectl apply -f -
  kubectl apply -n "$e2e_namespace" -f "${manifest_root}/k8s/router-lb-mock-service.yaml"
  retry_command_with_policy "kubernetes_watch" "router-lb-mock rollout" 3 2 \
    kubectl rollout status deployment/router-lb-mock -n "$e2e_namespace" --timeout=5m
  retry_command_with_policy "kubernetes_watch" "router-lb-mock pod wait" 3 2 \
    kubectl wait --for=condition=Ready pod -l app=router-lb-mock -n "$e2e_namespace" --timeout=5m
elif [[ "$suite_mock_profile" == "shared_services" ]]; then
  python3 scripts/release/render_template.py "${manifest_root}/k8s/router-shared-service-mock-deployment.yaml.tmpl" | kubectl apply -f -
  kubectl apply -n "$e2e_namespace" -f "${manifest_root}/k8s/router-shared-service-mock-service.yaml"
  retry_command_with_policy "kubernetes_watch" "router-shared-service-mock rollout" 3 2 \
    kubectl rollout status deployment/router-shared-service-mock -n "$e2e_namespace" --timeout=5m
  retry_command_with_policy "kubernetes_watch" "router-shared-service-mock pod wait" 3 2 \
    kubectl wait --for=condition=Ready pod -l app=router-shared-service-mock -n "$e2e_namespace" --timeout=5m
elif [[ "$suite_mock_profile" == "redis" ]]; then
  kubectl apply -n "$e2e_namespace" -f "${manifest_root}/k8s/router-redis-deployment.yaml"
  kubectl apply -n "$e2e_namespace" -f "${manifest_root}/k8s/router-redis-service.yaml"
  retry_command_with_policy "kubernetes_watch" "router-redis rollout" 3 2 \
    kubectl rollout status deployment/router-redis -n "$e2e_namespace" --timeout=5m
  retry_command_with_policy "kubernetes_watch" "router-redis pod wait" 3 2 \
    kubectl wait --for=condition=Ready pod -l app=router-redis -n "$e2e_namespace" --timeout=5m
  python3 scripts/release/render_template.py "${manifest_root}/k8s/router-redis-mock-deployment.yaml.tmpl" | kubectl apply -f -
  kubectl apply -n "$e2e_namespace" -f "${manifest_root}/k8s/router-redis-mock-service.yaml"
  retry_command_with_policy "kubernetes_watch" "router-redis-mock rollout" 3 2 \
    kubectl rollout status deployment/router-redis-mock -n "$e2e_namespace" --timeout=5m
  retry_command_with_policy "kubernetes_watch" "router-redis-mock pod wait" 3 2 \
    kubectl wait --for=condition=Ready pod -l app=router-redis-mock -n "$e2e_namespace" --timeout=5m
fi

retry_command_with_policy "kubernetes_watch" "router-app rollout" 3 2 \
  kubectl rollout status deployment/router-app -n "$e2e_namespace" --timeout=5m
retry_command_with_policy "kubernetes_watch" "router-app pod wait" 3 2 \
  kubectl wait --for=condition=Ready pod -l app=router-app -n "$e2e_namespace" --timeout=5m

router_pod_name="$(select_running_pod "$e2e_namespace" "app=router-app")"
if [[ -z "$router_pod_name" ]]; then
  echo "Could not resolve a running router-app pod after readiness wait." >&2
  exit 1
fi

kubectl exec -n "$e2e_namespace" "pod/${router_pod_name}" -c router -- sh -lc \
  'test -n "$AZURE_FEDERATED_TOKEN_FILE" && test -f "$AZURE_FEDERATED_TOKEN_FILE"'

kubectl exec -n "$e2e_namespace" "pod/${router_pod_name}" -c router -- sh -lc \
  '/app/.venv/bin/python -c "from azure.identity import DefaultAzureCredential; token = DefaultAzureCredential().get_token(\"https://management.azure.com/.default\"); assert token.token; print(len(token.token))"'

export RUN_E2E_AKS="1"

if [[ "$suite_port_forward_mode" == "replicas" ]]; then
  mapfile -t router_pod_names < <(select_running_pods "$e2e_namespace" "app=router-app" 2)
  if (( ${#router_pod_names[@]} < 2 )); then
    echo "Expected two running router-app pods for e2e-aks-redis." >&2
    exit 1
  fi

  replica_a_port="$(allocate_local_port)"
  replica_a_log="${tmp_dir}/port-forward-replica-a.log"
  for attempt in 1 2 3; do
    kubectl port-forward -n "$e2e_namespace" "pod/${router_pod_names[0]}" "${replica_a_port}:8000" >"${replica_a_log}" 2>&1 &
    replica_a_pid=$!
    if wait_for_http_endpoint "http://127.0.0.1:${replica_a_port}/health/ready" 60 "$replica_a_pid" "$replica_a_log"; then
      port_forward_pids+=("$replica_a_pid")
      break
    fi
    kill "$replica_a_pid" >/dev/null 2>&1 || true
    if ! python3 scripts/release/retry_policy.py should-retry "port_forward_start" "$replica_a_log"; then
      exit 1
    fi
    sleep $((2 * attempt))
  done
  if ! kill -0 "$replica_a_pid" >/dev/null 2>&1; then
    echo "Failed to establish port-forward for replica A." >&2
    exit 1
  fi

  replica_b_port="$(allocate_local_port)"
  replica_b_log="${tmp_dir}/port-forward-replica-b.log"
  for attempt in 1 2 3; do
    kubectl port-forward -n "$e2e_namespace" "pod/${router_pod_names[1]}" "${replica_b_port}:8000" >"${replica_b_log}" 2>&1 &
    replica_b_pid=$!
    if wait_for_http_endpoint "http://127.0.0.1:${replica_b_port}/health/ready" 60 "$replica_b_pid" "$replica_b_log"; then
      port_forward_pids+=("$replica_b_pid")
      break
    fi
    kill "$replica_b_pid" >/dev/null 2>&1 || true
    if ! python3 scripts/release/retry_policy.py should-retry "port_forward_start" "$replica_b_log"; then
      exit 1
    fi
    sleep $((2 * attempt))
  done
  if ! kill -0 "$replica_b_pid" >/dev/null 2>&1; then
    echo "Failed to establish port-forward for replica B." >&2
    exit 1
  fi

  export E2E_BASE_URL_REPLICA_A="http://127.0.0.1:${replica_a_port}"
  export E2E_BASE_URL_REPLICA_B="http://127.0.0.1:${replica_b_port}"
  export E2E_BASE_URL="$E2E_BASE_URL_REPLICA_A"
else
  local_port="${E2E_LOCAL_PORT:-$(allocate_local_port)}"
  port_forward_log="${tmp_dir}/port-forward.log"
  for attempt in 1 2 3; do
    kubectl port-forward -n "$e2e_namespace" svc/router-app "${local_port}:8000" >"${port_forward_log}" 2>&1 &
    port_forward_pid=$!
    if wait_for_http_endpoint "http://127.0.0.1:${local_port}/health/ready" 60 "$port_forward_pid" "$port_forward_log"; then
      port_forward_pids+=("$port_forward_pid")
      break
    fi
    kill "$port_forward_pid" >/dev/null 2>&1 || true
    if ! python3 scripts/release/retry_policy.py should-retry "port_forward_start" "$port_forward_log"; then
      exit 1
    fi
    sleep $((2 * attempt))
  done
  if ! kill -0 "$port_forward_pid" >/dev/null 2>&1; then
    echo "Failed to establish router service port-forward." >&2
    exit 1
  fi
  export E2E_BASE_URL="http://127.0.0.1:${local_port}"
fi

if [[ -n "$suite_activation_env" ]]; then
  export "${suite_activation_env}=1"
fi
if [[ -n "$suite_outputs_env" ]]; then
  export "${suite_outputs_env}=${tmp_dir}/terraform-outputs.json"
fi
export VALIDATION_ARTIFACTS_DIR="$artifacts_dir"

echo "Running pytest with flags: ${pytest_flags[*]}"
uv run pytest "$tests_path" "${pytest_flags[@]}" 2>&1 | tee "${artifacts_dir}/pytest.log"
