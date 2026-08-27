"""Deterministic parsers for documented Bank of Greece and Banca d'Italia rows."""
from __future__ import annotations

from typing import Iterable

from .sources import bank_of_greece_observations, banca_d_italia_observations


GREEK_MATURITIES = (3.0, 5.0, 7.0, 10.0, 15.0, 20.0, 30.0)
ITALIAN_BTP_MATURITIES = (3.0, 5.0, 10.0, 30.0)


def _number(value: str) -> float:
    value = value.strip().replace(" ", "")
    if value in {"", "-", "--", "n/a", "N/A"}:
        raise ValueError("missing numeric value")
    return float(value.replace(",", "."))


def _records(maturities, yields):
    return [
        {"maturity_years": maturity, "yield_percent": yield_percent}
        for maturity, yield_percent in zip(maturities, yields)
    ]


def parse_bank_of_greece_row(valuation_date: str, cells: Iterable[str], source: str):
    cells = list(cells)
    if len(cells) != 14:
        raise ValueError("Bank of Greece row must contain 14 price/yield cells")
    yields = []
    for index in range(0, 14, 2):
        _number(cells[index])
        yields.append(_number(cells[index + 1]))
    return bank_of_greece_observations(
        valuation_date,
        _records(GREEK_MATURITIES, yields),
        source=source,
    )


def parse_banca_d_italia_bmk0100_row(valuation_date: str, cells: Iterable[str], source: str):
    cells = list(cells)
    if len(cells) not in {4, 5}:
        raise ValueError("BMK0100 row must contain four BTP yields and optional CCT")
    yields = [_number(value) for value in cells[:4]]
    return banca_d_italia_observations(
        valuation_date,
        _records(ITALIAN_BTP_MATURITIES, yields),
        source=source,
    )
