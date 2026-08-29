# U2: Political-Financial-Security Closure

## Purpose

U2 extends the U1 algebraic closure kernel into a coupled three-Republic political-financial-security system for Greece, India, and Italy.

The source architecture specifies a political-financial fixed point

$$p^*=\Phi(r^*),\qquad r^*=\Psi(p^*)$$

and therefore

$$r^*=(\Psi\circ\Phi)(r^*).$$

U2 adds warfare economics as an endogenous security layer rather than treating security as an exogenous afterthought.

## State

For Republic $i\in\{G,I,T\}$, define the reduced state

$$x_i=(r_i,p_i,s_i,g_i),$$

where $r_i$ is the financial state, $p_i$ the political state, $s_i$ the security state, and $g_i$ defense expenditure.

The complete state is $X=(r,p,s,g)$.

## Coupled maps

The computational kernel represents

$$p^*=\Phi(r^*,s^*),$$

$$r^*=\Psi(p^*,s^*),$$

and

$$s^*=\Omega(r^*,p^*,g^*).$$

Defense expenditure is endogenous through a policy rule

$$g^*=\Gamma(r^*,p^*,s^*).$$

The implementation is deliberately reduced-form at U2. It does not claim empirical estimates for the three Republics.

## Warfare-economics layer

The supporting warfare-economics framework treats military capability as a resource-allocation problem and specifies military production, security production, budget constraints, and opportunity costs. In particular,

$$M=A K^\alpha L^\beta T^\gamma,$$

and

$$C+G_m=Y,$$

with security produced as

$$S=f(G_m,T,E).$$

U2 therefore treats defense expenditure and external security contributions as economically relevant state variables.

## Closure criterion

A candidate equilibrium $X^*$ must satisfy

$$\|F(X^*)-X^*\|_\infty<\varepsilon,$$

with all state variables finite and within their declared admissible domains.

Local stability is assessed using the Jacobian of the composite transition map. A sufficient local condition is

$$\rho(DF(X^*))<1.$$

A numerical fixed point is not interpreted as proof of global uniqueness or political legitimacy.

## Sovereignty constraint

The U2 kernel contains exactly three sovereign nodes. Differentiation in financial, political, or security variables does not imply political subordination. The model tests compatibility of sovereign states under a common equilibrium condition; it does not prescribe constitutional union.

## Validation sequence

1. deterministic kernel tests;
2. three-Republic dimensionality tests;
3. fixed-point residual tests;
4. finite-state tests;
5. local-Jacobian reproducibility tests;
6. full repository regression suite;
7. reproducibility CI;
8. empirical calibration only after the abstract closure kernel is validated.
