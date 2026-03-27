# Changelog

This changelog tracks released versions and public release notes for `model-traffic-manager`.

Internal task-level delivery history remains in `_docs/_CHANGELOG/`.

## v0.1.0 - 2026-03-27

### Added
- first public release of `model-traffic-manager` (#1)
- Azure-native routing for chat completions and embeddings (#1)
- tiered failover, cooldown, circuit handling, and weighted routing (#1)
- outbound Managed Identity support with API-key fallback (#1)
- inbound API bearer-token and Microsoft Entra ID authentication (#1)
- Azure-backed and AKS-backed live validation suites (#1)
- Apache-2.0 license, funding metadata, and public repository trust files (#1)

### Changed
- root README to position the repository as a stronger flagship product (#1)
- contribution flow to be simpler for external contributors while preserving the maintainer workflow (#1)
- public repository surface with clearer product framing, audience fit, and architecture overview (#1)

### Fixed
- live AKS validation stability issues around observability and inbound-auth execution paths (#1)
- inbound-auth live suite caller-pod selection so the suite targets a running ready pod (#1)

### Security
- protected router entrypoints can now enforce explicit inbound authentication and authorization (#1)
- the repository now includes a public security reporting path and support guidance (#1)
