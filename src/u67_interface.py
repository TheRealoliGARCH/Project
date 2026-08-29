"""Canonical U6 -> U7 uniqueness-certificate interface."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Sequence, Tuple


class U67InterfaceError(ValueError):
    """Raised when the U6 -> U7 contract is violated."""


Vector = Tuple[float, ...]


@dataclass(frozen=True)
class UniquenessCertificate:
    """U6 certificate carried into U7 without weakening its semantics."""

    equilibrium: Vector
    jacobian_bound: float
    domain_lower: Vector
    domain_upper: Vector
    certified: bool
    provenance: str


def _vector(values: Sequence[float], name: str) -> Vector:
    result = tuple(float(v) for v in values)
    if not result:
        raise U67InterfaceError(f"{name} must be non-empty")
    if not all(isfinite(v) for v in result):
        raise U67InterfaceError(f"{name} must contain only finite values")
    return result


def build_uniqueness_certificate(
    equilibrium: Sequence[float],
    jacobian_bound: float,
    domain_lower: Sequence[float],
    domain_upper: Sequence[float],
    *,
    certified: bool,
    provenance: str,
) -> UniquenessCertificate:
    x = _vector(equilibrium, "equilibrium")
    lower = _vector(domain_lower, "domain_lower")
    upper = _vector(domain_upper, "domain_upper")
    if len(x) != len(lower) or len(x) != len(upper):
        raise U67InterfaceError("equilibrium and domain vectors must have equal lengths")
    bound = float(jacobian_bound)
    if not isfinite(bound) or bound < 0.0:
        raise U67InterfaceError("jacobian_bound must be finite and non-negative")
    if any(lo > hi for lo, hi in zip(lower, upper)):
        raise U67InterfaceError("domain lower bound cannot exceed upper bound")
    if any(v < lo or v > hi for v, lo, hi in zip(x, lower, upper)):
        raise U67InterfaceError("equilibrium must lie inside the admissible domain")
    if not provenance:
        raise U67InterfaceError("provenance must be non-empty")
    if certified and not bound < 1.0:
        raise U67InterfaceError("certified uniqueness requires jacobian_bound < 1")
    return UniquenessCertificate(x, bound, lower, upper, bool(certified), provenance)


def validate_u7_certificate(certificate: UniquenessCertificate) -> None:
    """Validate that U7 receives a genuine, non-ambiguous U6 certificate."""
    if not certificate.certified:
        raise U67InterfaceError("U7 integration requires a certified U6 uniqueness result")
    if not certificate.jacobian_bound < 1.0:
        raise U67InterfaceError("U6 certificate does not establish contraction")
    if not certificate.provenance:
        raise U67InterfaceError("certificate provenance is required")


__all__ = ["UniquenessCertificate", "U67InterfaceError", "build_uniqueness_certificate", "validate_u7_certificate"]
