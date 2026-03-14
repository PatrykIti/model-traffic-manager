SHELL := /bin/bash
PYTHON_VERSION := $(shell cat .python-version)
UV_CACHE_DIR ?= /tmp/uv-cache
UV := UV_CACHE_DIR=$(UV_CACHE_DIR) uv

.PHONY: bootstrap lock lint format typecheck test check validate-workflows validate-terraform release-check run docker-build smoke clean

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

test:
	$(UV) run pytest --cov=app --cov-report=term-missing --cov-fail-under=85

check: lint typecheck test

validate-workflows:
	$(UV) run python scripts/release/validate_github_workflows.py

validate-terraform:
	terraform -chdir=infra/integration-azure init -backend=false
	terraform -chdir=infra/integration-azure validate
	terraform -chdir=infra/e2e-aks init -backend=false
	terraform -chdir=infra/e2e-aks validate

release-check: check validate-workflows validate-terraform

run:
	$(UV) run uvicorn app.entrypoints.api.main:app --host 0.0.0.0 --port 8000

docker-build:
	docker build -f docker/Dockerfile -t model-traffic-manager:dev .

smoke:
	$(UV) run pytest tests/unit/entrypoints/api/test_health.py tests/integration/api/test_startup.py

clean:
	rm -rf .mypy_cache .pytest_cache .ruff_cache htmlcov coverage.xml
