# SF06 compatibility-translation sensitivity — 2026-10-07

## Question

Does nominal self-compatibility robustly explain the translation from pollination response to female-fitness response?

## Preregistered primary model

`d_F = alpha + beta*d_I + gamma_SC*SC` with publication-cluster-robust SE.

Corrected public-S1 fragmentation result:

- gamma_SC = **+0.0639**;
- 95% CI = **[-0.2627, +0.3905]**;
- p = **0.701**;
- decision = **directionally consistent but unresolved**.

Publication-balanced weighting keeps a positive coefficient:

- gamma_SC = **+0.1211**;
- 95% CI = [-0.2427, +0.4850].

## Secondary parameterizations

However, the sign is not stable across other declared representations of translation.

### Difference model

`Delta = d_F - d_I ~ SC`:

- gamma_SC = **-0.1751**;
- 95% CI = [-0.6312, +0.2810];
- p = 0.452.

### Interaction model

`d_F ~ d_I + SC + d_I×SC`: 

- SC main coefficient = **-0.0545**;
- interaction coefficient = **-0.2548**;
- both unresolved.

### Zero-covariance weighted Delta sensitivity

- gamma_SC = **-0.3837**;
- 95% CI = [-0.8263, +0.0589];
- p = 0.089.

## Source-publication-disjoint subset

The non-overlap primary coefficient is again positive but unresolved:

- gamma_SC = +0.1565;
- 95% CI = [-0.3298, +0.6429].

But the zero-covariance weighted Delta sensitivity is negative:

- gamma_SC = -0.5467;
- 95% CI = [-1.0093, -0.0842];
- p = 0.0205.

Because within-pair I–F sampling covariance is unknown, this weighted Delta sensitivity is not promoted over the preregistered unweighted cluster-robust primary model. Its role is to show that the biological modifier is not estimand-stable.

## Interpretation

Aguilar et al. show that self-incompatible species are more vulnerable on marginal average responses. That does **not** imply that compatibility explains how a given pollination effect translates into female fitness.

The corrected SF06 evidence therefore supports:

> **compatibility is a vulnerability correlate, but not a robustly identified translation modifier in this reanalysis.**

This is consistent with the broader mechanistic distinction between nominal self-compatibility and effective reproductive assurance.

## Claim ceiling

Do not claim:

- self-compatibility explains the external many-to-many topology;
- the positive primary gamma establishes buffering;
- the negative secondary coefficients establish the opposite mechanism.

The only supported mechanistic conclusion is that nominal compatibility does not robustly resolve translation heterogeneity.
