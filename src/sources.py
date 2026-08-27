"""Source-specific normalization for official sovereign yield observations.

These adapters deliberately do not scrape or invent data. They convert explicitly
provided official records into the project's validated Observation schema while
preserving source metadata and requiring an explicit yield convention.
"""

from .data_contract import Observation, validate_observations

BANK_OF_GREECE = "Bank of Greece"
BANCA_D_ITALIA = "Banca d'Italia"


def _percent_to_decimal(value):
    return float(value) / 100.0


def _normalize(country, valuation_date, records, source, yield_type, compounding):
    observations = []
    for record in records:
        if "maturity_years" not in record or "yield_percent" not in record:
            raise ValueError("records require maturity_years and yield_percent")
        observations.append(
            Observation(
                country=country,
                valuation_date=valuation_date,
                maturity_years=float(record["maturity_years"]),
                yield_decimal=_percent_to_decimal(record["yield_percent"]),
                source=source,
                yield_type=yield_type,
                compounding=compounding,
            )
        )
    return validate_observations(observations)


def bank_of_greece_observations(
    valuation_date, records, *, source=BANK_OF_GREECE,
    yield_type="benchmark yield", compounding="source-reported"
):
    """Normalize explicitly supplied official Bank of Greece observations."""
    return _normalize(
        "Greece", valuation_date, records, source, yield_type, compounding
    )


def banca_d_italia_observations(
    valuation_date, records, *, source=BANCA_D_ITALIA,
    yield_type="benchmark yield", compounding="source-reported"
):
    """Normalize explicitly supplied official Banca d'Italia observations."""
    return _normalize(
        "Italy", valuation_date, records, source, yield_type, compounding
    )
