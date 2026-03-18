SHELL := /bin/bash
PYTHON_VERSION := $(shell cat .python-version)
UV_CACHE_DIR ?= /tmp/uv-cache
UV := UV_CACHE_DIR=$(UV_CACHE_DIR) uv
ENVIRONMENT ?= dev1
PYTEST_FLAGS ?= -vv -rA

.PHONY: bootstrap lock lint format typecheck validate-shell test check validate-workflows validate-terraform release-check integration-azure-local integration-azure-chat-local integration-azure-embeddings-local e2e-aks-local e2e-aks-live-model-local e2e-aks-live-embeddings-local e2e-aks-live-load-balancing-local e2e-aks-live-shared-services-local run docker-build smoke clean

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
	$(UV) run pytest $(PYTEST_FLAGS) --cov=app --cov-report=term-missing --cov-fail-under=85

check: lint typecheck validate-shell test

validate-workflows:
	$(UV) run python scripts/release/validate_github_workflows.py

validate-terraform:
	terraform -chdir=infra/integration-azure init -backend=false
	terraform -chdir=infra/integration-azure validate
	terraform -chdir=infra/integration-azure-chat init -backend=false
	terraform -chdir=infra/integration-azure-chat validate
	terraform -chdir=infra/integration-azure-embeddings init -backend=false
	terraform -chdir=infra/integration-azure-embeddings validate
	terraform -chdir=infra/e2e-aks init -backend=false
	terraform -chdir=infra/e2e-aks validate
	terraform -chdir=infra/e2e-aks-live-model init -backend=false
	terraform -chdir=infra/e2e-aks-live-model validate
	terraform -chdir=infra/e2e-aks-live-embeddings init -backend=false
	terraform -chdir=infra/e2e-aks-live-embeddings validate
	terraform -chdir=infra/e2e-aks-live-load-balancing init -backend=false
	terraform -chdir=infra/e2e-aks-live-load-balancing validate
	terraform -chdir=infra/e2e-aks-live-shared-services init -backend=false
	terraform -chdir=infra/e2e-aks-live-shared-services validate

release-check: check validate-workflows validate-terraform

integration-azure-local:
	bash scripts/release/run_azure_test_suite.sh integration-azure "$(ENVIRONMENT)"

integration-azure-chat-local:
	bash scripts/release/run_azure_test_suite.sh integration-azure-chat "$(ENVIRONMENT)"

integration-azure-embeddings-local:
	bash scripts/release/run_azure_test_suite.sh integration-azure-embeddings "$(ENVIRONMENT)"

e2e-aks-local:
	bash scripts/release/run_azure_test_suite.sh e2e-aks "$(ENVIRONMENT)"

e2e-aks-live-model-local:
	bash scripts/release/run_azure_test_suite.sh e2e-aks-live-model "$(ENVIRONMENT)"

e2e-aks-live-embeddings-local:
	bash scripts/release/run_azure_test_suite.sh e2e-aks-live-embeddings "$(ENVIRONMENT)"

e2e-aks-live-load-balancing-local:
	bash scripts/release/run_azure_test_suite.sh e2e-aks-live-load-balancing "$(ENVIRONMENT)"

e2e-aks-live-shared-services-local:
	bash scripts/release/run_azure_test_suite.sh e2e-aks-live-shared-services "$(ENVIRONMENT)"

run:
	$(UV) run uvicorn app.entrypoints.api.main:app --host 0.0.0.0 --port 8000

docker-build:
	docker build -f docker/Dockerfile -t model-traffic-manager:dev .

smoke:
	$(UV) run pytest $(PYTEST_FLAGS) tests/unit/entrypoints/api/test_health.py tests/integration/api/test_startup.py

clean:
	rm -rf .mypy_cache .pytest_cache .ruff_cache htmlcov coverage.xml
