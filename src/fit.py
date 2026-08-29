"""Dependency-free coarse NSS fitting by grid search plus linear least squares."""

from __future__ import annotations

from itertools import product
from typing import Sequence

from .nss import NSSParameters, loadings, spot_yield, rmse


def _solve_linear(a: list[list[float]], b: list[float]) -> list[float]:
    n = len(b)
    aug = [row[:] + [rhs] for row, rhs in zip(a, b)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot][col]) < 1e-14:
            raise ValueError("singular normal equations")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [x / scale for x in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            aug[row] = [x - factor * y for x, y in zip(aug[row], aug[col])]
    return [aug[i][-1] for i in range(n)]


def fit_nss_grid(
    maturities: Sequence[float],
    yields: Sequence[float],
    tau1_grid: Sequence[float],
    tau2_grid: Sequence[float],
) -> NSSParameters:
    """Fit NSS parameters by exhaustive tau grid and conditional OLS."""
    if len(maturities) != len(yields) or len(maturities) < 4:
        raise ValueError("need matching maturities/yields and at least four observations")
    best = None
    best_loss = float("inf")
    for tau1, tau2 in product(tau1_grid, tau2_grid):
        if tau1 <= 0 or tau2 <= 0 or tau1 == tau2:
            continue
        x = [loadings(m, tau1, tau2) for m in maturities]
        xtx = [[sum(row[i] * row[j] for row in x) for i in range(4)] for j in range(4)]
        xty = [sum(row[i] * y for row, y in zip(x, yields)) for i in range(4)]
        try:
            beta = _solve_linear(xtx, xty)
        except ValueError:
            continue
        p = NSSParameters(*beta, tau1, tau2)
        fitted = [spot_yield(m, p) for m in maturities]
        loss = rmse(yields, fitted)
        if loss < best_loss:
            best, best_loss = p, loss
    if best is None:
        raise ValueError("no admissible NSS solution on supplied grids")
    return best
