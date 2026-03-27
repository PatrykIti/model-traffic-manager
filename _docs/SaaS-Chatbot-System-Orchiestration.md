[Repository README](../README.md) | [Internal docs](./README.md)

# SaaS Chatbot System Orchestration Architecture (Azure + AKS)

Author: Patryk Ciechański
Purpose: Architecture specification for multi-tenant chatbot infrastructure, SaaS control plane, and tenant orchestration using Azure and AKS.

This document defines:

- SaaS tenant model
- Infrastructure layers
- Networking topology
- AKS cluster strategy
- Tenant provisioning workflow
- Admin dashboard control plane
- Model Traffic Manager integration
- Kubernetes isolation strategy
- Tiering strategy (shared / dedicated)

---

# 1. Terminology

## SaaS Tenant

A **tenant** is a company using the chatbot platform.

This is **NOT** the Azure Entra Tenant.

In this architecture:

tenant = customer company using the SaaS

Example tenants:

| tenant_slug | company |
|-------------|--------|
| acme | ACME Corp |
| pizzabot | PizzaBot Ltd |
| bigbank | BigBank SA |

---

# 2. Tenant Identifier Model

Each tenant has two identifiers.

## tenant_id

Internal immutable identifier.

tenant_id = UUID

Example:

8b3f6c5a-8c12-4d4a-91a0-88f9c24e8b21

Used for:

- database relations
- audit logs
- billing
- internal APIs

---

## tenant_slug

Human readable identifier.

tenant_slug = acme

Used for:

- Kubernetes namespaces
- domains
- resource naming

Example:

tenant-acme

---

# 3. Tenant Database Model

Minimal table structure.

tenants
-------

tenant_id (uuid)
tenant_slug
company_name
customer_tier
placement_type
cluster_id
namespace
region
status
created_at

Example:

tenant_id: 8b3f6c5a...
tenant_slug: acme
customer_tier: starter
placement_type: shared
cluster_id: aks-shared-prod
namespace: tenant-acme
region: westeurope
status: active

---

# 4. Tenant Placement Strategy

Tenants can run in three modes.

## Shared

Multiple tenants share one cluster.

Isolation:

- namespace
- RBAC
- resource quotas
- network policies

Example:

cluster: aks-shared-prod

namespaces:

tenant-acme
tenant-pizzabot
tenant-startupai

---

## Dedicated Node Pool

Tenant runs on a dedicated node pool.

Still same cluster.

Isolation:

- node pool
- node taints
- node selectors

Example:

cluster: aks-shared-prod
node_pool: tenant-acme-pool

---

## Dedicated Cluster

Enterprise customers receive a full AKS cluster.

Example:

cluster: aks-bigbank-prod
network: spoke-bigbank

---

# 5. Infrastructure Layers

The infrastructure is separated into two layers.

## Layer 1 — Platform Infrastructure

Provisioned via Terraform.

Includes:

- hub network
- spoke networks
- baseline AKS clusters
- container registry
- key vault
- monitoring
- DNS
- ingress
- firewall

Terraform is NOT used for tenant onboarding.

---

## Layer 2 — Tenant Runtime Control Plane

Managed by the Admin Dashboard service.

Responsibilities:

- onboarding tenants
- upgrading customer tiers
- provisioning namespaces
- deploying tenant workloads
- managing secrets
- managing quotas
- managing ingress
- routing configuration

This acts as a SaaS Control Plane.

---

# 6. Admin Control Plane Architecture

Admin system runs in a separate AKS cluster.

Cluster:

aks-admin-control

Responsibilities:

- internal admin dashboard
- provisioning worker
- infrastructure orchestrator
- tenant database
- audit logs
- job queue

---

# 7. Networking Architecture

Hub-Spoke architecture.

                +-------------------+
                |        HUB        |
                |-------------------|
                | Firewall          |
                | Private DNS       |
                | Shared services   |
                +---------+---------+
                          |
        -----------------------------------------
        |                     |                 |
+---------------+   +----------------+   +----------------+
| Admin Spoke   |   | Shared AKS     |   | Enterprise     |
|               |   | Spoke          |   | Tenant Spokes  |
| aks-admin     |   | aks-shared     |   | aks-enterprise |
+---------------+   +----------------+   +----------------+

---

# 8. Cluster Strategy

Clusters are separated by function.

## Admin Cluster

aks-admin-control

Contains:

- dashboard
- orchestrator
- provisioning workers

This cluster does NOT run tenant workloads.

---

## Shared Runtime Cluster

aks-chatbot-shared

Hosts most tenants.

Isolation via namespaces.

---

## Enterprise Clusters

Provisioned per large customer.

Example:

aks-bigbank-prod
aks-enterprise-voiceai

---

# 9. Kubernetes Tenant Isolation

Each tenant gets its own namespace.

Example:

tenant-acme
tenant-pizzabot
tenant-aiagency

Inside namespace:

deployments
services
configmaps
secrets
ingress

Isolation mechanisms:

