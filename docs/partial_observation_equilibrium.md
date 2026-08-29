# Partial-Observation Equilibrium and Financial Triangulation

## 1. Purpose

The unified sovereign political-financial framework should distinguish an equilibrium that exists mathematically from an equilibrium that can be identified from incomplete observations. This document extends the existing U1--U7 theory using the information-fusion structure developed in *The Theory of Financial Triangulation*.

Financial triangulation treats heterogeneous observations as evidence about a latent state and formalizes the problem as inference on a partially observed network. The source theory defines triangulation efficiency through entropy reduction and formulates Bayesian updating over competing source hypotheses. Those ideas are generalized here from source identification to sovereign equilibrium identification.

## 2. Latent state and observation operator

Let the latent sovereign state be

$$
X=(X_M,X_P,X_W,X_E,X_N),
$$

where the components may represent monetary, political, welfare-strategic, epistemic, and network states. Let

$$
S=(S_1,\ldots,S_n)
$$

be the observable information vector. The observation process is represented by

$$
S=\mathcal H(X)+\varepsilon,
$$

where $\mathcal H$ is the observation operator and $\varepsilon$ contains measurement and specification noise.

The observation operator is conceptually distinct from the equilibrium mapping. The same equilibrium restrictions can therefore admit states that are mathematically different but observationally indistinguishable.

## 3. Structural equilibrium versus observed equilibrium

Let

$$
\mathcal E_0
=
\mathcal A\cap\mathcal D\cap\mathcal W\cap\mathcal I
$$

be the structural equilibrium set inherited from the U1--U6 architecture. Introduce the observational restriction

$$
\mathcal O(S)
=
\{x:\;S\text{ is compatible with }\mathcal H(x)\}.
$$

The partially observed equilibrium set is then

$$
\boxed{
\mathcal E^\star(S)
=
\mathcal E_0\cap\mathcal O(S).
}
$$

Thus existence of a structural equilibrium does not imply observational recoverability of that equilibrium.

## 4. Observational equivalence

For a deterministic observation operator define

$$
[x]_{\mathcal H}
=
\{x'\in\mathcal E_0:\mathcal H(x')=\mathcal H(x)\}.
$$

This is the observational equivalence class of $x$. A state is observationally recoverable on $\mathcal E_0$ if and only if

$$
[x]_{\mathcal H}=\{x\}.
$$

The distinction gives three separate claims:

1. **Existence:** $\mathcal E^\star(S)\neq\varnothing$.
2. **Structural uniqueness:** $|\mathcal E_0|=1$ under the relevant admissibility domain.
3. **Observational uniqueness:** $|\mathcal E^\star(S)|=1$.

None of these implications should be asserted without the corresponding assumptions.

## 5. Bayesian formulation

Let $p(x)$ be a prior over admissible latent states and $p(S\mid x)$ the observation likelihood. Then

$$
p(x\mid S)
=
\frac{p(S\mid x)p(x)}{p(S)}.
$$

For competing equilibrium hypotheses $E_i$,

$$
P(E_i\mid S)
\propto
P(S\mid E_i)P(E_i).
$$

The maximum-posterior state is therefore

$$
X^*
=\arg\max_x p(x\mid S).
$$

This is an inference statement, not by itself a proof that the selected state is the unique structural equilibrium.

## 6. Epistemic uncertainty

Let $X$ be discrete for the entropy formulation. Define

$$
H(X)=-\sum_xp(x)\log p(x),
$$

and posterior uncertainty

$$
H(X\mid S).
$$

Define triangulation efficiency as

$$
\boxed{
\eta(S)=1-\frac{H(X\mid S)}{H(X)}
}
$$

when $H(X)>0$. Higher $\eta$ means greater reduction in uncertainty relative to the prior.

For continuous states, entropy should not be used naively; an appropriate continuous-state divergence, posterior concentration measure, or bounded uncertainty set should be specified instead.

## 7. Epistemic monotonicity

For any additional signal $T$, conditional mutual information gives

$$
I(X;T\mid S)\ge0.
$$

Since

