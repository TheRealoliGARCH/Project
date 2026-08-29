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

## Unified theorem development

The project is being extended toward a unified verification framework for a three-Republic political-financial system. The development is deliberately modular: each theoretical layer is to be verified independently before the layers are coupled.

The current roadmap is:

1. **U1 — Algebraic closure:** verify the three-rate symmetric representation
   $$(r_1,r_2,r_3)\longleftrightarrow(r_A,r_B,r_C)\longleftrightarrow P(\lambda),$$
   including Vieta identities, root recovery, and permutation invariance.
2. **U2 — Political-financial closure:** verify the coupled fixed-point conditions for monetary and political states.
3. **U3 — Welfare--warfare optimality:** verify resource constraints, welfare first-order/second-order conditions, and strategic allocation consistency.
4. **U4 — Dynamic stability:** compute the closed-loop Jacobian, test spectral stability, and conduct perturbation and stress tests.
5. **U5 — ISG--BCI identification:** test whether observational and causal restrictions identify a unique latent realization, including discrimination of endogenous echo signals.
6. **U6 — Global uniqueness:** establish conditions under which the compatible equilibrium is unique rather than merely existent.
7. **U7 — End-to-end validation:** combine exact algebraic tests, numerical tests, statistical identification, Monte Carlo experiments, and empirical validation.

### U1 status: algebraic closure kernel implemented

The first executable U1 layer is now present in `src/algebraic_closure.py`, with deterministic tests in `tests/test_algebraic_closure.py`. It implements the three elementary symmetric invariants, the associated monic cubic, polynomial closure residuals, and permutation-invariance checks. The implementation uses only the Python standard library.

The central object is the unified equilibrium set

$$
\mathcal E
=
\mathcal A\cap\mathcal D\cap\mathcal W\cap\mathcal I,
$$

where $\mathcal A$, $\mathcal D$, $\mathcal W$, and $\mathcal I$ denote algebraic admissibility, dynamic stability, welfare--strategic admissibility, and epistemic identification respectively.

A unified equilibrium must satisfy all four classes of restrictions simultaneously. Separate validity of individual modules is not sufficient: the project must establish their compatibility at a common state.

## Verification principle

The computational program distinguishes exact identities from numerical and statistical claims. In particular, polynomial closure is not treated as synonymous with economic equilibrium; numerical stability is not treated as proof of global uniqueness; and statistical identification is not treated as proof of upstream algebraic consistency.

The intended progression is:

$$
\text{theory}
\rightarrow
\text{exact tests}
\rightarrow
\text{simulation}
\rightarrow
\text{data}
\rightarrow
\text{estimation}
\rightarrow
\text{stress testing}
\rightarrow
\text{institutional evaluation}.
$$

New implementation claims will be recorded here only as the corresponding code and tests are actually added to the repository.
