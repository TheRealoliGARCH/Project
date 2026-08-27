# Project

This repository contains reproducible research for sovereign term-structure and discount-factor analysis, beginning with a Greece--Italy Nelson--Siegel--Svensson (NSS) study.

## Current paper

- `paper/nss_discount_curves.tex` — Nelson--Siegel--Svensson Estimation of Greek and Italian Sovereign Discount Curves

The paper distinguishes coupon-bond yields-to-maturity from zero-coupon spot yields and defines the implied discount factor under continuous compounding as

$$
D(m)=e^{-m y(m)}.
$$

The empirical workflow is designed to use comparable official Bank of Greece and Banca d'Italia maturity cross-sections before making a symmetric country comparison.

## Reproducibility principle

Observed data, model estimates, and forecasts are kept distinct. Missing official observations are not silently fabricated or treated as measured values.
