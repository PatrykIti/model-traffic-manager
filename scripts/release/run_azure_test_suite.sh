#!/usr/bin/env bash
set -Eeuo pipefail

SUITE="${1:-}"
ENVIRONMENT="${2:-dev1}"

if [[ -z "$SUITE" ]]; then
  echo "Usage: bash scripts/release/run_azure_test_suite.sh <integration-azure|e2e-aks|e2e-aks-live-model|e2e-aks-live-embeddings> [environment]" >&2
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

for cmd in az terraform uv python3; do
  require_cmd "$cmd"
done

subscription_id="$(az account show --query id -o tsv)"
tenant_id="$(az account show --query tenantId -o tsv)"
account_name="$(az account show --query name -o tsv)"
run_id="local-$(date -u +%Y%m%d%H%M%S)-$RANDOM"
tmp_dir="$(mktemp -d "${TMPDIR:-/tmp}/mtm-${SUITE}-XXXXXX")"

case "$SUITE" in
  integration-azure)
    scope_dir="infra/integration-azure"
    tests_path="tests/integration_azure"
    tf_args=(
      "-var-file=../_shared/env/${ENVIRONMENT}.tfvars"
      "-var=subscription_id=${subscription_id}"
      "-var=run_id=${run_id}"
    )
    ;;
  e2e-aks)
    for cmd in docker gh kubectl; do
      require_cmd "$cmd"
    done
    scope_dir="infra/e2e-aks"
    tests_path="tests/e2e_aks"
    tf_args=(
      "-var-file=../_shared/env/${ENVIRONMENT}.tfvars"
      "-var-file=env/${ENVIRONMENT}.tfvars"
      "-var=subscription_id=${subscription_id}"
      "-var=run_id=${run_id}"
    )
    if [[ -n "${KUBERNETES_VERSION:-}" ]]; then
      tf_args+=("-var=kubernetes_version=${KUBERNETES_VERSION}")
    fi
    ;;
  e2e-aks-live-model)
    for cmd in docker gh kubectl; do
      require_cmd "$cmd"
    done
    scope_dir="infra/e2e-aks-live-model"
    tests_path="tests/e2e_aks_live_model"
    tf_args=(
      "-var-file=../_shared/env/${ENVIRONMENT}.tfvars"
      "-var-file=env/${ENVIRONMENT}.tfvars"
      "-var=subscription_id=${subscription_id}"
      "-var=run_id=${run_id}"
    )
    if [[ -n "${KUBERNETES_VERSION:-}" ]]; then
      tf_args+=("-var=kubernetes_version=${KUBERNETES_VERSION}")
    fi
    ;;
  e2e-aks-live-embeddings)
    for cmd in docker gh kubectl; do
      require_cmd "$cmd"
    done
    scope_dir="infra/e2e-aks-live-embeddings"
    tests_path="tests/e2e_aks_live_embeddings"
    tf_args=(
      "-var-file=../_shared/env/${ENVIRONMENT}.tfvars"
      "-var-file=env/${ENVIRONMENT}.tfvars"
      "-var=subscription_id=${subscription_id}"
      "-var=run_id=${run_id}"
    )
    if [[ -n "${KUBERNETES_VERSION:-}" ]]; then
      tf_args+=("-var=kubernetes_version=${KUBERNETES_VERSION}")
    fi
    ;;
  *)
    echo "Unsupported suite: $SUITE" >&2
    exit 1
    ;;
esac

apply_started="0"
port_forward_pid=""
resource_group=""
aks_cluster_name=""
e2e_namespace="${E2E_NAMESPACE:-e2e-router}"
e2e_image="${E2E_IMAGE:-}"
federated_credential_created="0"
e2e_image_pull_secret_name="${E2E_IMAGE_PULL_SECRET_NAME:-ghcr-pull}"

