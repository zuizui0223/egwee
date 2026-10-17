# Interaction–function reliability sufficiency audit — 2026-10-06

## Question

Could the three representation-stable downstream interaction–function mismatches be generated simply because interaction endpoints are measured less reliably than reproductive function?

This audit addresses a measurement-artifact null. It does **not** test the prevalence of downstream mismatches across the full corpus.

## Why this matters

Standardized effects and correlations can be attenuated toward zero when the measured endpoint is noisy. If pollinator abundance, visitation or pollen quantity are substantially less reliable than fruit/seed output, an equal latent fragmentation response could appear as a weak I response and a strong F response.

The three resolved downstream anchors were therefore audited using source-level replication, standard errors or observation effort wherever recoverable.

## Wandoo

Source Table 6 reports population means, standard errors and sample sizes for pollen tubes and seeds per fruit.

Estimated population-mean reliabilities:

- interaction / pollen tubes: **R_I = 0.511**;
- reproductive function / seeds per fruit: **R_F = 0.856**;
- reliability ratio R_I/R_F = **0.597**.

The observed registered correlations have opposite signs (`r_I=+0.598`, `r_F=-0.704`). Correcting their magnitudes for the estimated reliabilities does not remove this opposition.

Under an equal-latent-effect attenuation model fitted with the registered sampling covariance:

- lack-of-fit chi-square(1) = **10.53**;
- descriptive misfit p = **0.00117**;
- probability of obtaining a downstream-resolved contrast under the fitted artifact null = **0.0117**.

Classical positive reliability attenuation cannot reverse the expected sign, so Wandoo is the strongest qualitative false-reassurance anchor.

## Cardiopetalum

Table 1 reports fragment-level means and SDs. The source sampled ten marked plants per fragment; pollinator abundance used multiple flowers on each of those plants.

Using SD/sqrt(10) for both endpoints gives:

- R_I = **0.822**;
- R_F = **0.820**;
- R_I/R_F = **1.003**.

To explain the observed correlation magnitudes (`r_I=-0.240`, `r_F=-0.933`) purely by reliability attenuation under an equal latent correlation would require approximately:

- required R_I/R_F = **0.0663**.

The observed proxy ratio is therefore about fifteen times larger than the reliability disparity required by the artifact explanation.

Under the fitted equal-latent-effect attenuation model:

- lack-of-fit chi-square(1) = **8.75**;
- descriptive misfit p = **0.00310**;
- downstream-resolved probability = **0.0247**.

## Kakamega Acanthopale

Visitation occurrence is reconstructed from site-level zero/non-zero observation counts, so binomial measurement error can be estimated directly.

- I reliability = **0.599**.

To favour the attenuation-artifact null as strongly as possible, F reliability is fixed to **1.0** rather than estimated from the reported within-site fruit-set SDs.

Thus:

- conservative R_I/R_F = **0.599**;
- reliability ratio required to explain the absolute g contrast = **0.0150**.

Even under this worst-case advantage for F reliability, the observed reliability ratio is roughly forty times larger than the attenuation ratio required.

Under the fitted equal-latent standardized-effect model:

- lack-of-fit chi-square(1) = **8.96**;
- descriptive misfit p = **0.00276**;
- downstream-resolved probability = **0.0112**.

## Monte Carlo diagnostic

A dedicated workflow simulated **2,000,000** draws from the three fitted equal-latent-effect attenuation nulls using each programme's registered sampling covariance and multiplicity threshold.

Empirical downstream-resolution rates:

- Wandoo: **0.011777**;
- Cardiopetalum: **0.0246285**;
- Kakamega Acanthopale: **0.0110715**.

All three appeared downstream-resolved in **2 / 2,000,000** draws (`1e-6`). The analytic product of the programme-specific rates is `3.25e-6`.

**This joint number is not a formal p-value.** The three anchors were recognized after outcome inspection, so using their joint simulation frequency as confirmatory inference would be circular.

## What the audit supports

The audit rejects a simple explanation that the three anchor mismatches exist merely because the interaction endpoint is much less reliable than reproductive function.

More specifically:

1. Wandoo retains opposite process/function signs after reliability correction;
2. Cardiopetalum does not show the reliability asymmetry needed to attenuate I from the F-sized latent response;
3. Kakamega remains incompatible with the required attenuation ratio even when F is granted perfect reliability.

Therefore:

> **The existence of downstream false-reassurance mismatches in these three independent fragmentation programmes is not readily explained by the audited difference in endpoint measurement reliability.**

## What the audit does not support

Do not claim:

- that downstream mismatches occur more frequently than upstream mismatches in nature;
- that `3:0` is a confirmatory sign/binomial result;
- that all seven pair-testable programmes have adequately estimated endpoint reliability;
- that classical reliability attenuation exhausts every form of measurement bias;
- that visits, pollinator abundance or pollen quantity are universally poor measurements.

The broader 3-versus-0 asymmetry remains hypothesis-generating because reliability calibration is incomplete for unresolved programmes and the three anchors were identified post hoc.

## General ecological interpretation

The stronger and more general result is not a prevalence asymmetry. It is a **sentinel sufficiency failure**:

> Fragmentation can depress reproductive function more strongly than would be inferred from apparently retained interaction quantity, and this failure mode persists after explicit stress-testing of differential endpoint reliability in the three resolved anchors.

This is narrower than discovering that visitation and pollination effectiveness differ, which is already established. The contribution is the matched fragmentation-context evidence together with an explicit measurement-artifact audit.

## Reproducibility

- `scripts/check_if_reliability_sufficiency.py`
- `evidence/meta_extraction/if_reliability_wandoo_table6_v1.csv`
- `evidence/meta_extraction/if_reliability_sufficiency_v1.csv`
- workflow `.github/workflows/if-reliability-sufficiency.yml`
- successful workflow run: `37409380227`.
