"""Nelson--Siegel--Svensson yield and discount curve primitives."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(frozen=True)
class NSSParameters:
    beta0: float
    beta1: float
    beta2: float
    beta3: float
    tau1: float
    tau2: float

    def validate(self) -> None:
        if self.tau1 <= 0 or self.tau2 <= 0:
            raise ValueError("tau1 and tau2 must be strictly positive")


def _lambda(x: float) -> float:
    if x < 0:
        raise ValueError("maturity ratios must be non-negative")
    if abs(x) < 1e-8:
        return 1.0 - x / 2.0 + x * x / 6.0
    return -math.expm1(-x) / x


def loadings(maturity: float, tau1: float, tau2: float) -> tuple[float, float, float, float]:
    """Return the canonical NSS linear loadings for one maturity."""
    if maturity < 0:
        raise ValueError("maturity must be non-negative")
    if tau1 <= 0 or tau2 <= 0:
        raise ValueError("tau1 and tau2 must be strictly positive")
    x1 = maturity / tau1
    x2 = maturity / tau2
    l1 = _lambda(x1)
    l2 = _lambda(x2)
    return (1.0, l1, l1 - math.exp(-x1), l2 - math.exp(-x2))


def spot_yield(maturity: float, p: NSSParameters) -> float:
    """Continuously compounded NSS zero-coupon spot yield."""
    if maturity < 0:
        raise ValueError("maturity must be non-negative")
    p.validate()
    l0, l1, l2, l3 = loadings(maturity, p.tau1, p.tau2)
    return p.beta0 * l0 + p.beta1 * l1 + p.beta2 * l2 + p.beta3 * l3


def discount_factor(maturity: float, p: NSSParameters) -> float:
    """Discount factor exp(-maturity * continuously compounded spot yield)."""
    if maturity < 0:
        raise ValueError("maturity must be non-negative")
    return math.exp(-maturity * spot_yield(maturity, p))


def curve(maturities: Iterable[float], p: NSSParameters) -> list[float]:
    return [spot_yield(m, p) for m in maturities]


def discount_curve(maturities: Iterable[float], p: NSSParameters) -> list[float]:
    return [discount_factor(m, p) for m in maturities]


def rmse(observed: Sequence[float], fitted: Sequence[float]) -> float:
    if len(observed) != len(fitted) or not observed:
        raise ValueError("observed and fitted must have equal non-zero length")
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(observed, fitted)) / len(observed))
