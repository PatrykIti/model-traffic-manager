[Repository README](../README.md) | [Internal docs](./README.md) | [SaaS Orchestration Reference](./SaaS-Chatbot-System-Orchiestration.md)

# Chatbot Platform Above the Router

## Purpose

This document describes how to build a separate chatbot platform on top of `Model Traffic Manager` instead of pushing the entire chatbot product into the router itself.

That separation is important.

## Architectural Rule

The router and the chatbot platform are two different products.

### Router

The router is responsible for:

- model routing
- failover across AI regions and accounts
- outbound authentication via Managed Identity
- health state handling
- rate limiting and observability for model traffic

### Chatbot Platform

The chatbot platform is responsible for:

- chatbot creation
- chatbot configuration
- prompt versioning
- drafts and publication flows
- chatbot tool management
- user conversations
- the builder frontend
- the test playground
- chatbot release management

The shortest rule is:

> the router executes, and the chatbot platform manages the product.

## Why These Concerns Should Not Be Mixed

If prompt versioning, bot editing, publication, and conversations are pushed into the router, we will again build a very broad platform instead of a specialized traffic and execution layer.

That leads to:

- blurred ownership
- harder product evolution
- higher operational complexity
- weaker testability

## Target System Split

### 1. Model Traffic Manager

Our router.

It provides:

- the inference gateway
- account and region failover
- Managed Identity authentication to downstream services
- a unified execution layer

### 2. Chatbot Control Plane

The business backend used to manage chatbots.

It provides:

- chatbot CRUD
- prompt templates
- prompt versions
- releases
- environment promotion
- test runs
- metadata and ownership

### 3. Chatbot Runtime API

The runtime layer for conversations with the chatbot.

It provides:

- final prompt assembly
- active release resolution
- variable substitution
- router invocation
- conversation and trace persistence

### 4. Chatbot Web UI

The frontend used for:

- building chatbots
- editing prompts
- viewing versions
- testing
- publishing
- basic monitoring

### 5. Shared Persistence

A separate data layer for the chatbot platform:

- Postgres
- Redis
- blob storage
- optionally a vector database

## Chatbot Creation Flow

1. The user creates a new chatbot in the UI.
2. The backend stores the chatbot as a logical entity.
3. The user creates or edits a prompt template.
4. A prompt change creates a new draft or a new version.
5. The user tests the chatbot in the playground.
6. After approval, the user publishes a release.
7. The conversation runtime uses only the active release.

## Conversation Flow

1. The user opens a chat with the chatbot.
2. The runtime loads the chatbot's active release.
3. The runtime builds the final prompt from:
   - the system prompt
   - instructions
   - model parameters
   - optional tools
   - optional RAG context
4. The runtime calls the router with the selected deployment.
5. The router selects an upstream and performs inference.
6. The runtime returns the response and stores the conversation.

## Where Prompt Versioning Belongs

Prompt versioning does not belong in the router.

It belongs to the `Chatbot Control Plane`.

The router should not know:

- which prompt version is a draft
- which prompt version is published
- how the editing UI works
- how prompt publication works

## Data Model for the Chatbot Platform

### Core Entities

#### `chatbot`

The logical product entity.

Example fields:

- `id`
- `name`
- `slug`
- `description`
- `owner_id`
- `status`
- `created_at`
- `updated_at`

#### `prompt_template`

The logical prompt definition attached to a chatbot.

Example fields:

- `id`
- `chatbot_id`
- `name`
- `current_draft_id`

#### `prompt_version`

An immutable prompt snapshot.

Example fields:

- `id`
- `prompt_template_id`
- `version_number`
- `content`
- `variables_schema`
- `created_by`
- `created_at`
- `change_note`

#### `chatbot_release`

A snapshot of the configuration that is ready to run.

It should bind together:

- a specific prompt version
- a model deployment
- generation settings
- tools
- an optional RAG policy
- the target environment

Example fields:

