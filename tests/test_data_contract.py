import pytest
from src.data_contract import Observation, require_common_date, validate_observations


def row(country="Greece", date="2026-07-31", maturity=3.0):
    return Observation(country, date, maturity, 0.03, "official", "benchmark_yield", "annual")


def test_validation_sorts_maturities():
    rows = validate_observations([row(maturity=10.0), row(maturity=3.0)])
    assert [x.maturity_years for x in rows] == [3.0, 10.0]


def test_duplicate_maturity_rejected():
    with pytest.raises(ValueError):
        validate_observations([row(), row()])


def test_common_date_required():
    italy = [row(country="Italy", date="2026-08-01")]
    with pytest.raises(ValueError):
        require_common_date([row()], italy)


def test_common_date_returned():
    italy = [row(country="Italy")]
    assert require_common_date([row()], italy) == "2026-07-31"
