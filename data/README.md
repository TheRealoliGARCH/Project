# Data contract

The project intentionally separates raw sovereign-market data from model output.

Expected processed schema:

```text
country,date,maturity_years,yield_cc
Greece,YYYY-MM-DD,3,0.0290
Italy,YYYY-MM-DD,3,0.0292
```

`yield_cc` must be a decimal, continuously compounded annual model input. Raw coupon-bond yields-to-maturity must not be silently relabelled as observed zero-coupon rates. Any transformation must be documented in acquisition metadata and output must be described as model-implied where appropriate.

Raw official artifacts are captured with source URL, retrieval timestamp and SHA-256 checksum. The initial common-period specification is in `docs/EMPIRICAL_RUN_SPEC.md`: June 2025 is represented by the end-of-month label `2025-06-30` solely as a common monthly-period identifier.

The first empirical milestone is a common-period Greek/Italian maturity cross-section with sufficiently dense observations to support NSS estimation while preserving each source's documented yield convention.