# SF06 sign-topology monotonicity boundary — 2026-10-07

## Status

Logical consequence of the recorded public-S1 preliminary result plus the subsequently frozen stricter sign rule. This note does not use a new outcome model and does not rescue a preferred result.

## Inputs already exposed and retained

The first public-S1 execution used all **426 response-labelled physical rows** available in the accessible Supplementary Table S1 and produced:

- exact paired units: **59**;
- habitat-fragmentation paired units: **55**;
- best deterministic IVW-Hedges-d sign lookup: **0 mismatches**.

The later structural audit confirmed that the accessible DOCX itself contains those 426 physical rows. The current outcome-blind exact-pair manifest also contains **59** total pairs and **55** habitat-fragmentation pairs on the same public file.

## Current stricter topology rule

For each paired unit and response:

- retain `lower` only if every constituent source-row Hedges-d value is negative;
- retain `nonlower` only if every constituent source-row Hedges-d value is non-negative;
- exclude the response/pair from the scale-stable topology if constituent signs are mixed or missing.

The earlier preliminary topology classified the same pair universe using the sign of the inverse-variance weighted Hedges-d summary.

## Monotonicity argument

Inverse-variance weights are strictly positive.

Therefore, for any response whose constituent effects are all negative, its inverse-variance weighted summary must also be negative. Likewise, if all constituent effects are non-negative, the weighted summary must be non-negative.

Hence every pair retained by the stricter constituent-consensus rule has **the same I-sign and F-sign states that it had under the earlier IVW-sign rule**.

The stricter topology can only:

1. retain a pair with unchanged sign states; or
2. remove a mixed/missing-sign pair.

It cannot create a new I-sign → F-sign combination.

Because the earlier 55-pair habitat-fragmentation IVW-sign map had a deterministic lookup with **zero mismatches**, every subset produced by the stricter consensus rule must also have zero deterministic mismatches.

Whole-publication deletion and whole-species deletion are additional subset operations and likewise cannot create a mismatch.

## Consequence

For the accessible public-S1 universe:

> **sign-level pollination → female-fitness non-identifiability cannot be supported by the current stricter consensus-sign analysis.**

This conclusion does not require waiting for the current workflow to recompute the same topology. The rerun remains useful for:

- exact retained consensus-pair counts;
- resolved-95% sensitivity counts;
- non-overlap coverage bookkeeping;
- the representation-specific compatibility residual under the current strict numeric-eligibility rule.

But it cannot reverse the sign-topology decision from identifying to non-identifying.

## Ecological interpretation

This is directionally inconvenient but informative.

Aguilar et al. already report positive cross-species coupling between pollination and female-fitness effects (`r=0.421`, `n=82`). The public-S1 sign result strengthens the coarse-grained part of that picture: at literature/species-effect scale, the **direction** of female-fitness response appears recoverable from pollination direction in the paired public subset.

That does not imply quantitative sentinel sufficiency. A deterministic sign lookup says nothing about how strongly female fitness changes, and the published correlation is far from a one-to-one calibration.

The contrast with frozen EGWEE matched programmes therefore points to a grain distinction:

- **coarse cross-species literature scale:** pollination and female fitness can be directionally coupled;
- **matched programme/local-system scale:** identical interaction-quantity states can coexist with different reproductive-function states and large amplitude mismatches.

The defensible emerging question is no longer “is pollination direction globally non-identifying?” It is:

> **At what ecological and inferential grain does average pollination–fitness coupling cease to be sufficient for diagnosing local reproductive impairment?**

## Claim ceiling

Allowed:

- the accessible SF06 public-S1 subset cannot validate EGWEE sign-level non-identifiability;
- coarse sign coupling and local quantitative translation failure can coexist;
- the external negative result narrows EGWEE toward a grain/amplitude/sentinel-sufficiency question.

Not allowed:

- the public S1 proves universal sign determinism in nature;
- the 426-row public supplement represents all 500 hierarchical inputs used by Aguilar et al.;
- zero sign mismatches imply accurate quantitative prediction;
- the negative SF06 result invalidates the frozen within-programme EGWEE topology;
- grain dependence is established as a causal ecological law rather than an interpretation to test explicitly.
