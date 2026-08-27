"""Country-level orchestration without fabricated source observations."""
from .data_contract import Observation, validate_observations
from .fit import fit_nss


def estimate_country_curve(observations, tau1_grid, tau2_grid):
    rows = validate_observations(observations)
    maturities = [row.maturity_years for row in rows]
    yields = [row.yield_decimal for row in rows]
    return fit_nss(maturities, yields, tau1_grid, tau2_grid)


def estimate_pair(greece, italy, tau1_grid, tau2_grid):
    from .data_contract import require_common_date
    require_common_date(greece, italy)
    return {
        "Greece": estimate_country_curve(greece, tau1_grid, tau2_grid),
        "Italy": estimate_country_curve(italy, tau1_grid, tau2_grid),
    }


def source_observation(**kwargs):
    """Construct an explicit observation; callers must provide source metadata."""
    return Observation(**kwargs)