print_e2e_diagnostics() {
  if [[ "$SUITE" != e2e-aks && "$SUITE" != e2e-aks-live-model && "$SUITE" != e2e-aks-live-embeddings || -z "$aks_cluster_name" ]]; then
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

  if [[ -n "$port_forward_pid" ]]; then
    echo "Cleaning up: stopping port-forward process ${port_forward_pid}"
    kill "$port_forward_pid" >/dev/null 2>&1 || true
  fi

  if [[ ( "$SUITE" == "e2e-aks" || "$SUITE" == "e2e-aks-live-model" || "$SUITE" == "e2e-aks-live-embeddings" ) && "$federated_credential_created" == "1" && -n "$resource_group" && -n "${UAI_NAME:-}" ]]; then
    echo "Cleaning up: deleting federated credential router-e2e-${run_id}"
    az identity federated-credential delete \
      --resource-group "$resource_group" \
      --identity-name "$UAI_NAME" \
      --name "router-e2e-${run_id}" \
      --yes >/dev/null 2>&1 || true
  fi

  if [[ "$apply_started" == "1" ]]; then
    echo "Cleaning up: running terraform destroy for ${SUITE}"
    if ! terraform -chdir="$scope_dir" destroy -auto-approve -input=false "${tf_args[@]}"; then
      destroy_exit_code=$?
      echo "Cleanup warning: terraform destroy failed for ${SUITE}" >&2
    fi
  fi

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

if [[ ( "$SUITE" == "e2e-aks" || "$SUITE" == "e2e-aks-live-model" || "$SUITE" == "e2e-aks-live-embeddings" ) && -z "$e2e_image" ]]; then
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

  echo "$ghcr_token" | docker login ghcr.io -u "$ghcr_username" --password-stdin
  docker buildx build \
    --platform "$e2e_image_platform" \
    -f docker/Dockerfile \
    -t "$e2e_image" \
    --push \
    .
fi

terraform -chdir="$scope_dir" init -backend=false
apply_started="1"
terraform -chdir="$scope_dir" apply -auto-approve -input=false "${tf_args[@]}"
terraform -chdir="$scope_dir" output -json > "${tmp_dir}/terraform-outputs.json"

if [[ "$SUITE" == "integration-azure" ]]; then
  export RUN_INTEGRATION_AZURE="1"
  export INTEGRATION_AZURE_SCOPE="${INTEGRATION_AZURE_SCOPE:-https://management.azure.com/.default}"

  uv run pytest "$tests_path" -ra
  exit 0
fi

resource_group="$(terraform -chdir="$scope_dir" output -raw resource_group_name)"
aks_cluster_name="$(terraform -chdir="$scope_dir" output -raw aks_cluster_name)"
aks_oidc_issuer_url="$(terraform -chdir="$scope_dir" output -raw aks_oidc_issuer_url)"
UAI_NAME="$(terraform -chdir="$scope_dir" output -raw user_assigned_identity_name)"
uai_client_id="$(terraform -chdir="$scope_dir" output -raw user_assigned_identity_client_id)"

az aks get-credentials --resource-group "$resource_group" --name "$aks_cluster_name" --overwrite-existing

az identity federated-credential create \
  --resource-group "$resource_group" \
  --identity-name "$UAI_NAME" \
  --name "router-e2e-${run_id}" \
  --issuer "$aks_oidc_issuer_url" \
  --subject "system:serviceaccount:${e2e_namespace}:router-app" \
  --audiences "api://AzureADTokenExchange"
federated_credential_created="1"

kubectl create namespace "$e2e_namespace" --dry-run=client -o yaml | kubectl apply -f -

if [[ "$SUITE" == "e2e-aks-live-model" ]]; then
  python3 scripts/release/render_live_model_router_config.py "${tmp_dir}/terraform-outputs.json" > "${tmp_dir}/router-live-model.yaml"
  kubectl create configmap router-config \
    --from-file=router.yaml="${tmp_dir}/router-live-model.yaml" \
    --namespace "$e2e_namespace" \
    --dry-run=client -o yaml | kubectl apply -f -
elif [[ "$SUITE" == "e2e-aks-live-embeddings" ]]; then
  python3 scripts/release/render_live_embeddings_router_config.py "${tmp_dir}/terraform-outputs.json" > "${tmp_dir}/router-live-embeddings.yaml"
  kubectl create configmap router-config \
    --from-file=router.yaml="${tmp_dir}/router-live-embeddings.yaml" \
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

if [[ "$e2e_image" == ghcr.io/* ]]; then
  ghcr_username="${GHCR_USERNAME:-${GHCR_OWNER:-$(gh api user -q .login 2>/dev/null || true)}}"
  ghcr_token="${GHCR_TOKEN:-$(gh auth token 2>/dev/null || true)}"

  if [[ -z "$ghcr_username" || -z "$ghcr_token" ]]; then
    echo "Private GHCR image pull requires GHCR_TOKEN and GHCR_USERNAME (or an authenticated gh cli session)." >&2
    exit 1
  fi

  echo "Configuring image pull secret ${e2e_image_pull_secret_name} for ${e2e_namespace}"
  kubectl create secret docker-registry "$e2e_image_pull_secret_name" \
    --docker-server=ghcr.io \
    --docker-username="$ghcr_username" \
    --docker-password="$ghcr_token" \
    --namespace "$e2e_namespace" \
    --dry-run=client -o yaml | kubectl apply -f -
fi

manifest_root="infra/e2e-aks"
if [[ "$SUITE" == "e2e-aks-live-model" ]]; then
  manifest_root="infra/e2e-aks-live-model"
elif [[ "$SUITE" == "e2e-aks-live-embeddings" ]]; then
  manifest_root="infra/e2e-aks-live-embeddings"
fi

python3 scripts/release/render_template.py "${manifest_root}/k8s/router-serviceaccount.yaml.tmpl" | kubectl apply -f -
if [[ "$e2e_image" == ghcr.io/* ]]; then
  kubectl patch serviceaccount/router-app \
    -n "$e2e_namespace" \
    --type merge \
    -p "{\"imagePullSecrets\":[{\"name\":\"${e2e_image_pull_secret_name}\"}]}"
fi
python3 scripts/release/render_template.py "${manifest_root}/k8s/router-deployment.yaml.tmpl" | kubectl apply -f -
kubectl apply -n "$e2e_namespace" -f "${manifest_root}/k8s/router-service.yaml"

kubectl rollout status deployment/router-app -n "$e2e_namespace" --timeout=5m

kubectl exec -n "$e2e_namespace" deployment/router-app -- sh -lc \
  'test -n "$AZURE_FEDERATED_TOKEN_FILE" && test -f "$AZURE_FEDERATED_TOKEN_FILE"'

kubectl exec -n "$e2e_namespace" deployment/router-app -- sh -lc \
  '/app/.venv/bin/python -c "from azure.identity import DefaultAzureCredential; token = DefaultAzureCredential().get_token(\"https://management.azure.com/.default\"); assert token.token; print(len(token.token))"'

kubectl port-forward -n "$e2e_namespace" svc/router-app 18080:8000 >"${tmp_dir}/port-forward.log" 2>&1 &
port_forward_pid="$!"
sleep 10

export RUN_E2E_AKS="1"
export E2E_BASE_URL="http://127.0.0.1:18080"

if [[ "$SUITE" == "e2e-aks-live-model" ]]; then
  export RUN_E2E_AKS_LIVE_MODEL="1"
  export E2E_LIVE_MODEL_OUTPUTS_JSON="${tmp_dir}/terraform-outputs.json"
elif [[ "$SUITE" == "e2e-aks-live-embeddings" ]]; then
  export RUN_E2E_AKS_LIVE_EMBEDDINGS="1"
  export E2E_LIVE_EMBEDDINGS_OUTPUTS_JSON="${tmp_dir}/terraform-outputs.json"
fi

uv run pytest "$tests_path" -ra
