"""Canonical U1 -> U2 interface.

U1's symmetric invariants are deliberately kept distinct from the ordered
three-Republic financial vector consumed by U2. Root recovery from the
symmetric polynomial is permutation-invariant and therefore cannot, by itself,
assign roots to Greece, India, and Italy.
"""

from __future__ import annotations

from math import isfinite
from typing import Sequence, Tuple


RepublicRates = Tuple[float, float, float]
SymmetricRates = Tuple[float, float, float]


class U12InterfaceError(ValueError):
    """Raised when a U1 -> U2 hand-off violates its contract."""


def _finite_triplet(values: Sequence[float], name: str) -> RepublicRates:
    if len(values) != 3:
        raise U12InterfaceError(f"{name} must contain exactly three values")
    result = tuple(float(value) for value in values)
    if not all(isfinite(value) for value in result):
        raise U12InterfaceError(f"{name} must contain only finite values")
    return result  # type: ignore[return-value]


def symmetric_invariants(rates: Sequence[float]) -> SymmetricRates:
    """Return U1 elementary symmetric invariants for three rates."""
    r1, r2, r3 = _finite_triplet(rates, "rates")
    return (
        r1 + r2 + r3,
        r1 * r2 + r2 * r3 + r3 * r1,
        r1 * r2 * r3,
    )


def u1_to_u2_financial_state(
    republic_rates: Sequence[float],
) -> RepublicRates:
    """Pass an ordered U1 rate vector into the U2 financial state.

    The canonical U2 ordering is (Greece, India, Italy). This adapter is an
    identity on the ordered rate vector; symmetric invariants are available
    separately and are never substituted for the ordered state.
    """
    return _finite_triplet(republic_rates, "republic_rates")


def validate_symmetric_closure(rates: Sequence[float], invariants: Sequence[float]) -> None:
    """Validate that supplied U1 invariants correspond to the ordered rates."""
    expected = symmetric_invariants(rates)
    supplied = _finite_triplet(invariants, "invariants")
    for index, (actual, target) in enumerate(zip(supplied, expected)):
        tolerance = 1e-12 * max(1.0, abs(target))
        if abs(actual - target) > tolerance:
            raise U12InterfaceError(
                f"symmetric invariant {index} violates U1 closure: "
                f"expected {target}, received {actual}"
            )


__all__ = [
    "RepublicRates",
    "SymmetricRates",
    "U12InterfaceError",
    "symmetric_invariants",
    "u1_to_u2_financial_state",
    "validate_symmetric_closure",
]
