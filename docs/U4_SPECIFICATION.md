# U4 — Stress Testing and Robustness

## Purpose

U4 tests the reduced-form three-Republic political-financial-security system under explicit deterministic shocks. It is downstream of U2 closure and U3 welfare-warfare optimality.

The three Republics remain represented as three sovereign nodes. U4 does not assign empirical probabilities to shocks and does not claim that any scenario is politically desirable.

## 1. Shock channels

For Republic $i$, the baseline state is

$$X_i=(p_i,r_i,s_i,G_{m,i},Y_i).$$

U4 applies additive shocks through four channels:

$$\Delta r_i,\qquad \Delta p_i,\qquad \Delta s_i,\qquad \Delta E_i.$$

The shocked security state is therefore

$$s_i'=s_i+\Delta s_i+\Delta E_i,$$

while political and financial states satisfy

$$p_i'=p_i+\Delta p_i,$$

$$r_i'=r_i+\Delta r_i.$$

Defense expenditure and output are held fixed in this reduced-form stress layer so that the shock response can be isolated.

## 2. Feasibility

The U3 resource identity remains

$$C_i=Y_i-G_{m,i}.$$

A stressed state is resource-feasible only when

$$Y_i-G_{m,i}>0\quad\forall i.$$

The implementation reports the minimum civilian-resource margin across the three Republics.

## 3. Local stability certificate

Given a supplied upper bound $b$ on the infinity norm of the relevant local Jacobian,

$$b\geq\|J\|_\infty,$$

U4 defines the conservative stability margin

$$m_s=1-b.$$

Thus

$$m_s>0$$

is a sufficient contraction certificate. It is not a claim of global stability.

## 4. Robustness criterion

A scenario is classified as robust only when both conditions hold:

$$Y_i-G_{m,i}>0\quad\forall i,$$

and

$$m_s>0.$$

The kernel also reports the political-financial state deviation

$$\Delta X=(\Delta p_G,\Delta p_I,\Delta p_T,\Delta r_G,\Delta r_I,\Delta r_T).$$

## 5. Deterministic shock grid

The default grid uses one-channel shocks at levels $\{-1,0,1\}$ for each of the four channels, producing 12 reproducible scenarios. This is a verification grid, not an empirical probability distribution.

## 6. Verification boundary

Passing U4 establishes deterministic feasibility and a conservative local-stability certificate for the specified stress scenarios. It does not establish empirical shock probabilities, global stability, strategic equilibrium under arbitrary deviations, or political legitimacy. Those claims require downstream analysis.
