[Repository README](../README.md) | [Official docs](../docs/README.md) | [AGENTS](../AGENTS.md)

# Internal Documentation

This directory is the internal delivery space for the repository.

## Purpose

`_docs/` stores the documentation needed to plan, track, and evolve the repository with AI-assisted workflows:

- MVP planning and implementation guidance
- task decomposition
- changelog history
- internal workflow agreements

This is intentionally separate from `docs/`, which is reserved for the official application documentation.

## Sections

- [_MVP/README.md](./_MVP/README.md) for product intent, architecture, stack, configuration, routing, and testing guidance
- [_INFRA/README.md](./_INFRA/README.md) for internal infrastructure scope and Terraform guidance
- [_TASKS/README.md](./_TASKS/README.md) for the task board and task authoring rules
- [_CHANGELOG/README.md](./_CHANGELOG/README.md) for changelog workflow and entry index

## Informational References

Higher-level chatbot platform and SaaS orchestration reference documents were intentionally moved out of this repository to keep the internal documentation scoped to the router itself.

## Navigation rules

- Every documentation directory must have a `README.md`.
- Every documentation Markdown file should expose navigation controls near the top.
- When a new documentation area is added, update this index and the `README.md` above it.
