# Data contract

The project intentionally separates raw sovereign-market data from model output.

Expected processed schema:

```text
country,date,maturity_years,yield_cc
Greece,YYYY-MM-DD,3,0.0290
Italy,YYYY-MM-DD,3,0.0292
```

`yield_cc` must be a decimal, continuously compounded annual yield. Raw coupon-bond yields-to-maturity must not be silently relabelled as zero-coupon rates. Any transformation must be documented in the acquisition metadata.

The first empirical milestone is a common-date Greek/Italian maturity cross-section with sufficiently dense observations to support symmetric NSS estimation.
