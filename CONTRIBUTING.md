[Repository README](./README.md) | [Official docs](./docs/README.md) | [Support](./SUPPORT.md) | [Code of Conduct](./CODE_OF_CONDUCT.md)

# Contributing

Thanks for your interest in `model-traffic-manager`.

This repository is open to:

- bug fixes
- tests and validation improvements
- documentation improvements
- example configurations
- focused feature work that fits the product scope

## Product scope first

Before contributing, make sure the change fits the repository boundary:

- this project is an Azure- and AKS-focused AI traffic router
- it is not a generic AI gateway, SaaS control plane, or prompt-management platform
- small, explicit, testable changes are preferred over large framework-heavy refactors

If you want to propose a bigger feature or product-direction change, open an issue first so the design can be discussed before implementation work starts.

## Local setup

Canonical local commands:

```text
make bootstrap
make check
make run
```

Recommended pre-commit setup:

```text
uv tool install pre-commit
pre-commit install
pre-commit run --all-files
```

## Pull request expectations

- use descriptive branches such as `feature/...`, `fix/...`, or `docs/...`
- keep pull requests focused on one coherent change set
- add or update tests when behavior changes
- update documentation when user-visible behavior, config, or operations guidance changes
- keep local validation and CI aligned by using the same `make` targets
- use the repository pull request template
- fill in the `Release Impact` and `Release Notes` sections when the change should appear in public release notes

Before opening or updating a pull request:

- run `pre-commit run --all-files`
- resolve every failing hook
- ensure all changed Markdown files remain in English
- avoid mixing unrelated refactors into the same PR

## Release workflow

- semantic release notes are still sourced from merged pull-request bodies
- `semantic-release` now runs automatically on pushes to the default branch and can still be started manually in `dry_run` mode
- release tags in the form `v*` now publish a versioned container image to GHCR through the dedicated `release-image` workflow
- the expensive Azure-backed `release-validation` workflow remains manual by design so it can stay a deliberate release gate instead of a post-release cost surprise

## Public contributor workflow versus maintainer workflow

This repository has an internal maintainer workflow in [`AGENTS.md`](./AGENTS.md) and [`_docs/_TASKS`](./_docs/_TASKS/README.md).

For external contributors:

- you do not need to create or update internal task files unless a maintainer asks for it
- you do not need to add `_docs/_CHANGELOG` entries yourself unless you are working as a maintainer
- maintainers may reconcile internal task and changelog bookkeeping during review

For maintainers and repeat contributors:

- follow the full repository process in [`AGENTS.md`](./AGENTS.md)
- keep `_docs/_TASKS` and `_docs/_CHANGELOG` synchronized
- update official docs in `docs/` whenever behavior changes

## Documentation expectations

- `docs/` is for official product and operator documentation
- `_docs/` is for internal planning and delivery workflow
- every documentation directory must contain a `README.md`
- every Markdown document other than the root `README.md` must include navigation links near the top
- all Markdown content must be written in English

## Security and conduct

- for vulnerabilities or anything sensitive, follow [`SECURITY.md`](./SECURITY.md) instead of opening a public issue
- participation in project spaces is governed by [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md)
