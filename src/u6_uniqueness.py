"""U6 global-uniqueness primitives.

U6 separates existence, local stability, and global uniqueness.  The primary
sufficient condition implemented here is contraction of a fixed-point map on a
specified admissible box.  Jacobian helpers provide an exact two-conic
reference calculation for algebraic derivative validation.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt
from typing import Callable, Sequence

Vector = Sequence[float]
Map = Callable[[Vector], Sequence[float]]


@dataclass(frozen=True)
class ContractionCertificate:
    bound: float
    unique_fixed_point: bool


def _finite_vector(values: Vector, name: str) -> None:
    if not values or not all(isfinite(x) for x in values):
        raise ValueError(f"{name} must be non-empty and finite")


def jacobian_two_conics(x: float, y: float, a: float, h: float, b: float,
                        f: float, g: float, alpha: float, eta: float,
                        beta: float, phi: float, gamma: float) -> tuple[tuple[float, float], tuple[float, float]]:
    values = (x, y, a, h, b, f, g, alpha, eta, beta, phi, gamma)
    if not all(isfinite(v) for v in values):
        raise ValueError("all conic parameters must be finite")
    return (
        (2.0 * (a * x + h * y + f), 2.0 * (h * x + b * y + g)),
        (2.0 * (alpha * x + eta * y + phi), 2.0 * (eta * x + beta * y + gamma)),
    )


def transpose(matrix: Sequence[Sequence[float]]) -> tuple[tuple[float, ...], ...]:
    if not matrix or not matrix[0]:
        raise ValueError("matrix must be non-empty")
    width = len(matrix[0])
    if any(len(row) != width for row in matrix):
        raise ValueError("matrix must be rectangular")
    return tuple(tuple(row[i] for row in matrix) for i in range(width))


def conic_jacobian_symmetry_condition(x: float, y: float, h: float, b: float,
                                      g: float, alpha: float, eta: float,
                                      phi: float) -> bool:
    lhs = alpha * x + eta * y + phi
    rhs = h * x + b * y + g
    return lhs == rhs


def numerical_jacobian(map_fn: Map, point: Vector, step: float = 1e-6) -> tuple[tuple[float, ...], ...]:
    _finite_vector(point, "point")
    if not isfinite(step) or step <= 0:
        raise ValueError("step must be positive and finite")
    base = tuple(map_fn(point))
    if len(base) != len(point) or not all(isfinite(v) for v in base):
        raise ValueError("map must return a finite vector of matching dimension")
    columns = []
    for j in range(len(point)):
        plus = list(point); minus = list(point)
        plus[j] += step; minus[j] -= step
        fp = tuple(map_fn(plus)); fm = tuple(map_fn(minus))
        if len(fp) != len(point) or len(fm) != len(point):
            raise ValueError("map dimension must remain fixed")
        columns.append(tuple((fp[i] - fm[i]) / (2.0 * step) for i in range(len(point))))
    return tuple(tuple(columns[j][i] for j in range(len(point))) for i in range(len(point)))


def infinity_norm(matrix: Sequence[Sequence[float]]) -> float:
    if not matrix or any(len(row) != len(matrix) for row in matrix):
        raise ValueError("matrix must be non-empty and square")
    return max(sum(abs(x) for x in row) for row in matrix)


def contraction_certificate(jacobian_bound: float) -> ContractionCertificate:
    if not isfinite(jacobian_bound) or jacobian_bound < 0:
        raise ValueError("Jacobian bound must be finite and non-negative")
    return ContractionCertificate(jacobian_bound, jacobian_bound < 1.0)


def fixed_point_residual(map_fn: Map, point: Vector) -> tuple[float, ...]:
    _finite_vector(point, "point")
    image = tuple(map_fn(point))
    if len(image) != len(point) or not all(isfinite(v) for v in image):
        raise ValueError("map must return a finite vector of matching dimension")
    return tuple(image[i] - point[i] for i in range(len(point)))


def invariant_box(map_fn: Map, lower: Vector, upper: Vector, samples: Sequence[Vector]) -> bool:
    _finite_vector(lower, "lower")
    _finite_vector(upper, "upper")
    if len(lower) != len(upper) or any(lo > hi for lo, hi in zip(lower, upper)):
        raise ValueError("invalid box")
    for point in samples:
        if len(point) != len(lower):
            raise ValueError("sample dimension mismatch")
        image = tuple(map_fn(point))
        if len(image) != len(lower) or any(not isfinite(v) for v in image):
            return False
        if any(v < lo or v > hi for v, lo, hi in zip(image, lower, upper)):
            return False
    return True
