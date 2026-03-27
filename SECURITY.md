[Repository README](./README.md) | [Support](./SUPPORT.md) | [Contributing](./CONTRIBUTING.md)

# Security Policy

## Supported versions

Until `model-traffic-manager` reaches `1.0`, security fixes are provided on a best-effort basis for:

- the latest state of the default development branch
- the latest public release tag, when release tags exist

Older branches, stale forks, and pinned historical commits should not be assumed to receive security fixes.

## Reporting a vulnerability

Please do not open a public issue for exploitable vulnerabilities.

Preferred disclosure path:

1. use GitHub private vulnerability reporting if it is enabled for this repository
2. if that path is unavailable, contact the maintainer privately through the repository owner profile at [`PatrykIti`](https://github.com/PatrykIti)

Please include:

- affected version, branch, or commit
- deployment shape or environment details
- reproduction steps
- expected impact
- any relevant logs or traces with secrets removed

The goal is to acknowledge valid reports within five business days and to coordinate a fix before public disclosure whenever practical.

## Security scope

This repository treats the following areas as security-sensitive:

- inbound authentication and authorization
- outbound identity and secret handling
- Azure and AKS validation runners
- routing decisions that could expose traffic to the wrong upstream
- observability paths that could leak secrets or caller credentials

## Disclosure expectations

- do not publish proof-of-concept exploit details before a fix or mitigation exists
- redact API keys, bearer tokens, JWTs, and secret references from all reports
- prefer the smallest reproducible case that still demonstrates impact
