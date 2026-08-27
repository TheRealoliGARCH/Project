# Empirical protocol

1. Download observations from official Bank of Greece and Banca d'Italia publications or statistical endpoints.
2. Preserve the raw source file or exact source metadata outside the estimation code.
3. Record country, valuation date, maturity in years, yield, source, yield type, and compounding convention.
4. Align both countries to the same valuation date.
5. Reject duplicate or non-positive maturities.
6. Do not relabel coupon-bond yields-to-maturity as zero-coupon spot yields.
7. Fit NSS only after validation.
8. Label all outputs as model-implied when the input is not itself a zero-coupon curve.

The current repository intentionally contains no fabricated Italian observations. The empirical adapter milestone is complete only when official observations can be fetched or reproducibly imported with the metadata above.
