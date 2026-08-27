# Acquisition Protocol

## Purpose

Official source artifacts are captured before normalization. Parsing is a separate step from acquisition.

## Required provenance

Each captured artifact records:

- source name;
- source URL;
- UTC retrieval timestamp;
- SHA-256 checksum;
- local artifact path.

## Integrity rule

A captured artifact whose bytes no longer match its recorded SHA-256 checksum is rejected.

## Empirical rule

No adapter may invent a maturity, valuation date, yield, yield type, or compounding convention. Missing observations remain missing.

## Pipeline

1. Capture raw official artifact.
2. Record provenance and checksum.
3. Parse documented observations.
4. Normalize through the country-specific source adapter.
5. Validate each national cross-section.
6. Require a common Greece--Italy valuation date.
7. Estimate NSS curves.
8. Generate spot, discount-factor, spread, and diagnostic outputs.
