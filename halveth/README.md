# HALVETH × TRON

An extensible research and development environment
built on the TRON java-tron codebase.

## Modules

- networks: Independent blockchain networks
- nodes: Node configurations and lifecycle
- contracts: TVM and smart-contract development
- agents: Automation and autonomous experiments
- audits: Security validation and regression testing
- experiments: Consensus, state and protocol research
- tools: Reusable development utilities

## First implemented research tool

- [PBFT Quorum Lab](experiments/README.md): a browser-based, offline model of
  quorum intersection and availability bounds, with explicit separation from
  TRON's documented DPoS block-solidification rule.

## Research process

SOURCE → RECEIVE → RELATE → VERIFY → PRESERVE → UPDATE

## Security research

Unpublished vulnerability reports, exploit reproductions,
private keys and confidential evidence are maintained
separately from this public repository.

## Provenance and licensing

This repository is a public fork of java-tron. The upstream source and this
repository's root `LICENSE` remain the governing license reference for files
added here. HALVETH-specific work is kept in the `halveth/` directory with
source links and explicit scope notes. This directory does not claim ownership
of upstream TRON code or third-party research. Keep unpublished security
evidence and private research attachments out of this public fork.

Upstream: https://github.com/tronprotocol/java-tron
