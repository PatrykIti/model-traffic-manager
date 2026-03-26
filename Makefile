SHELL := /bin/bash
PYTHON_VERSION := $(shell cat .python-version)
UV_CACHE_DIR ?= /tmp/uv-cache
UV := UV_CACHE_DIR=$(UV_CACHE_DIR) uv
ENVIRONMENT ?= dev1
PYTEST_FLAGS ?= -vv -rA
SELECTION ?= all
RUN_MODE ?= continue-on-error
LOCAL_LOG_ROOT ?= /tmp/mtm-local-logs

.PHONY: bootstrap lock lint format typecheck validate-shell test check validate-workflows validate-terraform release-check list-validation-suites validation-suite-local validation-matrix-local validate-all-local validate-release-local integration-azure-local integration-azure-chat-local integration-azure-embeddings-local e2e-aks-local e2e-aks-live-model-local e2e-aks-live-embeddings-local e2e-aks-live-load-balancing-local e2e-aks-live-shared-services-local e2e-aks-live-observability-local e2e-aks-redis-local run docker-build smoke clean

bootstrap:
	$(UV) sync --frozen --python "$(PYTHON_VERSION)"

lock:
	$(UV) lock --python "$(PYTHON_VERSION)"

lint:
	$(UV) run ruff check .

format:
	$(UV) run ruff format .

typecheck:
	$(UV) run mypy app

validate-shell:
	bash -n docker/entrypoint.sh
	bash -n scripts/release/run_azure_test_suite.sh

test:
	mkdir -p "$(LOCAL_LOG_ROOT)"
	set -o pipefail; $(UV) run pytest $(PYTEST_FLAGS) --cov=app --cov-report=term-missing --cov-fail-under=85 2>&1 | tee "$(LOCAL_LOG_ROOT)/pytest.log"

check: lint typecheck validate-shell test

validate-workflows:
	$(UV) run python scripts/release/validate_github_workflows.py

list-validation-suites:
	python3 scripts/release/validation_suite_registry.py list

validate-terraform:
	@while read -r scope_dir; do \
		terraform -chdir="$$scope_dir" init -backend=false; \
		terraform -chdir="$$scope_dir" validate; \
	done < <(python3 scripts/release/validation_suite_registry.py list-scope-dirs)

release-check: check validate-workflows validate-terraform

validation-suite-local:
	mkdir -p "$(LOCAL_LOG_ROOT)"
	set -o pipefail; bash scripts/release/run_azure_test_suite.sh "$(SUITE)" "$(ENVIRONMENT)" 2>&1 | tee "$(LOCAL_LOG_ROOT)/validation-suite-$(SUITE)-$(ENVIRONMENT).log"

validation-matrix-local:
	mkdir -p "$(LOCAL_LOG_ROOT)"
	set -o pipefail; python3 scripts/release/run_validation_matrix.py --environment "$(ENVIRONMENT)" --selection "$(SELECTION)" --mode "$(RUN_MODE)" 2>&1 | tee "$(LOCAL_LOG_ROOT)/validation-matrix-$(SELECTION)-$(ENVIRONMENT).log"

validate-all-local:
	$(MAKE) validation-matrix-local ENVIRONMENT="$(ENVIRONMENT)" SELECTION=all RUN_MODE=continue-on-error

validate-release-local:
	$(MAKE) validation-matrix-local ENVIRONMENT="$(ENVIRONMENT)" SELECTION=release RUN_MODE=continue-on-error

integration-azure-local:
	$(MAKE) validation-suite-local SUITE=integration-azure ENVIRONMENT="$(ENVIRONMENT)"

integration-azure-chat-local:
	$(MAKE) validation-suite-local SUITE=integration-azure-chat ENVIRONMENT="$(ENVIRONMENT)"

integration-azure-embeddings-local:
	$(MAKE) validation-suite-local SUITE=integration-azure-embeddings ENVIRONMENT="$(ENVIRONMENT)"

e2e-aks-local:
	$(MAKE) validation-suite-local SUITE=e2e-aks ENVIRONMENT="$(ENVIRONMENT)"

e2e-aks-live-model-local:
	$(MAKE) validation-suite-local SUITE=e2e-aks-live-model ENVIRONMENT="$(ENVIRONMENT)"

e2e-aks-live-embeddings-local:
	$(MAKE) validation-suite-local SUITE=e2e-aks-live-embeddings ENVIRONMENT="$(ENVIRONMENT)"

e2e-aks-live-load-balancing-local:
	$(MAKE) validation-suite-local SUITE=e2e-aks-live-load-balancing ENVIRONMENT="$(ENVIRONMENT)"

e2e-aks-live-shared-services-local:
	$(MAKE) validation-suite-local SUITE=e2e-aks-live-shared-services ENVIRONMENT="$(ENVIRONMENT)"

e2e-aks-live-observability-local:
	$(MAKE) validation-suite-local SUITE=e2e-aks-live-observability ENVIRONMENT="$(ENVIRONMENT)"

e2e-aks-redis-local:
	$(MAKE) validation-suite-local SUITE=e2e-aks-redis ENVIRONMENT="$(ENVIRONMENT)"

run:
	$(UV) run uvicorn app.entrypoints.api.main:app --host 0.0.0.0 --port 8000

docker-build:
	docker build -f docker/Dockerfile -t model-traffic-manager:dev .

smoke:
	mkdir -p "$(LOCAL_LOG_ROOT)"
	set -o pipefail; $(UV) run pytest $(PYTEST_FLAGS) tests/unit/entrypoints/api/test_health.py tests/integration/api/test_startup.py 2>&1 | tee "$(LOCAL_LOG_ROOT)/smoke.log"

clean:
	rm -rf .mypy_cache .pytest_cache .ruff_cache htmlcov coverage.xml
