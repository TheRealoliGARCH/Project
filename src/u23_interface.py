"""Canonical U2 -> U3 interface.

U2 exposes the coupled state X=(r,p,s,g). U3 consumes the ordered
three-Republic baseline needed for welfare/warfare allocation. This adapter
makes that field-level hand-off explicit and refuses ambiguous or invalid
states.
"""

from __future__ import annotations

from math import isfinite
from typing import Mapping, Sequence, Tuple


REPUBLICS = ("Greece", "India", "Italy")


class U23InterfaceError(ValueError):
    """Raised when the U2 -> U3 contract is violated."""


def _triplet(values: Sequence[float], field: str) -> Tuple[float, float, float]:
    if len(values) != 3:
        raise U23InterfaceError(f"{field} must contain exactly three values")
    result = tuple(float(value) for value in values)
    if not all(isfinite(value) for value in result):
        raise U23InterfaceError(f"{field} must contain only finite values")
    return result


def u2_to_u3_baseline(state: Mapping[str, Sequence[float]]) -> dict[str, Tuple[float, float, float]]:
    """Map U2 state fields into the canonical U3 baseline.

    Required fields are r, p, s, and g, each ordered as Greece, India, Italy.
    U3 receives copies of the values; no field is inferred from another.
    """
    required = ("r", "p", "s", "g")
    missing = [field for field in required if field not in state]
    if missing:
        raise U23InterfaceError(f"missing U2 state fields: {', '.join(missing)}")
    return {field: _triplet(state[field], field) for field in required}


def validate_u3_resource_feasibility(
    baseline: Mapping[str, Sequence[float]],
    output: Sequence[float],
) -> Tuple[float, float, float]:
    """Validate C_i = Y_i - G_m,i and the U3 admissible resource domain."""
    g = _triplet(baseline["g"], "g")
    y = _triplet(output, "Y")
    consumption = tuple(yi - gi for yi, gi in zip(y, g))
    if not all(ci >= 0.0 for ci in consumption):
        raise U23InterfaceError("U3 resource constraint violated: C_i = Y_i - G_m,i must be non-negative")
    return consumption


__all__ = ["REPUBLICS", "U23InterfaceError", "u2_to_u3_baseline", "validate_u3_resource_feasibility"]
