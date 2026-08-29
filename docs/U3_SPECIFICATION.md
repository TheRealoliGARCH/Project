# U3 — Welfare-Warfare Optimality

## Purpose

U3 verifies the welfare and resource-allocation layer of the unified three-Republic system. It is downstream of U1 algebraic closure and U2 political-financial-security closure.

The implementation is deliberately reduced-form. It verifies mathematical conditions without asserting country-specific welfare preferences, defense technologies, or political legitimacy.

## 1. Resource constraint

For Republic $i$, output is allocated between civilian resources and military expenditure:

$$C_i + G_{m,i} = Y_i.$$

Hence

$$C_i = Y_i-G_{m,i},$$

with the admissible domain

$$0\leq G_{m,i}\leq Y_i,$$

and interior welfare calculations requiring $C_i>0$.

## 2. Security production

Security is represented generically as

$$S_i=f_i(G_{m,i},T_i,E_i),$$

where $T_i$ is threat and $E_i$ is external security contribution, including cooperative or alliance effects.

The executable kernel supplies a simple concave benchmark

$$S_i=1+A_iG_{m,i}^{\eta_i}+E_i-T_i,$$

for deterministic testing only. Empirical or structural security functions can be supplied through the same function interface.

## 3. Welfare

The benchmark social welfare function is

$$W_i=\alpha_i\ln C_i+(1-\alpha_i)\ln S_i,$$

where $0<\alpha_i<1$.

This represents the trade-off between civilian consumption and security identified in the warfare-economics framework.

## 4. First-order condition

For an interior optimum, the numerical implementation verifies

$$\frac{\partial W_i}{\partial G_{m,i}}=0.$$

For the welfare specification above this corresponds to

$$
\frac{\alpha_i}{C_i}
=
\frac{1-\alpha_i}{S_i}
\frac{\partial S_i}{\partial G_{m,i}}.
$$

The kernel reports the finite-difference FOC residual rather than treating numerical proximity as an exact identity.

## 5. Second-order condition

A strict local welfare maximum requires

$$\frac{\partial^2W_i}{\partial G_{m,i}^2}<0.$$

The test suite verifies this condition at an analytically known benchmark optimum.

## 6. Strategic allocation consistency

Strategic allocation is represented by non-negative weights $w_j$ satisfying

$$w_j\geq0,\qquad \sum_jw_j=1,$$

and a target-reproduction condition

$$\sum_jw_jX_j=P.$$

The kernel reports both the simplex residual and target residual. This permits later replacement of the benchmark allocation with the full active-set/KKT solution without changing the verification interface.

## 7. Cooperative security interpretation

External security contributions are endogenous candidates for later coupling to the U2 three-Republic system. The present U3 layer does not assume that cooperation is welfare-improving; it makes the channel explicit so that this proposition can be tested.

The warfare-economics source emphasizes that military spending creates opportunity costs while alliances and burden-sharing can generate economies of scale and enhanced security effectiveness. U3 therefore tests allocation consistency rather than imposing a presumption in favor of either militarization or demilitarization.

## 8. Verification boundary

Passing U3 establishes resource feasibility and local welfare/strategic optimality for the specified reduced-form system. It does not establish global optimality, empirical validity, political legitimacy, or strategic stability under arbitrary shocks. Those claims belong to later U4–U7 layers.
