[Repository README](./README.md) | [Official docs](./docs/README.md) | [Internal docs](./_docs/README.md)

# Contributing

## Working model

This repository is developed with a strict split between official documentation and internal delivery documentation:

- `docs/` is for official application documentation.
- `_docs/` is for internal planning, task tracking, changelog history, and implementation notes.

All Markdown content must be written in English.

## Before you start

1. Read [AGENTS.md](./AGENTS.md).
2. Check the current task board in [_docs/_TASKS/README.md](./_docs/_TASKS/README.md).
3. Create or update the task and subtask files for the work you are about to do.

## Required workflow for every change

1. Create a main task in `_docs/_TASKS/`.
2. Create at least one technical subtask when the change has implementation details, structure changes, or pseudocode worth tracking.
3. Update the relevant documentation in `docs/` and/or `_docs/`.
4. Add or update the changelog entry in `_docs/_CHANGELOG/`.
5. Update the task board and changelog index.
6. Run pre-commit before committing.

## Install and use pre-commit

Recommended installation options:

- `uv tool install pre-commit`
- or `python3 -m pip install pre-commit`

Then enable and run it:

```text
pre-commit install
pre-commit run --all-files
```

Canonical local commands:

```text
make bootstrap
make check
make run
```

## Branching and pull requests

- Use descriptive branches such as `feature/...`, `fix/...`, or `docs/...`.
- Keep pull requests focused on one coherent task group.
- Link the relevant task and subtask IDs in the pull request.
- Use the repository pull request template.
- Keep local validation and CI aligned by using the same `make` targets.

## Documentation expectations

- Every documentation directory must contain a `README.md`.
- Every documentation Markdown file except the root repository `README.md` must include navigation links near the top.
- `docs/` should explain the application from the user/operator/contributor perspective.
- `_docs/` should explain internal planning, task decomposition, and delivery workflow.

## Validation expectations

Before opening or updating a pull request:

- run `pre-commit run --all-files`
- resolve every failing hook
- update task status and changelog references
- ensure all changed Markdown files are in English
