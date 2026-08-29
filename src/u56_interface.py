"""Canonical U5 -> U6 identification/uniqueness interface.

Statistical identification and mathematical uniqueness are distinct claims.
This adapter carries identified restrictions and their epistemic provenance
into U6 without converting them into a uniqueness certificate.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Mapping, Sequence, Tuple


class U56InterfaceError(ValueError):
    """Raised when the U5 -> U6 contract is violated."""


@dataclass(frozen=True)
class IdentificationResult:
    """U5 output relevant to the U6 hand-off."""

    parameter_names: Tuple[str, ...]
    estimates: Tuple[float, ...]
    identified: Tuple[bool, ...]
    uncertainty: Tuple[float, ...]
    provenance: str


@dataclass(frozen=True)
class EquilibriumRestrictions:
    """U6 input derived from U5, without a uniqueness claim."""

    parameter_names: Tuple[str, ...]
    restrictions: Tuple[float, ...]
    uncertainty: Tuple[float, ...]
    provenance: str
    uniqueness_certified: bool = False


def _finite_vector(values: Sequence[float], name: str) -> Tuple[float, ...]:
    result = tuple(float(v) for v in values)
    if not result:
        raise U56InterfaceError(f"{name} must be non-empty")
    if not all(isfinite(v) for v in result):
        raise U56InterfaceError(f"{name} must contain only finite values")
    return result


def build_identification_result(
    parameter_names: Sequence[str],
    estimates: Sequence[float],
    identified: Sequence[bool],
    uncertainty: Sequence[float],
    *,
    provenance: str,
) -> IdentificationResult:
    names = tuple(parameter_names)
    if not names or len(set(names)) != len(names) or any(not name for name in names):
        raise U56InterfaceError("parameter_names must be non-empty and unique")
    estimates_v = _finite_vector(estimates, "estimates")
    uncertainty_v = _finite_vector(uncertainty, "uncertainty")
    identified_v = tuple(bool(v) for v in identified)
    if len(estimates_v) != len(names) or len(identified_v) != len(names) or len(uncertainty_v) != len(names):
        raise U56InterfaceError("parameter fields must have equal lengths")
    if any(v < 0.0 for v in uncertainty_v):
        raise U56InterfaceError("uncertainty must be non-negative")
    if not provenance:
        raise U56InterfaceError("provenance must be non-empty")
    return IdentificationResult(names, estimates_v, identified_v, uncertainty_v, provenance)


def identification_to_equilibrium_restrictions(
    result: IdentificationResult,
) -> EquilibriumRestrictions:
    """Pass identified quantities into U6 without asserting uniqueness."""
    if not any(result.identified):
        raise U56InterfaceError("at least one parameter must be identified")
    restrictions = tuple(
        estimate if is_identified else float("nan")
        for estimate, is_identified in zip(result.estimates, result.identified)
    )
    # Unidentified entries are represented by absent restrictions, not NaN.
    restrictions = tuple(v for v, ok in zip(restrictions, result.identified) if ok)
    names = tuple(name for name, ok in zip(result.parameter_names, result.identified) if ok)
    uncertainty = tuple(v for v, ok in zip(result.uncertainty, result.identified) if ok)
    return EquilibriumRestrictions(names, restrictions, uncertainty, result.provenance, False)


def validate_no_uniqueness_inference(
    restrictions: EquilibriumRestrictions,
) -> None:
    """Ensure an identification hand-off has not been mislabeled as unique."""
    if restrictions.uniqueness_certified:
        raise U56InterfaceError(
            "U5 identification cannot certify U6 mathematical uniqueness"
        )


__all__ = [
    "IdentificationResult",
    "EquilibriumRestrictions",
    "U56InterfaceError",
    "build_identification_result",
    "identification_to_equilibrium_restrictions",
    "validate_no_uniqueness_inference",
]
