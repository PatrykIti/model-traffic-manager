[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-004-04-01: Dockerfile, Entrypoint, and Image Policy
# FileName: TASK-004-04-01-dockerfile-entrypoint-and-image-policy.md

**Priority:** High
**Category:** Runtime Bootstrap
**Estimated Effort:** Medium
**Dependencies:** TASK-004-04
**Status:** **In Progress** (2026-03-13)

---

## Overview

Define the first production-like container contract for the repository bootstrap.

This work item owns:
- `docker/Dockerfile`
- `docker/entrypoint.sh`

---

## Target Files

```text
docker/Dockerfile
docker/entrypoint.sh
```

---

## Detailed Work Items

1. Use a Python `3.12` base image pinned by digest.
2. Install project dependencies via `uv` or an approved build strategy that preserves reproducibility.
3. Run the app through a single clear entrypoint path.
4. Keep the first image simple; do not over-engineer multi-stage or distroless flow unless needed by the bootstrap.

---

## Pseudocode

```text
docker_build():
    copy lock and project metadata
    install dependencies
    copy app source and configs
    set entrypoint
```

---

## Testing Requirements

- image builds successfully
- container start command matches local run expectations
- base image selection respects the no-floating-tag policy

Current note:
- Dockerfile and entrypoint were implemented and the base image was pinned by digest.
- Local `make docker-build` could not be fully verified because the Docker daemon is not running on the current machine.

---

## Documentation Updates Required

- `docs/operations/README.md`
- `docs/getting-started/README.md`
- `_docs/_TASKS/TASK-004-04-01-dockerfile-entrypoint-and-image-policy.md`
