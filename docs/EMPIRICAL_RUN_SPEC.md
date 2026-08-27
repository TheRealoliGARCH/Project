# Greece--Italy Empirical Run Specification

## Common-period convention

The first reproducible comparison uses monthly-average observations for June 2025. The project's valuation-date field is set to `2025-06-30`, meaning the end-of-month label for that common monthly observation period; it does not claim that either source published an intraday cross-section at midnight on that date.

## Official sources

Greece: Bank of Greece, `Greek government securities`:
https://www.bankofgreece.gr/en/statistics/financial-markets-and-interest-rates/greek-government-securities

The published benchmark maturities are 3, 5, 7, 10, 15, 20 and 30 years.

Italy: Banca d'Italia, `BMK0100 - Titoli di Stato guida: rendimenti a scadenza lordi`.
The project uses the BTP 3, 5, 10 and 30 year columns and excludes CCT.

## Interpretation boundary

Both inputs are benchmark yields to maturity. The initial model maps the fitted NSS yield curve into a model discount curve. Outputs must be labelled `model-implied discount factors`, not observed zero-coupon discount factors.

## Required provenance

Before an empirical result is accepted, the exact source artifacts used must be captured by `src.acquisition`, with source URL, retrieval timestamp and SHA-256 checksum retained alongside the raw artifact.

## Selection rule

Use a monthly observation only when both countries have a documented value for the same calendar month. Label that common period by its final calendar day and reject silent interpolation or carry-forward.
