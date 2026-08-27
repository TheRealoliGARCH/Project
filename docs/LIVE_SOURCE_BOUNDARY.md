# Controlled Live-Source Boundary

Live retrieval is intentionally separated from estimation and parsing.

## Contract

1. Retrieve an official artifact once from an explicit URL.
2. Persist the raw response verbatim.
3. Record source name, URL, UTC retrieval time, and SHA-256 checksum.
4. Verify the captured artifact before downstream parsing.
5. Select a documented row explicitly; ambiguous matches fail.
6. Pass cells to the existing country parser and adapter.

## Non-goals

The live boundary does not:

- interpolate maturities;
- infer missing dates;
- repair missing yields;
- convert yields to zero-coupon rates;
- relabel gross YTM as a spot rate.

## Testability

Network retrieval is dependency-injected. Unit tests use deterministic fetchers and do not require live network access. Production callers supply explicit official source URLs and documented row selectors.
