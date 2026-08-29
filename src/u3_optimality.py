"""U3 welfare--warfare optimality kernel.

U3 verifies the resource-allocation layer specified by the Project roadmap:
resource constraints, welfare first-order/second-order conditions, and
strategic allocation consistency.  The kernel is deliberately reduced-form:
security production is supplied as a deterministic function so that empirical
or structural security specifications can be added without changing the
welfare accounting identities.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, log
from typing import Callable, Sequence


SecurityFunction = Callable[[float, float, float], float]


@dataclass(frozen=True)
class U3Parameters:
    """Parameters for a single Republic's welfare problem."""

    output: float
    preference_security: float
    threat: float
    external_security: float

    def validate(self) -> None:
        values = (self.output, self.preference_security, self.threat, self.external_security)
        if not all(isfinite(x) for x in values):
            raise ValueError("parameters must be finite")
        if self.output <= 0:
            raise ValueError("output must be positive")
        if not 0 < self.preference_security < 1:
            raise ValueError("preference_security must lie strictly between 0 and 1")
        if self.threat < 0 or self.external_security < 0:
            raise ValueError("threat and external security must be non-negative")


def resource_constraint(output: float, defense: float) -> float:
    """Return civilian resources C = Y - G_m."""
    if not isfinite(output) or not isfinite(defense):
        raise ValueError("output and defense must be finite")
    if output <= 0:
        raise ValueError("output must be positive")
    if defense < 0 or defense > output:
        raise ValueError("defense must satisfy 0 <= defense <= output")
    return output - defense


def welfare(
    output: float,
    defense: float,
    preference_security: float,
    security_fn: SecurityFunction,
    threat: float,
    external_security: float,
) -> float:
    """Compute W = alpha log(C) + (1-alpha) log(S)."""
    if not 0 < preference_security < 1:
        raise ValueError("preference_security must lie strictly between 0 and 1")
    civilian = resource_constraint(output, defense)
    security = security_fn(defense, threat, external_security)
    if civilian <= 0 or security <= 0:
        raise ValueError("welfare requires positive civilian resources and security")
    return preference_security * log(civilian) + (1.0 - preference_security) * log(security)


def finite_difference_first(
    function: Callable[[float], float], x: float, step: float = 1e-5
) -> float:
    """Central finite-difference first derivative."""
    if step <= 0 or not isfinite(step):
        raise ValueError("step must be finite and positive")
    return (function(x + step) - function(x - step)) / (2.0 * step)


def finite_difference_second(
    function: Callable[[float], float], x: float, step: float = 1e-4
) -> float:
    """Central finite-difference second derivative."""
    if step <= 0 or not isfinite(step):
        raise ValueError("step must be finite and positive")
    return (function(x + step) - 2.0 * function(x) + function(x - step)) / (step * step)


def welfare_derivatives(
    output: float,
    defense: float,
    preference_security: float,
    security_fn: SecurityFunction,
    threat: float,
    external_security: float,
    step: float = 1e-5,
) -> tuple[float, float]:
    """Return numerical first and second derivatives of welfare with respect to defense."""
    params = (output, preference_security, threat, external_security)
    if not all(isfinite(x) for x in params):
        raise ValueError("inputs must be finite")
    if defense <= step or defense + step >= output:
        raise ValueError("defense must leave room for central differences")

    def objective(g: float) -> float:
        return welfare(
            output,
            g,
            preference_security,
            security_fn,
            threat,
            external_security,
        )

    first = finite_difference_first(objective, defense, step)
    second = finite_difference_second(objective, defense, step)
    return first, second


def security_power(defense: float, threat: float, external_security: float, productivity: float = 1.0, elasticity: float = 0.5) -> float:
    """Simple concave security production benchmark: S = 1 + A G^eta + E - T."""
    if productivity <= 0 or not 0 < elasticity <= 1:
        raise ValueError("productivity must be positive and elasticity must lie in (0, 1]")
    if defense < 0 or threat < 0 or external_security < 0:
        raise ValueError("defense, threat, and external security must be non-negative")
    return 1.0 + productivity * defense**elasticity + external_security - threat


def welfare_foc_residual(*args, **kwargs) -> float:
    """Return the U3 welfare FOC residual; equilibrium requires it to be zero."""
    first, _ = welfare_derivatives(*args, **kwargs)
    return first


def welfare_soc(*args, **kwargs) -> float:
    """Return the U3 second-order condition value; a strict local maximum has SOC < 0."""
    _, second = welfare_derivatives(*args, **kwargs)
    return second


def check_resource_allocation(weights: Sequence[float], states: Sequence[float], target: float, tolerance: float = 1e-10) -> bool:
    """Check non-negative simplex weights and exact target reproduction within tolerance."""
    if len(weights) != len(states) or len(weights) == 0:
        raise ValueError("weights and states must have equal non-zero dimension")
    if tolerance < 0 or not isfinite(tolerance):
        raise ValueError("tolerance must be finite and non-negative")
    if not all(isfinite(x) for x in weights) or not all(isfinite(x) for x in states) or not isfinite(target):
        raise ValueError("weights, states, and target must be finite")
    if any(w < -tolerance for w in weights):
        return False
    if abs(sum(weights) - 1.0) > tolerance:
        return False
    reproduced = sum(w * x for w, x in zip(weights, states))
    return abs(reproduced - target) <= tolerance


def strategic_allocation_residual(weights: Sequence[float], states: Sequence[float], target: float) -> tuple[float, float]:
    """Return simplex and target residuals for a strategic allocation."""
    if len(weights) != len(states) or not weights:
        raise ValueError("weights and states must have equal non-zero dimension")
    simplex_residual = sum(weights) - 1.0
    target_residual = sum(w * x for w, x in zip(weights, states)) - target
    return simplex_residual, target_residual


def validate_u3_point(params: U3Parameters, defense: float, security_fn: SecurityFunction) -> None:
    """Validate an interior U3 candidate point."""
    params.validate()
    if not isfinite(defense) or not 0.0 < defense < params.output:
        raise ValueError("defense must lie strictly between zero and output for an interior candidate")
    security = security_fn(defense, params.threat, params.external_security)
    if not isfinite(security) or security <= 0:
        raise ValueError("candidate security must be finite and positive")