- `id`
- `chatbot_id`
- `release_number`
- `prompt_version_id`
- `model_deployment_id`
- `tool_policy_id`
- `environment`
- `status`
- `published_by`
- `published_at`

#### `tool_binding`

Describes the tools attached to a chatbot.

Example fields:

- `id`
- `chatbot_id`
- `tool_name`
- `tool_type`
- `configuration`
- `enabled`

#### `conversation`

A conversation session.

Example fields:

- `id`
- `chatbot_id`
- `release_id`
- `user_id`
- `started_at`
- `last_activity_at`

#### `message`

Messages inside a conversation.

Example fields:

- `id`
- `conversation_id`
- `role`
- `content`
- `attachments`
- `created_at`

#### `evaluation_run`

An optional entity for testing prompts and releases.

Example fields:

- `id`
- `chatbot_id`
- `release_id`
- `dataset_id`
- `status`
- `score`
- `created_at`

## Prompt Versioning: Expected Behavior

### Rule

We do not edit a live production prompt.

We create:

- a draft
- a new version
- a release

### Minimal Workflow

1. `draft`
   The user edits the prompt.
2. `save version`
   An immutable `prompt_version` is created.
3. `test`
   The user runs the playground or an evaluation.
4. `publish`
   A `chatbot_release` is created.
5. `promote`
   The release can move to `dev`, `stage`, or `prod`.
6. `rollback`
   The system can switch back to an older release.

### Why a Release Is a Separate Entity

Because production does not receive only a prompt.

Production receives a complete set of runtime inputs:

- the prompt version
- the model deployment
- temperature and generation parameters
- tools
- an optional safety policy

Together, that set forms a release.

## Builder Frontend: Main Screens

At the start, the frontend should include:

- the chatbot list
- the chatbot configuration screen
- the prompt editor
- version history
- version diff
- the test playground
- the release publication screen
- a basic conversation and usage view

## How the Platform Should Use the Router

The chatbot platform should not call providers directly.

It should call only the router.

For example:

- `POST /v1/chat/completions/{deployment_id}`
- `POST /v1/embeddings/{deployment_id}`

Additional observability headers may also be added:

- `X-Chatbot-Id`
- `X-Release-Id`
- `X-Environment`
- `X-Tenant-Id`

Those headers should exist only for tracing and telemetry, not for prompt-versioning logic.

## What the Router Should Know About the Chatbot Platform

Very little.

The router may know:

- `chatbot_id`
- `release_id`
- `tenant_id`

for the purposes of:

- logging
- metrics
- cost tracking
- debugging

The router should not know:

- what a prompt draft looks like
- how publication works
- what the builder UI looks like

## Suggested Stack for the Chatbot Platform

### Backend

- Python `3.12`
- FastAPI
- Pydantic
- SQLAlchemy or SQLModel, but only once the control plane is introduced

### Database

- Postgres

### Cache and Sessions

- Redis

### Files and Assets

- blob storage

### Frontend

- Next.js

### Inference

- through `Model Traffic Manager`

### Optional Components Later

- `pgvector` or a separate vector database
- an evaluation worker
- an async job runner

## Repository or Service Split

There are two sensible options.

### Option A: One Repository, Two Bounded Contexts

- `router`
- `chatbot-platform`

plus shared contracts.

This is acceptable at the start.

### Option B: Separate Repositories

- repository 1: `model-traffic-manager`
- repository 2: `chatbot-platform`

This becomes better once the products start evolving independently.

At the start, I would recommend:

- a separate repository for the router
- a separate repository for the chatbot platform

because the responsibilities are different.

## Recommended Build Order

The best order is:

1. Build the router.
2. Build a simple chatbot runtime.
3. Add the chatbot control plane.
4. Add prompt versioning.
5. Add releases and cross-environment promotion.
6. Add tools, RAG, and evaluations.

## Most Important Product Rule

> We build the chatbot platform on top of the router, not inside the router.

That keeps:

- the router simple
- the architecture clean
- the responsibility split explicit
- both products easier to evolve
