"""Deterministic plotting for the Greece--Italy NSS discount-factor comparison."""
import csv
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
INPUT = RESULTS / "discount_factors_2025-06.csv"
OUTPUT = RESULTS / "greece_italy_discount_factors_2025-06.png"


def read_rows():
    with INPUT.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main():
    rows = read_rows()
    m = [float(r["maturity_years"]) for r in rows]
    gr = [float(r["greece_discount_factor"]) for r in rows]
    it = [float(r["italy_discount_factor"]) for r in rows]
    plt.figure(figsize=(8, 5))
    plt.plot(m, gr, label="Greece")
    plt.plot(m, it, label="Italy")
    plt.xlabel("Maturity (years)")
    plt.ylabel("NSS model-implied discount factor")
    plt.title("Greece and Italy Discount Factors, June 2025")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT, dpi=150)


if __name__ == "__main__":
    main()
