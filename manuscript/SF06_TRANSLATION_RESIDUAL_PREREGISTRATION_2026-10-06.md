# SF06 pollination→female-fitness translation-residual reanalysis — preregistration 2026-10-06

## Status

Prospectively specified **before opening or storing the row-level Hedges-d outcome cells** from Aguilar et al. (2024 online / 2025 volume), Supplementary Table S1 (doi:10.1093/aob/mcae076).

The source paper and its aggregate results are known: land-use effects on pollination and female fitness are positively correlated, and compatibility system moderates marginal average effects. EGWEE has already materialized the source publication/species/trait universe while deliberately excluding `Hedges' d` and `V(d)` cells.

This route asks a different question from the source paper and from the frozen EGWEE 16-programme translation map.

## Biological question

> **At the same observed pollination response to land-use change, does plant compatibility system predict the downstream female-fitness response?**

The hypothesis generated from the EGWEE translation analysis is that reproductive assurance can change the conversion from pollination damage to female fitness. A broad self-compatible (SC) label is an imperfect proxy for effective assurance, but the SF06 database provides enough coverage for a first independent external test.

## Source

Fixed public source:

- Aguilar et al., *Annals of Botany*, doi:10.1093/aob/mcae076;
- public Supplementary Table S1;
- source file hash must match or be recorded by the analysis workflow;
- no alternative dataset is substituted after outcomes are opened.

## Pair construction

Rows are parsed exactly from Supplementary Table S1.

Primary paired unit:

`source publication × plant species × land-use factor`.

A unit is eligible only when it contains both:

- `Pollination`; and
- `Female fitness`.

Primary exposure restriction:

- `land_use_factor`, after case/whitespace normalization, must equal `habitat fragmentation`.

Male-fitness rows are excluded from this analysis.

If more than one row exists for one response inside the same paired unit, rows are combined **within response** by inverse-variance fixed-effect weighting before I–F pairing. No outcome-based endpoint selection is allowed.

Compatibility is taken only from the source metadata:

- `SI` = self-incompatible;
- `SC` = self-compatible;
- `NA` / undetermined is retained descriptively but excluded from the primary compatibility coefficient.

## Primary estimand

Let:

- `d_I` = source Hedges d for pollination;
- `d_F` = source Hedges d for female fitness.

The source orientation is retained: negative values mean lower pollination or fitness under anthropogenic land-use change.

Primary model:

`d_F = alpha + beta * d_I + gamma * SC + error`

with equal weight per paired unit and **publication-cluster-robust** standard errors.

Primary coefficient:

`gamma_SC`.

Directional prediction:

`gamma_SC > 0`.

Interpretation: for the same observed pollination response, self-compatible plants retain higher / less-negative female fitness than self-incompatible plants.

The reported primary inference is the two-sided cluster-robust p-value and 95% CI. The directional prediction is evaluated by coefficient sign; no one-sided p-value is used as the headline.

## Secondary estimands

1. Pair difference:
   `Delta = d_F - d_I`.
   Negative Delta means female fitness is more negatively affected than pollination on the source Hedges-d representation.

2. Cluster-robust model:
   `Delta = alpha + gamma_delta * SC + error`.

3. Interaction sensitivity:
   `d_F = alpha + beta*d_I + gamma*SC + theta*(d_I*SC) + error`.

4. Sign-topology census by compatibility:
   - false reassurance point geometry: `d_I >= 0, d_F < 0`;
   - apparent over-warning/buffering point geometry: `d_I < 0, d_F >= 0`;
   - concordant deterioration: `d_I < 0, d_F < 0`;
   - concordant non-deterioration: otherwise.

These topology counts are descriptive and not prevalence estimates.

## Sensitivities

- all eligible land-use factors, without the habitat-fragmentation-only restriction;
- inverse-variance weighted Delta regression using `V_F + V_I` as a zero-covariance working variance;
- publication-balanced summary in which each publication contributes equally within compatibility class.

Unknown within-pair covariance is **not** estimated from outcomes and is not silently assumed known. The unweighted cluster-robust primary model avoids using a fabricated I–F sampling covariance.

## Decision rules

Support for the proposed compatibility translation modifier requires:

1. `gamma_SC > 0`; and
2. its 95% cluster-robust CI excludes zero in the primary habitat-fragmentation subset.

If the sign is positive but the interval includes zero, classify as `directionally_consistent_unresolved`.

