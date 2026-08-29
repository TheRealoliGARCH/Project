# U5: Empirical and Causal Validation

## Purpose

U5 introduces an explicit causal-validation layer downstream of U1--U4. It is a computational validation harness, not an empirical claim about Greece, India, or Italy until real data are supplied and identified.

## Source-derived foundation

The supplied *Causal Inference via Ghoshian Condensation with Stochastic Optimal Control* formulates causal inference through treatment/control counterfactuals, the average treatment effect (ATE), difference-in-differences, Bayesian updating, and structural causal models. It also connects stochastic dynamics and optimal control through SDE and HJB formulations.

The supplied political-science paper describes stochastic political states, controls, uncertainty, policy optimization, and international-relations applications. The stochastic-control paper supplies the SDE/HJB numerical foundation.

## U5 estimands

For treatment and control outcomes, the empirical contrast is

    ATE = E[Y(1)] - E[Y(0)].

For a two-group, two-period design, the DID contrast is

    DID = (Y_T,post - Y_T,pre) - (Y_C,post - Y_C,pre).

The implementation provides sample analogues and a Welch-style large-sample uncertainty estimate.

For a scalar causal effect with a normal likelihood and normal prior, U5 also provides the conjugate posterior mean and standard deviation and the posterior probability that the effect is positive.

## Synthetic-first rule

Before country data are interpreted, estimators must pass deterministic synthetic tests in which the intended contrast is known. U5 does not infer causality from correlation alone.

## Ghoshian transformation

The supplied stochastic-control and causal-inference papers use

    G(x) = alpha + beta*x + chi*exp(alpha + beta*x) + delta,

with beta non-zero. U5 exposes this transformation as a deterministic primitive for synthetic identification experiments.

## Verification boundary

U5 currently verifies algebraic estimands and deterministic statistical primitives. It does not establish empirical identification, satisfy untestable causal assumptions automatically, estimate country-specific parameters, or claim that an intervention is exogenous. Those claims require an explicit design and data.