$$
H(X\mid S,T)
=
H(X\mid S)-I(X;T\mid S),
$$

we obtain

$$
\boxed{
H(X\mid S,T)\le H(X\mid S).
}
$$

Therefore an additional signal cannot increase posterior uncertainty when the probability model is correctly specified. Equality occurs when the additional signal carries no conditional information about $X$.

This is the rigorous version of the triangulation principle. It does not imply that every additional variable improves practical identification: redundant, poorly measured, endogenous, or misspecified observations may add little usable information or invalidate the assumed likelihood.

## 8. Networked sovereign equilibrium

Represent the coupled sovereign-financial system by a time-varying graph

$$
G_t=(V_t,E_t).
$$

Nodes may represent sovereign, monetary, financial, fiscal, and strategic institutions. Edges encode economically or strategically meaningful dependencies. The latent object may therefore be written

$$
Z_t=(X_t,G_t).
$$

Observations can be node-level, edge-level, bilateral, or global. The observation operator becomes

$$
S_t=\mathcal H_t(X_t,G_t)+\varepsilon_t.
$$

For Greece, India, and Italy, the observation vector should distinguish country-specific signals from bilateral and common signals:

$$
S_t=(S_G,S_I,S_T,S_{GI},S_{GT},S_{IT},S_{\mathrm{global}}).
$$

This permits the theory to separate national conditions from common shocks and strategic interactions.

## 9. Observational recoverability

Define the posterior-compatible set at tolerance $\delta$ by

$$
\mathcal C_\delta(S)
=
\{x\in\mathcal E_0:\mathcal L(x;S)\ge\sup_{z\in\mathcal E_0}\mathcal L(z;S)-\delta\}.
$$

A sequence of increasingly informative observations provides observational recoverability if

$$
\operatorname{diam}(\mathcal C_{\delta_n}(S_n))\to0
$$

for a suitable sequence $\delta_n\to0$.

This criterion is deliberately stronger than merely obtaining a high posterior probability for one candidate. It asks whether competing admissible states are actually eliminated by the information set.

## 10. Identifiability condition

A sufficient local condition for deterministic observational identification is full column rank of the Jacobian

$$
D\mathcal H(x)
$$

on the relevant tangent space of the admissible equilibrium manifold. If the Jacobian is rank deficient, local observational equivalence may remain even when the structural equilibrium is unique.

Global identification requires a stronger injectivity condition:

$$
\mathcal H(x)=\mathcal H(x')
\quad\Longrightarrow\quad
x=x'
$$

for all $x,x'\in\mathcal E_0$.

## 11. Relationship to U1--U7

The strengthened interpretation is:

$$
\boxed{
U1\to U2\to U3\to U4\to U5\to U6\to U7
\to\text{observational recoverability}
}
$$

U1 establishes algebraic admissibility. U2--U4 impose political-financial, welfare-strategic, and dynamic restrictions. U5 addresses identification, U6 addresses global uniqueness, and U7 validates deterministic computational composition. The present extension supplies the missing observation-theoretic layer: whether the uniquely compatible structural state can be recovered from the information actually available.

This should not be interpreted as declaring a new U8 until its mathematical and empirical requirements have been separately specified and tested.

## 12. Three-Republic specialization

For Greece, India, and Italy, the natural empirical object is a joint latent state

$$
X=(X_G,X_I,X_T,X_{GI},X_{GT},X_{IT},X_C),
$$

where $X_C$ denotes common/global conditions. The corresponding observations should be partitioned in the same manner. The three-Republic model is then a coupled partially observed system rather than three independent country models.

The immediate empirical objective is to determine which components are recoverable from sovereign yield curves, discount factors, monetary and fiscal observables, and other admissible information, and which remain observationally equivalent.

## 13. Scope and evidentiary boundary

The Theory of Financial Triangulation motivates the entropy, Bayesian, heterogeneous-signal, and network components of this extension. It does not by itself establish the economic validity of the unified sovereign model, nor does it supply empirical identification for Greece, India, or Italy. Those claims require explicit data, likelihood specifications, identification tests, and reproducible computation.
