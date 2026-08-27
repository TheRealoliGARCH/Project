# Official Source Adapters

The project separates acquisition from normalization.

`src.sources` currently provides deterministic adapters for explicitly supplied
official observations from the Bank of Greece and Banca d'Italia. Each input
record must contain:

- `maturity_years`
- `yield_percent`

The caller must also supply one valuation date for the cross-section. The
adapter converts percentage yields to decimal form and preserves the source,
yield type, and compounding metadata in the `Observation` contract.

These functions are intentionally not web scrapers. Official websites may
change formats, and silent scraping failure can contaminate empirical work.
A future acquisition module should download or parse a documented official
artifact, store the raw artifact or a cryptographic checksum, and then pass
explicitly extracted records through these adapters.

## Methodological boundary

A normalized `benchmark yield` remains a benchmark yield. The adapter does not
relabel it as a zero-coupon spot rate. Any transformation from coupon-bearing
market data to a zero-coupon curve must be explicit in a later estimation or
bootstrapping stage.
