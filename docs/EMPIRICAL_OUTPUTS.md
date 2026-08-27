# Empirical Outputs

The executable empirical pipeline produces NSS parameters and model-implied discount factors from the stored June 2025 benchmark-yield cross-sections.

## Required execution order

```text
python empirical/run_comparison.py
python empirical/plot_comparison.py
python -m unittest discover -s tests -v
```

## Output invariants

For each reported maturity `m`, the output stores:

`difference_gr_minus_it = greece_discount_factor - italy_discount_factor`.

The regression tests require positive country discount factors and exact agreement of the stored difference with the two stored factors to numerical precision.

## Interpretation

The plot compares NSS model-implied discount factors under the repository's declared benchmark-yield transformation convention. It must not be described as a direct observation of zero-coupon discount factors.
