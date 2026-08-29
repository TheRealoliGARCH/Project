"""Algebraic closure primitives for the three-rate financial system.

The module deliberately uses only the Python standard library.  It implements
Vieta's elementary symmetric invariants for three rates and evaluates the
associated monic cubic.  Root recovery is intentionally kept separate from
these exact identities: a numerical root solver is not needed to verify the
forward algebraic closure itself.
"""

from __future__ import annotations

from itertools import permutations
from math import isclose
from typing import Iterable, Sequence


def symmetric_invariants(rates: Sequence[float]) -> tuple[float, float, float]:
    """Return the elementary symmetric invariants of exactly three rates.

    Returns ``(r_A, r_B, r_C)`` where

    ``r_A = r1 + r2 + r3``
    ``r_B = r1*r2 + r2*r3 + r3*r1``
    ``r_C = r1*r2*r3``.
    """
    if len(rates) != 3:
        raise ValueError("exactly three rates are required")
    r1, r2, r3 = rates
    return (
        r1 + r2 + r3,
        r1 * r2 + r2 * r3 + r3 * r1,
        r1 * r2 * r3,
    )


def polynomial_value(x: float, invariants: Sequence[float]) -> float:
    """Evaluate lambda^3 - r_A lambda^2 + r_B lambda - r_C."""
    if len(invariants) != 3:
        raise ValueError("exactly three invariants are required")
    r_a, r_b, r_c = invariants
    return x**3 - r_a * x**2 + r_b * x - r_c


def closure_residual(rates: Sequence[float]) -> float:
    """Return max absolute polynomial residual at the three supplied rates."""
    invariants = symmetric_invariants(rates)
    return max(abs(polynomial_value(rate, invariants)) for rate in rates)


def permuted_invariants(rates: Sequence[float]) -> set[tuple[float, float, float]]:
    """Return invariants for every permutation of a three-rate vector."""
    if len(rates) != 3:
        raise ValueError("exactly three rates are required")
    return {symmetric_invariants(p) for p in permutations(rates)}


def permutation_invariant(rates: Sequence[float], *, rel_tol: float = 1e-12, abs_tol: float = 1e-12) -> bool:
    """Check that all six permutations preserve the symmetric invariants."""
    base = symmetric_invariants(rates)
    return all(
        all(isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol) for a, b in zip(base, candidate))
        for candidate in permuted_invariants(rates)
    )


def vieta_reconstruction(rates: Sequence[float], x: float) -> float:
    """Evaluate the cubic constructed from ``rates`` at ``x``."""
    return polynomial_value(x, symmetric_invariants(rates))
