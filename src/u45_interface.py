"""Canonical U4 -> U5 causal-design interface.

A stress scenario is not itself a causal treatment. This module carries the
scenario assignment, potential outcomes, observed outcome, covariates, and
provenance explicitly so U5 cannot infer causal identification from a shock
alone.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Mapping, Sequence, Tuple

REPUBLICS = ("Greece", "India", "Italy")
Vector = Tuple[float, float, float]


class U45InterfaceError(ValueError):
    """Raised when a U4 -> U5 causal-design contract is violated."""


def _vector(values: Sequence[float], name: str) -> Vector:
    if len(values) != 3:
        raise U45InterfaceError(f"{name} must contain exactly three values")
    result = tuple(float(v) for v in values)
    if not all(isfinite(v) for v in result):
        raise U45InterfaceError(f"{name} must contain only finite values")
    return result  # type: ignore[return-value]


@dataclass(frozen=True)
class CausalDesign:
    """Explicit causal-design object passed from U4 to U5."""

    treatment: Vector
    outcome: Vector
    potential_outcome_0: Vector
    potential_outcome_1: Vector
    covariates: Tuple[Vector, ...]
    scenario_id: str
    treatment_assigned_by_design: bool
    exogeneity_assumed: bool
    provenance: str


def build_causal_design(
    treatment: Sequence[float],
    outcome: Sequence[float],
    potential_outcome_0: Sequence[float],
    potential_outcome_1: Sequence[float],
    *,
    scenario_id: str,
    treatment_assigned_by_design: bool,
    exogeneity_assumed: bool,
    provenance: str,
    covariates: Sequence[Sequence[float]] = (),
) -> CausalDesign:
    """Construct an explicit U5 causal-design input.

    The constructor records causal assumptions; it does not infer them from
    the fact that U4 generated a stress scenario.
    """
    if not scenario_id:
        raise U45InterfaceError("scenario_id must be non-empty")
    if not provenance:
        raise U45InterfaceError("provenance must be non-empty")
    return CausalDesign(
        treatment=_vector(treatment, "treatment"),
        outcome=_vector(outcome, "outcome"),
        potential_outcome_0=_vector(potential_outcome_0, "potential_outcome_0"),
        potential_outcome_1=_vector(potential_outcome_1, "potential_outcome_1"),
        covariates=tuple(_vector(c, "covariate") for c in covariates),
        scenario_id=scenario_id,
        treatment_assigned_by_design=bool(treatment_assigned_by_design),
        exogeneity_assumed=bool(exogeneity_assumed),
        provenance=provenance,
    )


def validate_causal_design(design: CausalDesign) -> None:
    """Reject designs that omit the information needed to interpret causality."""
    for name in ("treatment", "outcome", "potential_outcome_0", "potential_outcome_1"):
        _vector(getattr(design, name), name)
    if not design.scenario_id or not design.provenance:
        raise U45InterfaceError("causal design requires scenario_id and provenance")
    for covariate in design.covariates:
        _vector(covariate, "covariate")


__all__ = ["CausalDesign", "REPUBLICS", "U45InterfaceError", "build_causal_design", "validate_causal_design"]
