"""Canonical U3 -> U4 interface."""

from __future__ import annotations

from math import isfinite
from typing import Mapping, Sequence, Tuple

REPUBLICS = ("Greece", "India", "Italy")
Vector = Tuple[float, float, float]
REQUIRED = ("p", "r", "s", "G_m", "Y")


class U34InterfaceError(ValueError):
    """Raised when the U3 -> U4 contract is violated."""


def _vector(values: Sequence[float], field: str) -> Vector:
    if len(values) != 3:
        raise U34InterfaceError(f"{field} must contain exactly three values")
    result = tuple(float(value) for value in values)
    if not all(isfinite(value) for value in result):
        raise U34InterfaceError(f"{field} must contain only finite values")
    return result  # type: ignore[return-value]


def u3_to_u4_baseline(state: Mapping[str, Sequence[float]]) -> dict[str, Vector]:
    """Extract the exact U4 baseline from a U3 output state."""
    missing = [field for field in REQUIRED if field not in state]
    if missing:
        raise U34InterfaceError(f"missing U3 output fields: {', '.join(missing)}")

    result = {field: _vector(state[field], field) for field in REQUIRED}
    for i, (g, y) in enumerate(zip(result["G_m"], result["Y"])):
        if g < 0.0 or y < 0.0:
            raise U34InterfaceError(f"negative resource value for {REPUBLICS[i]}")
        if g > y:
            raise U34InterfaceError(
                f"resource constraint violated for {REPUBLICS[i]}: G_m={g} > Y={y}"
            )
    return result


def validate_consumption_identity(state: Mapping[str, Sequence[float]], tolerance: float = 1e-12) -> Vector:
    """Return C_i=Y_i-G_m,i and validate the U3 resource identity."""
    baseline = u3_to_u4_baseline(state)
    consumption = tuple(y - g for y, g in zip(baseline["Y"], baseline["G_m"]))
    if not all(c >= -tolerance for c in consumption):
        raise U34InterfaceError("U3 resource identity implies negative consumption")
    return consumption  # type: ignore[return-value]


__all__ = ["REPUBLICS", "U34InterfaceError", "u3_to_u4_baseline", "validate_consumption_identity"]
