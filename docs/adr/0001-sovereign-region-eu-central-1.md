# 1. Selection of AWS Frankfurt (eu-central-1) as Sovereign Region

Date: 2026-01-10

## Status
Accepted

## Context
Deploying enterprise machine learning pipelines within the European Union requires compliance with the GDPR and Schrems II rulings regarding transatlantic data transfer restrictions.

## Decision
We establish **`eu-central-1` (Frankfurt, Germany)** as the primary sovereign deployment region for all compute, storage, and container registries, with `eu-west-1` (Dublin) as an EEA secondary failover.

## Consequences
- Guarantees 100% European data residency.
- Satisfies German BDSG and EU-wide GDPR regulatory standards.
- Low-latency access (< 15ms) across Central Europe.
