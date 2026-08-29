"""Observation operator and recoverability contract for the U7 output layer."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Sequence, Tuple


class ObservationalRecoverabilityError(ValueError):
    """Raised when an observation/recoverability contract is violated."""


Vector = Tuple[float, ...]


@dataclass(frozen=True)
class ObservationMap:
    """A deterministic observation operator y = H(x)."""

    source_indices: Tuple[int, ...]

    def apply(self, state: Sequence[float]) -> Vector:
        x = _vector(state, "state")
        if any(i < 0 or i >= len(x) for i in self.source_indices):
            raise ObservationalRecoverabilityError("observation index outside state")
        return tuple(x[i] for i in self.source_indices)


@dataclass(frozen=True)
class RecoverabilityResult:
    """Result of comparing two latent states through the observation operator."""

    observations_equal: bool
    latent_states_equal: bool
    identifiable: bool


def _vector(values: Sequence[float], name: str) -> Vector:
    result = tuple(float(v) for v in values)
    if not result:
        raise ObservationalRecoverabilityError(f"{name} must be non-empty")
    if not all(isfinite(v) for v in result):
        raise ObservationalRecoverabilityError(f"{name} must contain only finite values")
    return result


def build_observation_map(source_indices: Sequence[int]) -> ObservationMap:
    indices = tuple(int(i) for i in source_indices)
    if not indices:
        raise ObservationalRecoverabilityError("source_indices must be non-empty")
    if any(i < 0 for i in indices):
        raise ObservationalRecoverabilityError("source_indices must be non-negative")
    if len(set(indices)) != len(indices):
        raise ObservationalRecoverabilityError("source_indices must be unique")
    return ObservationMap(indices)


def assess_recoverability(
    observation_map: ObservationMap,
    state_a: Sequence[float],
    state_b: Sequence[float],
    *,
    tolerance: float = 1e-12,
) -> RecoverabilityResult:
    """Check observational equivalence and whether it distinguishes two states."""
    a = _vector(state_a, "state_a")
    b = _vector(state_b, "state_b")
    if len(a) != len(b):
        raise ObservationalRecoverabilityError("latent states must have equal dimensions")
    obs_a = observation_map.apply(a)
    obs_b = observation_map.apply(b)
    observations_equal = all(abs(x - y) <= tolerance for x, y in zip(obs_a, obs_b))
    latent_states_equal = all(abs(x - y) <= tolerance for x, y in zip(a, b))
    return RecoverabilityResult(
        observations_equal=observations_equal,
        latent_states_equal=latent_states_equal,
        identifiable=not observations_equal or latent_states_equal,
    )


def require_recoverability(
    observation_map: ObservationMap,
    state: Sequence[float],
    *,
    reference_state: Sequence[float] | None = None,
) -> Vector:
    """Return observations and reject an observationally ambiguous reference."""
    observation = observation_map.apply(state)
    if reference_state is not None:
        result = assess_recoverability(observation_map, state, reference_state)
        if result.observations_equal and not result.latent_states_equal:
            raise ObservationalRecoverabilityError(
                "distinct latent states are observationally equivalent"
            )
    return observation


__all__ = [
    "ObservationMap",
    "ObservationalRecoverabilityError",
    "RecoverabilityResult",
    "assess_recoverability",
    "build_observation_map",
    "require_recoverability",
]
