# June 2025 empirical provenance

## Bank of Greece

Source: Bank of Greece, `Greek government securities`, monthly average prices and yields for June 2025.

Official page:
https://www.bankofgreece.gr/en/statistics/financial-markets-and-interest-rates/greek-government-securities?order=asc&page=1&year=2025

The recorded series are benchmark-bond clean prices and yields expressed in percent. The project retains only the benchmark maturities 3, 5, 7, 10, 15, 20 and 30 years for the yield cross-section; prices are retained as raw provenance fields.

## Banca d'Italia

Source: Banca d'Italia, *The Financial Market*, Table 5 / BMK0100, `Benchmark government securities: gross yields to maturity`.

Official publication used for the historical June 2025 row:
https://www.bancaditalia.it/pubblicazioni/mercato-finanziario/2026-mercato-finanziario/en_statistiche_MFN_20260615.pdf?language_id=1

The recorded series are gross yields to maturity for benchmark BTP maturities 3, 5, 10 and 30 years. CCT is excluded.

## Reserve Bank of India

Source: Reserve Bank of India, `Government Securities Market`, observed June 19, 2025.

Official page:
https://www.rbi.org.in/home.aspx/scripts/webservice/Scripts/CurrencyData.aspx

The raw file records the RBI-reported yields for 7.06% GS 2028, 6.75% GS 2029, 6.79% GS 2034, 6.92% GS 2039 and 7.09% GS 2054. Maturity in years is calculated as the approximate remaining time from the observation date to the stated calendar maturity year, using the security labels as the documented maturity anchors. These are therefore residual-maturity approximations rather than an RBI-published standardized tenor grid.

## Period convention

`2025-06` is a common June 2025 comparison period, not an assertion that all three central banks published observations at the same intraday timestamp.

## Transformation boundary

These raw yields are not zero-coupon spot rates. Any conversion to continuously compounded model inputs must be explicit and recorded separately; the raw files above must remain unchanged.
