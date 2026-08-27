"""Explicit transformations from documented benchmark yields to NSS model inputs."""
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class YieldTransformation:
    name: str
    description: str


def benchmark_yield_as_continuous_decimal(value: float) -> float:
    """Modeling convention: treat an already-decimal benchmark yield as continuous."""
    if value <= -1.0:
        raise ValueError("yield must exceed -100%")
    return value


BENCHMARK_AS_CONTINUOUS = YieldTransformation(
    name="benchmark_yield_as_continuous_decimal",
    description=(
        "Modeling convention only: documented benchmark yield-to-maturity decimals "
        "are supplied directly to the NSS objective as continuously compounded spot-yield proxies."
    ),
)


def transform_yields(values: Iterable[float]) -> list[float]:
    return [benchmark_yield_as_continuous_decimal(v) for v in values]
