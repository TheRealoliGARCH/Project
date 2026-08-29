"""U5 empirical and causal validation primitives.

This module implements deterministic synthetic identification checks inspired by
the supplied Ghoshian stochastic-control and causal-inference papers. It keeps
causal estimands explicit: treatment/control contrasts, ATE, DID, and a
normal-normal Bayesian posterior for a scalar causal effect.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, sqrt
from statistics import NormalDist
from typing import Sequence


@dataclass(frozen=True)
class CausalEstimate:
    effect: float
    standard_error: float
    z_score: float
    p_value_two_sided: float


def _finite_vector(values: Sequence[float], name: str) -> None:
    if not values:
        raise ValueError(f"{name} must be non-empty")
    if not all(isfinite(x) for x in values):
        raise ValueError(f"{name} must contain only finite values")


def ghoshian_transform(x: float, alpha: float, beta: float, chi: float, delta: float) -> float:
    """Evaluate G(x)=alpha+beta*x+chi*exp(alpha+beta*x)+delta."""
    if not all(isfinite(v) for v in (x, alpha, beta, chi, delta)) or beta == 0:
        raise ValueError("inputs must be finite and beta must be non-zero")
    value = alpha + beta * x + chi * exp(alpha + beta * x) + delta
    if not isfinite(value):
        raise ValueError("Ghoshian transform is not finite")
    return value


def ate(treated: Sequence[float], control: Sequence[float]) -> float:
    """Difference in sample means, the empirical analogue of the ATE contrast."""
    _finite_vector(treated, "treated")
    _finite_vector(control, "control")
    return sum(treated) / len(treated) - sum(control) / len(control)


def difference_in_differences(
    treated_pre: Sequence[float], treated_post: Sequence[float],
    control_pre: Sequence[float], control_post: Sequence[float],
) -> float:
    """Return the canonical two-group, two-period DID contrast."""
    for values, name in ((treated_pre, "treated_pre"), (treated_post, "treated_post"),
                         (control_pre, "control_pre"), (control_post, "control_post")):
        _finite_vector(values, name)
    if not (len(treated_pre) and len(treated_post) and len(control_pre) and len(control_post)):
        raise ValueError("all DID samples must be non-empty")
    treated_change = sum(treated_post) / len(treated_post) - sum(treated_pre) / len(treated_pre)
    control_change = sum(control_post) / len(control_post) - sum(control_pre) / len(control_pre)
    return treated_change - control_change


def frequentist_effect(treated: Sequence[float], control: Sequence[float]) -> CausalEstimate:
    """Welch-style large-sample estimate for a two-sample causal contrast."""
    _finite_vector(treated, "treated")
    _finite_vector(control, "control")
    if len(treated) < 2 or len(control) < 2:
        raise ValueError("at least two observations per arm are required")
    mt = sum(treated) / len(treated)
    mc = sum(control) / len(control)
    vt = sum((x - mt) ** 2 for x in treated) / (len(treated) - 1)
    vc = sum((x - mc) ** 2 for x in control) / (len(control) - 1)
    se = sqrt(vt / len(treated) + vc / len(control))
    if se <= 0 or not isfinite(se):
        raise ValueError("standard error must be positive")
    z = (mt - mc) / se
    p = 2.0 * (1.0 - NormalDist().cdf(abs(z)))
    return CausalEstimate(mt - mc, se, z, p)


def normal_normal_posterior(
    estimate: float, standard_error: float, prior_mean: float = 0.0, prior_sd: float = 1.0,
) -> tuple[float, float]:
    """Return posterior mean and SD for a normal likelihood and normal prior."""
    values = (estimate, standard_error, prior_mean, prior_sd)
    if not all(isfinite(v) for v in values):
        raise ValueError("inputs must be finite")
    if standard_error <= 0 or prior_sd <= 0:
        raise ValueError("standard_error and prior_sd must be positive")
    prior_precision = 1.0 / (prior_sd ** 2)
    likelihood_precision = 1.0 / (standard_error ** 2)
    posterior_precision = prior_precision + likelihood_precision
    posterior_mean = (prior_precision * prior_mean + likelihood_precision * estimate) / posterior_precision
    posterior_sd = 1.0 / sqrt(posterior_precision)
    return posterior_mean, posterior_sd


def posterior_probability_positive(mean: float, sd: float) -> float:
    """Return P(effect > 0) under a normal posterior."""
    if not isfinite(mean) or not isfinite(sd) or sd <= 0:
        raise ValueError("mean must be finite and sd must be positive")
    return NormalDist().cdf(mean / sd)
