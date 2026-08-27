"""Validation and normalization for sovereign yield cross-sections."""
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Observation:
    country: str
    valuation_date: str
    maturity_years: float
    yield_decimal: float
    source: str
    yield_type: str
    compounding: str


def validate_observations(observations: Iterable[Observation]) -> list[Observation]:
    rows = list(observations)
    if not rows:
        raise ValueError("at least one observation is required")
    countries = {row.country for row in rows}
    dates = {row.valuation_date for row in rows}
    if len(countries) != 1 or len(dates) != 1:
        raise ValueError("each cross-section must contain one country and valuation date")
    maturities = [row.maturity_years for row in rows]
    if any(m <= 0 for m in maturities) or len(set(maturities)) != len(maturities):
        raise ValueError("maturities must be positive and unique")
    if any(not (-0.99 < row.yield_decimal < 10.0) for row in rows):
        raise ValueError("yield outside admissible numeric range")
    return sorted(rows, key=lambda row: row.maturity_years)


def require_common_date(greece: Iterable[Observation], italy: Iterable[Observation]) -> str:
    gr = validate_observations(greece)
    it = validate_observations(italy)
    if gr[0].valuation_date != it[0].valuation_date:
        raise ValueError("Greece and Italy must share a valuation date")
    return gr[0].valuation_date
