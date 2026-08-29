# U7: End-to-End Validation

## Purpose

U7 validates the integrated U1--U6 architecture as a deterministic pipeline. It verifies stage composition, explicit stage contracts, and reproducible reconstruction.

## Pipeline contract

For stages $S_1,\ldots,S_n$, starting from $x_0$,

$$
x_k=S_k(x_{k-1}).
$$

Every stage must satisfy its declared contract before the next stage executes.

## Deterministic reconstruction

For identical initial state and deterministic stage functions,

$$
\operatorname{Pipeline}(x_0)=\operatorname{Pipeline}(x_0).
$$

U7 records a SHA-256 digest of the complete ordered stage-output structure and compares repeated executions.

## Verification boundary

U7 establishes computational integration and deterministic reproducibility. It does not, by itself, establish empirical validity, causal identification, global uniqueness, or economic truth beyond the contracts inherited from U1--U6.

## Failure policy

A failed stage contract stops the pipeline. U7 must not silently coerce, skip, or repair an invalid intermediate state.
