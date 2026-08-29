"""U7 deterministic end-to-end validation for the U1--U6 stack."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Any, Callable, Mapping, Sequence


@dataclass(frozen=True)
class U7Result:
    outputs: Mapping[str, Any]
    digest: str


def _freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return tuple(sorted((str(k), _freeze(v)) for k, v in value.items()))
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(v) for v in value)
    if isinstance(value, float):
        return format(value, ".17g")
    return value


def stable_digest(value: Any) -> str:
    return sha256(repr(_freeze(value)).encode("utf-8")).hexdigest()


def validate_stage_contract(name: str, output: Any, validator: Callable[[Any], bool]) -> None:
    if not name or not isinstance(name, str):
        raise ValueError("stage name must be non-empty")
    if not validator(output):
        raise ValueError(f"stage contract failed: {name}")


def run_pipeline(stages: Sequence[tuple[str, Callable[[Any], Any], Callable[[Any], bool]]], initial_state: Any) -> U7Result:
    if not stages:
        raise ValueError("stages must be non-empty")
    state = initial_state
    outputs = {}
    for name, transform, validator in stages:
        state = transform(state)
        validate_stage_contract(name, state, validator)
        outputs[name] = state
    return U7Result(outputs=outputs, digest=stable_digest(outputs))


def assert_deterministic(
    stages: Sequence[tuple[str, Callable[[Any], Any], Callable[[Any], bool]]],
    initial_state: Any,
) -> U7Result:
    first = run_pipeline(stages, initial_state)
    second = run_pipeline(stages, initial_state)
    if first.digest != second.digest or _freeze(first.outputs) != _freeze(second.outputs):
        raise AssertionError("U7 pipeline is not deterministic")
    return first
