# Interaction–function sign uncertainty audit — 2026-10-01

## Why this audit

The scale audit established that the **sign** of a positive-valued direct fragmented/reference effect is invariant to switching between Hedges g and lnRR. That does not mean the sign itself is estimated precisely.

The current I–F sign-geometry census classifies panels by the signs of point estimates. We therefore asked a separate uncertainty question:

> **For the six panels with opposite I/F point-estimate signs, are both endpoint directions individually resolved away from zero?**

Endpoint direction was classified from the existing effect estimate and sampling variance using the same normal-approximation 95% interval used elsewhere in the evidence package: `effect ± 1.96 × SE`.

## Result

Across all 18 primary I–F panels:

- opposite-sign point estimates: **6**;
- opposite signs with **both endpoint directions resolved**: **0**;
- opposite signs with **one endpoint resolved and the other unresolved**: **2**;
- opposite signs with **both endpoint directions unresolved**: **4**.

The two one-sided-resolved cases are:

1. *Eucalyptus wandoo*: I point estimate positive but its 95% interval narrowly crosses zero; F is resolved negative.
2. Kakamega *Acanthopale pubescens*: I point estimate positive but unresolved; F is resolved negative.

The four both-unresolved opposite-sign panels are:

- Sevenello LARO;
- Sevenello POAR;
- Zurich *Onobrychis viciifolia*;
- Toronto common milkweed.

Thus **none of the six point-sign-discordant panels provides two individually resolved endpoint directions of opposite sign at the 95% level**.

## What this changes

The sign geometry remains a useful **descriptive point-estimate topology**, because direct-study signs do not change under g→lnRR re-expression and gradient signs remain on their registered Fisher-z scale.

But the stronger wording “resolved qualitative sign reversal” is not justified.

The main paper should distinguish:

### A. Stronger paired-difference evidence

Three independent programmes have a resolved I–F **difference** with F worse than I under their audited representations:

- *Eucalyptus wandoo*;
- *Cardiopetalum calophyllum*;
- Kakamega *Acanthopale pubescens* programme.

This does not require each marginal endpoint to be individually significant.

### B. Descriptive point-sign geometry

Six panels in five programmes have opposite **point-estimate** signs, but none has both marginal directions individually resolved. These panels are useful for hypothesis generation and for showing that point trajectories are heterogeneous; they are not proof of sign reversal.

## Consequence for the species-specific landscape claim

Three multi-panel programmes show more than one point-estimate sign geometry among focal species under one registered exposure frame. This is an interesting descriptive observation, but the species-specific sign categories themselves often have wide endpoint uncertainty.

The manuscript may therefore say:

> **Point-estimate interaction–function trajectories vary among focal plants sharing the same exposure frame.**

It should not say that species-specific opposite-sign responses are individually resolved in those programmes.

## Claim ceiling

Allowed:

- 6/18 panels have opposite I/F point-estimate signs;
- those six occur in five independent programmes;
- zero of those six have both endpoint directions individually resolved at 95%;
- Wandoo and Kakamega Acanthopale each have resolved negative F with an unresolved positive I point estimate;
- paired I–F difference evidence can be stronger than marginal sign resolution;
- point-estimate sign geometry is scale-stable with respect to g→lnRR sign for direct positive-valued endpoints.

Not allowed:

- “six resolved sign reversals”;
- “five programmes prove qualitative decoupling by sign”;
- treating a CI crossing zero as evidence of no response;
- treating endpoint marginal significance as equivalent to the paired I–F difference test;
- a prevalence estimate from the 18 dependent panels.

## Machine-readable implementation

- `evidence/meta_extraction/if_sign_uncertainty_v1.csv`
- `scripts/check_if_sign_uncertainty.py`
