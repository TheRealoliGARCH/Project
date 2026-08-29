"""U4 deterministic stress-testing and robustness kernel.

U4 evaluates the reduced-form three-Republic equilibrium under explicit
financial, political, security, and external-cooperation shocks.  It is a
robustness layer downstream of U2 closure and U3 welfare-warfare optimality.
The kernel deliberately does not assign empirical probabilities to shocks.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable


@dataclass(frozen=True)
class U4State:
    """Three-Republic state used for deterministic stress tests."""

    political: tuple[float, ...]
    financial: tuple[float, ...]
    security: tuple[float, ...]
    defense: tuple[float, ...]
    output: tuple[float, ...]

    def validate(self) -> None:
        dimensions = {len(self.political), len(self.financial), len(self.security), len(self.defense), len(self.output)}
        if dimensions != {3}:
            raise ValueError("U4 requires exactly three Republics")
        values: Iterable[float] = (
            *self.political,
            *self.financial,
            *self.security,
            *self.defense,
            *self.output,
        )
        if not all(isfinite(x) for x in values):
            raise ValueError("state values must be finite")
        if any(y <= 0 for y in self.output):
            raise ValueError("output must be positive")
        if any(g < 0 or g > y for g, y in zip(self.defense, self.output)):
            raise ValueError("defense must satisfy 0 <= defense <= output")


@dataclass(frozen=True)
class U4Shock:
    """Additive shock to the four U4 channels."""

    financial: tuple[float, ...] = (0.0, 0.0, 0.0)
    political: tuple[float, ...] = (0.0, 0.0, 0.0)
    security: tuple[float, ...] = (0.0, 0.0, 0.0)
    external_cooperation: tuple[float, ...] = (0.0, 0.0, 0.0)

    def validate(self) -> None:
        fields = (self.financial, self.political, self.security, self.external_cooperation)
        if any(len(x) != 3 for x in fields):
            raise ValueError("each shock channel must have three Republic values")
        if not all(isfinite(x) for field in fields for x in field):
            raise ValueError("shock values must be finite")


@dataclass(frozen=True)
class U4Result:
    """Stress-test result with explicit feasibility and stability diagnostics."""

    shocked_state: U4State
    state_deviation: tuple[float, ...]
    max_absolute_deviation: float
    feasible: bool
    stability_margin: float

    @property
    def robust(self) -> bool:
        """Return whether the scenario is feasible and has positive stability margin."""
        return self.feasible and self.stability_margin > 0.0


def apply_shock(state: U4State, shock: U4Shock) -> U4State:
    """Apply an additive shock without silently clipping the resulting state."""
    state.validate()
    shock.validate()
    return U4State(
        political=tuple(a + b for a, b in zip(state.political, shock.political)),
        financial=tuple(a + b for a, b in zip(state.financial, shock.financial)),
        security=tuple(a + b + c for a, b, c in zip(state.security, shock.security, shock.external_cooperation)),
        defense=state.defense,
        output=state.output,
    )


def state_deviation(baseline: U4State, shocked: U4State) -> tuple[float, ...]:
    """Return the six political/financial deviations used by U4 reporting."""
    baseline.validate()
    shocked.validate()
    return tuple(
        [b - a for a, b in zip(baseline.political, shocked.political)]
        + [b - a for a, b in zip(baseline.financial, shocked.financial)]
    )


def feasibility_margin(state: U4State) -> float:
    """Return the minimum resource margin Y-G_m across the three Republics."""
    state.validate()
    return min(y - g for y, g in zip(state.output, state.defense))


def stability_margin(coupling_bound: float) -> float:
    """Return the conservative local stability margin 1-||J||_infinity."""
    if not isfinite(coupling_bound) or coupling_bound < 0:
        raise ValueError("coupling_bound must be finite and non-negative")
    return 1.0 - coupling_bound


def stress_test(state: U4State, shock: U4Shock, coupling_bound: float) -> U4Result:
    """Evaluate one deterministic stress scenario.

    A scenario is robust when resources remain feasible and the supplied
    Jacobian infinity-norm bound remains strictly below one.  This is a
    sufficient local-stability certificate, not a claim of global stability.
    """
    baseline = state
    shocked = apply_shock(state, shock)
    deviation = state_deviation(baseline, shocked)
    return U4Result(
        shocked_state=shocked,
        state_deviation=deviation,
        max_absolute_deviation=max((abs(x) for x in deviation), default=0.0),
        feasible=feasibility_margin(shocked) > 0.0,
        stability_margin=stability_margin(coupling_bound),
    )


def shock_grid(levels: tuple[float, ...] = (-1.0, 0.0, 1.0)) -> tuple[U4Shock, ...]:
    """Return deterministic one-channel shocks for reproducible stress tests."""
    if not levels or not all(isfinite(x) for x in levels):
        raise ValueError("levels must contain finite values")
    shocks = []
    for level in levels:
        shocks.extend(
            [
                U4Shock(financial=(level, 0.0, 0.0)),
                U4Shock(political=(level, 0.0, 0.0)),
                U4Shock(security=(level, 0.0, 0.0)),
                U4Shock(external_cooperation=(level, 0.0, 0.0)),
            ]
        )
    return tuple(shocks)
