# Source Formats and Parser Contracts

## Bank of Greece

The official Greek government-securities page publishes benchmark maturities in the fixed order:

`3, 5, 7, 10, 15, 20, 30 years`

Each row contains alternating price and yield columns. The parser therefore requires exactly fourteen cells:

`price_3, yield_3, ..., price_30, yield_30`

Both decimal commas and decimal points are accepted. Missing values are rejected rather than interpolated.

## Banca d'Italia

The Banca d'Italia *Financial Market* table `BMK0100` reports benchmark government securities gross yields to maturity. The BTP columns used by this project are:

`3-year, 5-year, 10-year, 30-year`

An optional fifth CCT column may follow and is deliberately excluded from the fixed-rate BTP comparison vector.

## Important limitation

These official source series are benchmark gross yields to maturity, not automatically zero-coupon continuously compounded spot rates. The parsers preserve that yield type and compounding metadata through the project data contract. Any later conversion to an NSS spot curve must remain explicitly documented as a modelling transformation, not a relabelling of the raw observations.

## Source references

- Bank of Greece: Greek government securities benchmark prices and yields.
- Banca d'Italia: *The Financial Market*, Table `BMK0100`, benchmark government securities gross yields to maturity.
