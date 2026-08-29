"""U2 political-financial-security closure kernel.

The kernel formalizes the coupled system described in
"Three Republics, One Equilibrium Point": political state p depends on
financial/security state, financial state r depends on political/security
state, and security is produced from defense expenditure and cooperation.

This is deliberately a deterministic abstract kernel. It does not encode
country-specific empirical estimates or political preferences.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class U2Parameters:
    """Linearized coupling parameters for the three-Republic system."""

    phi: tuple[tuple[float, ...], ...]
    psi: tuple[tuple[float, ...], ...]
    omega: tuple[tuple[float, ...], ...]
    gamma: tuple[tuple[float, ...], ...]
    baseline_p: tuple[float, ...]
    baseline_r: tuple[float, ...]
    baseline_s: tuple[float, ...]


def _matvec(matrix: tuple[tuple[float, ...], ...], vector: tuple[float, ...]) -> tuple[float, ...]:
    if not matrix or any(len(row) != len(vector) for row in matrix):
        raise ValueError("matrix/vector dimensions are incompatible")
    return tuple(sum(a * b for a, b in zip(row, vector)) for row in matrix)


def _add(*vectors: tuple[float, ...]) -> tuple[float, ...]:
    if not vectors:
        return ()
    if any(len(v) != len(vectors[0]) for v in vectors):
        raise ValueError("vectors must have equal dimension")
    return tuple(sum(v[i] for v in vectors) for i in range(len(vectors[0])))


def _sub(left: tuple[float, ...], right: tuple[float, ...]) -> tuple[float, ...]:
    if len(left) != len(right):
        raise ValueError("vectors must have equal dimension")
    return tuple(a - b for a, b in zip(left, right))


def political_map(r: tuple[float, ...], s: tuple[float, ...], params: U2Parameters) -> tuple[float, ...]:
    """Return p = Phi(r, s)."""
    return _add(params.baseline_p, _matvec(params.phi, r), _matvec(params.gamma, s))


def financial_map(p: tuple[float, ...], s: tuple[float, ...], params: U2Parameters) -> tuple[float, ...]:
    """Return r = Psi(p, s)."""
    return _add(params.baseline_r, _matvec(params.psi, p), _matvec(params.omega, s))


def security_map(r: tuple[float, ...], p: tuple[float, ...], defense: tuple[float, ...], params: U2Parameters) -> tuple[float, ...]:
    """Return a reduced-form security state.

    Defense expenditure and cross-Republic contributions enter through the
    supplied coupling matrix gamma. This preserves the treatise's principle
    that security depends on military expenditure and external contributions
    without asserting an empirical production function.
    """
    return _add(params.baseline_s, defense, _matvec(params.omega, r), _matvec(params.gamma, p))


def residual(
    r: tuple[float, ...],
    p: tuple[float, ...],
    s: tuple[float, ...],
    defense: tuple[float, ...],
    params: U2Parameters,
) -> tuple[float, ...]:
    """Return the stacked political, financial, and security fixed-point residual."""
    p_next = political_map(r, s, params)
    r_next = financial_map(p, s, params)
    s_next = security_map(r, p, defense, params)
    return _sub(_add(p_next, r_next, s_next), _add(p, r, s))


def sup_norm(vector: tuple[float, ...]) -> float:
    """Infinity norm."""
    return max((abs(x) for x in vector), default=0.0)


def jacobian_fd(function, x: tuple[float, ...], step: float = 1e-6) -> tuple[tuple[float, ...], ...]:
    """Central finite-difference Jacobian for deterministic local stability checks."""
    if step <= 0 or not isfinite(step):
        raise ValueError("step must be finite and positive")
    base = function(x)
    columns = []
    for j in range(len(x)):
        plus = list(x)
        minus = list(x)
        plus[j] += step
        minus[j] -= step
        fp = function(tuple(plus))
        fm = function(tuple(minus))
        columns.append(tuple((a - b) / (2.0 * step) for a, b in zip(fp, fm)))
    return tuple(tuple(columns[j][i] for j in range(len(x))) for i in range(len(base)))


def default_parameters(n: int = 3) -> U2Parameters:
    """Return a conservative symmetric three-Republic calibration."""
    if n != 3:
        raise ValueError("U2 currently requires exactly three Republics")
    eye = tuple(tuple(1.0 if i == j else 0.0 for j in range(n)) for i in range(n))
    coupling = tuple(tuple(0.1 if i != j else 0.2 for j in range(n)) for i in range(n))
    zero = tuple(tuple(0.0 for _ in range(n)) for _ in range(n))
    return U2Parameters(
        phi=coupling,
        psi=coupling,
        omega=zero,
        gamma=zero,
        baseline_p=(0.0,) * n,
        baseline_r=(0.0,) * n,
        baseline_s=(0.0,) * n,
    )


def validate_state(*states: tuple[float, ...]) -> None:
    """Reject non-finite state values."""
    for state in states:
        if not all(isfinite(x) for x in state):
            raise ValueError("state contains a non-finite value")
