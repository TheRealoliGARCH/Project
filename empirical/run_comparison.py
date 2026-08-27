"""Reproducible June 2025 Greece--Italy NSS comparison from project raw data."""
import csv
from pathlib import Path
from src.fit import fit_nss_grid
from src.nss import discount_factor, spot_yield, rmse
from src.transform import transform_yields, BENCHMARK_AS_CONTINUOUS

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw" / "2025-06"
OUT = ROOT / "results"
TAUS = [0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0, 15.0, 20.0, 30.0]
GRID = [i / 2 for i in range(1, 61)]


def read_country(filename):
    rows = []
    with (DATA / filename).open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            maturity = float(row["maturity_years"])
            yield_decimal = float(row["yield_percent"]) / 100.0
            rows.append((maturity, yield_decimal))
    rows.sort()
    return [m for m, _ in rows], transform_yields([y for _, y in rows])


def main():
    OUT.mkdir(exist_ok=True)
    datasets = {"Greece": "bank_of_greece_benchmark_yields.csv", "Italy": "banca_d_italia_bmk0100.csv"}
    fitted = {}
    diagnostics = []
    for country, filename in datasets.items():
        maturities, yields = read_country(filename)
        params = fit_nss_grid(maturities, yields, GRID, GRID)
        model = [spot_yield(m, params) for m in maturities]
        fitted[country] = params
        diagnostics.append([country, *params.__dict__.values(), rmse(yields, model)])
    with (OUT / "nss_parameters_2025-06.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["country", "beta0", "beta1", "beta2", "beta3", "tau1", "tau2", "rmse"])
        writer.writerows(diagnostics)
    with (OUT / "discount_factors_2025-06.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["maturity_years", "greece_discount_factor", "italy_discount_factor", "difference_gr_minus_it"])
        for m in TAUS:
            dg = discount_factor(m, fitted["Greece"])
            di = discount_factor(m, fitted["Italy"])
            writer.writerow([m, dg, di, dg - di])
    (OUT / "TRANSFORMATION_ASSUMPTION.txt").write_text(
        BENCHMARK_AS_CONTINUOUS.description + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