ResourceQuota
LimitRange
RBAC
NetworkPolicy

---

# 10. Example Tenant Deployment

Namespace:

tenant-acme

Resources:

deployment:
    chatbot-runtime

service:
    chatbot-api

ingress:
    acme.chat.yourplatform.ai

secret:
    tenant-acme-secrets

configmap:
    tenant-acme-config

---

# 11. Tenant Provisioning Workflow

Tenant onboarding flow.

1. Admin Dashboard creates tenant

2. Database stores tenant record

3. Placement Engine chooses cluster

4. Provision Worker starts job

5. Kubernetes API creates namespace

6. Helm deployment installs chatbot stack

7. Ingress configured

8. Secrets created

---

# 12. Admin API Example

POST /tenants
POST /tenants/{tenant_id}/upgrade-tier
POST /tenants/{tenant_id}/suspend
DELETE /tenants/{tenant_id}

Worker actions:

create namespace
deploy helm chart
configure ingress
set quotas
configure secrets

---

# 13. Router Boundary

There are two different routing concerns in the full platform.

## 13.1 SaaS Control-Plane Router

The orchestrator/admin service may expose its own routing or policy layer for:

- tenant onboarding flows
- customer-tier policy
- placement decisions
- quota and entitlement management
- admin APIs

This is part of the SaaS control plane.

## 13.2 Chatbot Runtime Model Traffic Manager

The `model-traffic-manager` repository in this workspace is a different service.

It is:

- the internal LLM traffic manager used by the chatbot system backend
- responsible for routing outbound model traffic from chatbot runtime services to configured upstream models
- configured per runtime environment by the chatbot backend or surrounding deployment workflow

It is not:

- the tenant orchestrator
- the customer-tier management service
- the namespace or cluster provisioning service
- the router for the admin control plane

---

# 14. Model Traffic Manager (Chatbot Runtime Router)

The chatbot system includes a Model Traffic Manager service.

Purpose:

- route requests to AI models
- manage load balancing
- support multiple providers
- apply the model-routing policy configured for the chatbot runtime environment

This service acts as the internal LLM gateway for chatbot runtime workloads.

---

## Responsibilities

model routing
provider selection
runtime traffic limiting
failover
health-aware model dispatch

---

## Example Routing

Request:

POST /chat
environment: tenant-acme-runtime
model: auto

Traffic Manager decides:

tenant-acme-runtime -> azure:gpt-4o
tenant-pizzabot-runtime -> azure:gpt-4o-mini
tenant-startupai-runtime -> local-llama

---

# 15. Chatbot Runtime Router Architecture

              Internet
                  |
                  ▼
          Chatbot Backend API
                  |
                  ▼
        Model Traffic Manager
                  |
      ------------------------------
      |            |               |
      ▼            ▼               ▼
   OpenAI      Azure OpenAI     Local Models

---

# 16. SaaS Control Plane vs Chatbot Runtime

Control Plane responsibilities:

- tenant onboarding
- customer-tier assignment
- placement strategy
- namespace provisioning
- quota and entitlement management

Chatbot Runtime responsibilities:

- chatbot application logic
- tenant-specific business configuration
- calling the internal Model Traffic Manager

Model Traffic Manager responsibilities in this repository:

- upstream selection
- failover
- health state
- runtime request limiting
- outbound auth to model providers

---

# 17. Full Platform Architecture

                           Internet
                               |
                               ▼
                        Global Ingress
                               |
                               ▼
                 Chatbot Backend Services
                               |
                               ▼
                    Internal Model Traffic Manager
                               |
                +--------------+--------------+
                |                             |
                ▼                             ▼
          Azure / OpenAI                 Local / Other Models

      Tenant namespaces and placement remain a concern of the control plane,
      not of the Model Traffic Manager itself.

---

# 18. Full Control Plane Architecture

                         +-------------------+
                         |  Admin Dashboard  |
                         +-------------------+
                                  |
                                  ▼
                         Provisioning Worker
                                  |
                 +----------------+----------------+
                 |                                 |
           Azure ARM API                    Kubernetes API
                 |                                 |
                 ▼                                 ▼
          Infrastructure                  Tenant Workloads

---

# 19. Key Design Principles

## Separation of Control and Runtime

Control Plane:

admin cluster
dashboard
orchestration

Runtime:

shared AKS
enterprise AKS

---

## Infrastructure vs Tenants

Terraform handles:

networks
base clusters
monitoring
registry
security

Dashboard handles:

tenants
namespaces
deployments
runtime orchestration
quotas

---

## Scalability

Shared cluster supports hundreds or thousands of tenants.

Enterprise customers can be isolated.

---

# 20. Benefits of This Architecture

- scalable SaaS model
- clear separation of concerns
- strong tenant isolation
- flexible pricing tiers
- easy expansion to multiple clusters
- supports voice + text AI workloads

---

# 21. Future Extensions

Possible future additions:

GPU node pools
vector databases per tenant
voice processing pipelines
regional clusters
edge inference

---

# End of Document
