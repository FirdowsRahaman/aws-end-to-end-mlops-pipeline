# 2. Integration of Green AI & Carbon Footprint Telemetry

Date: 2026-02-01

## Status
Accepted

## Context
European enterprise standards and ESG regulations (EU Corporate Sustainability Due Diligence Directive - CSDDD) require organizations to account for the carbon footprint of intensive compute operations such as ML model training.

## Decision
We embed automated power and carbon emission telemetry tracking (`monitoring/carbon_tracker.py`) into all continuous training pipelines, logging kWh and kg CO2e per experiment into CloudWatch and S3.

## Consequences
- Produces verifiable ESG / Green AI compliance evidence.
- Encourages model optimization (quantization, pruning, efficient batching).
