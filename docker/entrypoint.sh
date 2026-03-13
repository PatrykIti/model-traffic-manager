#!/usr/bin/env sh
set -eu

exec uvicorn app.entrypoints.api.main:app --host 0.0.0.0 --port 8000