If the sign is zero/negative, classify as `compatibility_translation_prediction_not_supported`.

No result can establish "effective reproductive assurance" because SF06 records compatibility, not experimentally measured viable assurance.

## Claim ceiling

Allowed if supported:

- compatibility system explains residual pollination→female-fitness translation in this external source database;
- this provides external evidence that average pollination damage does not uniquely determine female-fitness damage.

Not allowed:

- compatibility is the universal mechanism of EGWEE false reassurance;
- SC equals effective reproductive assurance;
- the source Hedges-d residual is effect-scale invariant;
- the reanalysis changes the frozen EGWEE 16-programme denominator;
- individual SF06 rows are independent when they share a publication.

## Independence from the source paper's published question

Aguilar et al. test compatibility as a moderator of the **marginal average effect** on pollination and on female fitness separately and report a positive overall pollination–female-fitness association.

This preregistration instead tests whether compatibility explains the **residual translation between the two responses within paired source units**.


## Pre-outcome amendment: scale-stable external topology

This amendment was frozen **before any row-level Hedges-d outcome cells or generated SF06 pair/result files were stored in EGWEE**. It does not replace the compatibility model above. It separates the external test into a scale-stable generality lane and a scale-dependent mechanistic lane.

### Primary external-generality target

The main external generality question is now:

> **Among species/studies that measured pollination and female fitness under the same land-use contrast, does the sign of the pollination response deterministically identify the sign of the female-fitness response?**

For the **scale-stable primary topology**, response sign is defined from the constituent source rows *before* inverse-variance aggregation:

- `lower` only when **all** constituent effects for that response are negative;
- `nonlower` only when **all** constituent effects are zero or positive;
- `mixed` when constituent effects span both sides of zero.

A paired unit enters the scale-stable topology only when both I and F have consensus signs. This is deliberately stricter than using the sign of an inverse-variance weighted Hedges-d summary. Standardization by a positive SD cannot reverse each constituent mean-contrast sign, whereas changing effect representation can change relative weights and could in principle reverse the sign of an aggregated summary.

For the habitat-fragmentation subset, calculate the **best deterministic lookup** from consensus `I_sign` to consensus `F_sign`. For each observed I-sign state, choose the F-sign state that minimizes mismatches. Sum the remaining mismatches across I-sign states.

The sign of the inverse-variance weighted Hedges-d summaries is retained only as a **representation-specific sensitivity**, not as the scale-stable primary topology.

This is a structural compatibility diagnostic, not an out-of-sample error rate.

### Primary decision rule

Classify the external SF06 sign map as `external_sign_translation_nonidentifiability_supported` only when:

1. the habitat-fragmentation consensus-sign subset passes a **minimum coverage gate of at least 10 paired units from at least 5 source publications**;
2. the full habitat-fragmentation **consensus-sign** paired set has at least one deterministic mismatch; and
3. after deleting every whole source publication in turn, the best deterministic consensus I-sign→F-sign lookup still has at least one mismatch.

The minimum coverage gate is fixed before outcome opening to prevent a sparse consensus subset from being promoted as broad external generality. The source paper reports 82 species with simultaneous pollination and female-fitness effects before this stricter consensus filtering; the gate does not assume how many will remain.

If the full map is non-identifying but at least one publication deletion removes all mismatches, classify as influence-sensitive.

### Conservative uncertainty sensitivity

For each endpoint separately, call a sign **resolved lower** only when the 95% marginal interval `d ± 1.96*sqrt(V)` lies below zero, and **resolved nonlower** only when the interval lies above zero. Pairs with either unresolved endpoint are excluded from this sensitivity.

The resolved-only topology is descriptive unless enough pairs remain; it is not required for the primary structural decision because marginal non-resolution does not make a point estimate equal to zero.

### Compatibility remains a secondary mechanism test

The preregistered model

`d_F = alpha + beta*d_I + gamma*SC + error`

remains unchanged as a **representation-specific mechanistic test**. A positive `gamma_SC` can support compatibility as one translation modifier on the source Hedges-d scale, but it is not used to establish the scale-stable external generality claim.

Thus the evidence hierarchy is:

1. **scale-stable external generality:** sign-level I→F non-identifiability;
2. **scale-dependent mechanism probe:** compatibility residual on source Hedges d.

Neither lane estimates the prevalence of false reassurance in nature.
