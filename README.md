# Project

This repository contains reproducible research and computational verification for a unified sovereign political-financial framework, with an empirical foundation in sovereign term-structure and discount-factor analysis. The empirical work includes a Greece--India--Italy Nelson--Siegel--Svensson (NSS) study and the theoretical program develops a modular U1--U7 verification architecture for a three-Republic political-financial system.

## Repository scope

The Project brings together four complementary layers:

- **Empirical sovereign finance:** comparable official sovereign maturity cross-sections, NSS estimation, spot-yield curves, and continuously compounded discount factors.
- **Mathematical structure:** exact algebraic closure and explicit equilibrium restrictions.
- **Computational verification:** deterministic unit tests, numerical validation, stress testing, identification checks, global-uniqueness certificates, and end-to-end reconstruction.
- **Reproducible research:** executable workflows, generated research outputs, and a strict separation between observations, estimates, forecasts, and theoretical claims.

The three-Republic development framework is intended to study Greece, India, and Italy as a coupled political-financial system. The repository therefore treats monetary, political, welfare--strategic, dynamic, and epistemic restrictions as potentially interdependent rather than as isolated empirical exercises.

## Current paper

- `paper/nss_discount_curves.tex` — Nelson--Siegel--Svensson Estimation of Greek, Indian, and Italian Sovereign Discount Curves

The paper distinguishes coupon-bond yields-to-maturity from zero-coupon spot yields and defines the implied discount factor under continuous compounding as

$$
D(m)=e^{-m y(m)}.
$$

The empirical workflow uses comparable official sovereign maturity cross-sections for Greece, India, and Italy before making the three-country comparison.

## Reproducibility principle

Observed data, model estimates, and forecasts are kept distinct. Missing official observations are not silently fabricated or treated as measured values. Computational claims are accepted only when the corresponding code and tests are present in the repository.

## Unified verification framework

The current executable architecture is:

$$
\boxed{U1\rightarrow U2\rightarrow U3\rightarrow U4\rightarrow U5\rightarrow U6\rightarrow U7}
$$

Each layer is independently tested before being coupled into the integrated system.

1. **U1 — Algebraic closure:** verify the three-rate symmetric representation
   $$(r_1,r_2,r_3)\longleftrightarrow(r_A,r_B,r_C)\longleftrightarrow P(\lambda),$$
   including Vieta identities, root recovery, and permutation invariance.
2. **U2 — Political-financial closure:** verify the coupled fixed-point conditions for monetary and political states.
3. **U3 — Welfare--warfare optimality:** verify resource constraints, welfare first-order/second-order conditions, and strategic allocation consistency.
4. **U4 — Dynamic stability:** compute the closed-loop Jacobian, test spectral stability, and conduct perturbation and stress tests.
5. **U5 — ISG--BCI identification:** test whether observational and causal restrictions identify a unique latent realization, including discrimination of endogenous echo signals.
6. **U6 — Global uniqueness:** establish sufficient conditions under which the compatible equilibrium is unique rather than merely existent.
7. **U7 — End-to-end validation:** combine exact algebraic tests, numerical tests, statistical identification, Monte Carlo experiments, and empirical validation into a deterministic integrated pipeline.

### Implementation status

**U1--U7 are implemented and regression-tested.** The architecture currently provides:

- an executable algebraic-closure kernel;
- political-financial fixed-point validation;
- welfare--warfare optimality checks;
- dynamic stability and stress-testing machinery;
- ISG--BCI identification and causal-validation machinery;
- global-uniqueness/contraction certificates and validated Jacobian primitives;
- deterministic end-to-end stage contracts and reconstruction digests.

The NSS empirical layer has also been cleaned so that the canonical NSS loading calculation is defined in `src/nss.py` and consumed by the fitter, eliminating a duplicated numerical implementation.

## Unified equilibrium object

The central theoretical object is the unified equilibrium set

$$
\mathcal E
=
\mathcal A\cap\mathcal D\cap\mathcal W\cap\mathcal I,
$$

where $\mathcal A$, $\mathcal D$, $\mathcal W$, and $\mathcal I$ denote algebraic admissibility, dynamic stability, welfare--strategic admissibility, and epistemic identification respectively.

A unified equilibrium must satisfy all four classes of restrictions simultaneously. Separate validity of individual modules is not sufficient: the project must establish their compatibility at a common state.

## Verification principle

The computational program distinguishes exact identities from numerical and statistical claims. In particular, polynomial closure is not treated as synonymous with economic equilibrium; numerical stability is not treated as proof of global uniqueness; a contraction certificate is treated as sufficient rather than necessary; and statistical identification is not treated as proof of upstream algebraic consistency.

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
