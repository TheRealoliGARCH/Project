# U6: Global Uniqueness

## Purpose

U6 strengthens the unified equilibrium result from existence or local stability to a sufficient condition for global uniqueness on an explicitly specified admissible domain.

## Fixed-point formulation

Let $T:\mathcal X\to\mathcal X$ be the complete equilibrium map. A fixed point satisfies

$$
T(x^*)=x^*.
$$

U6 does not infer global uniqueness from numerical convergence or local spectral stability.

## Contraction certificate

A sufficient condition for a unique fixed point on a complete invariant domain is

$$
\sup_{x\in\mathcal X}\|DT(x)\|_\infty < 1.
$$

The implementation exposes this as an explicit certificate. A bound equal to or above one is not certified as unique.

## Invariant domain

The map must remain inside the admissible domain. The executable invariant-box check is sample-based and therefore records computational evidence, not a proof of invariance for an uncountable domain.

## Jacobian validation

The supplied paper on two general conics gives

$$
J_{F,G}=2\begin{pmatrix}
ax+hy+f & hx+by+g\\
\alpha x+\eta y+\phi & \eta x+\beta y+\gamma
\end{pmatrix}.
$$

Its Jacobian symmetry condition is

$$
\alpha x+\eta y+\phi=hx+by+g.
$$

The factor $2$ in the Jacobian does not, by itself, imply that every Jacobian entry is divisible by $4$. Divisibility by $4$ additionally requires the corresponding linear forms to be even (for example, under an even-integer coefficient/parity specialization). U6 therefore tests the exact Jacobian formula directly and tests the stronger divisibility property only under an explicit parity specialization.

U6 uses these formulas as an algebraic Jacobian regression reference. The conic results themselves do not establish uniqueness of the Project equilibrium.

## Verification boundary

U6 establishes only sufficient computational certificates. Failure of the contraction test does not prove non-uniqueness; it means that this particular sufficient condition has not certified uniqueness.
