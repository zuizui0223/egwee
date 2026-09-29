# EGWEE submission state — SCIENTIFIC VALIDATION GREEN 2026-09-29

> **STATUS: SCIENTIFICALLY VALIDATED, HUMAN ADMINISTRATION PENDING.** The estimand-scale revision is complete and the current full CI reproduces the manuscript, scale-aware figure/table package, double-anonymous checks and reviewer package. Submission is still not authorised until author/declaration metadata and final approval are complete.

## Why the freeze was reopened

The historical five-cluster Hedges-g synthesis is exactly reproducible:

- full Fisher p = 0.01212432;
- omit-ML001 *Serapias* p = 0.18194353.

However, the biological interpretation is not invariant to effect-size scale. Re-expressing the same positive-valued direct endpoints as oriented lnRR changes endpoint ordering and the leave-one-*Serapias* robustness classification.

In *Serapias*:

- Hedges-g absolute order: G > C > F;
- lnRR absolute order: C > F > G;
- C–F lnRR contrast under raw-unit multivariate delta covariance: p = 0.6364.

For the omit-ML001 Fisher sensitivity:

- lnRR + raw-unit multivariate delta covariance: p = 8.31e-05;
- lnRR + zero covariance: p ≈ 0.00434;
- lnRR + covariance-free maximum-variance boundary: p ≈ 0.111.

Therefore neither “Serapias-dependent separation” nor its opposite is a scale/dependence-invariant ecological conclusion.

## Scale-stable result

All **17/17** primary direct effects are negative on both oriented Hedges g and oriented lnRR.

This supports a common direction of fragmentation-associated deterioration across the measured direct-response layers. It does **not** establish equal magnitudes, magnitude separation or a universal layer ordering.

The clearest qualitative sign discordance remains outside the primary direct stream in the separate *Eucalyptus wandoo* gradient, where interaction/pollen quantity is positive while reproductive function is negative.

## Exploratory ecological hypothesis

The lnRR audit suggests transition-specific filtering rather than one universal bottleneck:

- *Brosimum*: connectivity -0.537 → progeny vigour -0.204;
- *Eucalyptus socialis*: mating support -0.897 → family growth -0.056;
- *Spondias*: adult H_O -0.154, juvenile -0.536, seed -0.397;
- Chaco supplies interaction→reproduction amplification counterexamples.

These are post hoc hypothesis-generating observations. No universal attenuation or cohort-lag claim is authorised.

## Main-output revision

The former life-cycle-bottleneck Figure 4 / Table 2 are superseded as main inferential outputs.

The revised main package uses:

- Figure 4: estimand-scale sensitivity;
- Table 2: cluster/Fisher g-versus-lnRR sensitivity summary;
- Supplementary Table S4: the former 12-programme registered-scale process–function census, retained for transparency and hypothesis generation.

## Canonical audit files

- `manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-29_EFFECT_SCALE.md`
- `manuscript/ESTIMAND_SCALE_ROBUSTNESS_2026-09-29.md`
- `evidence/meta_extraction/estimand_scale_robustness_v1.csv`
- `evidence/meta_extraction/estimand_scale_cluster_summary_v2.csv`
- `evidence/meta_extraction/estimand_scale_fisher_sensitivity_v2.csv`
- `scripts/check_estimand_scale_robustness.py`
- `scripts/check_bottleneck_scale_robustness.py`
- `evidence/meta_extraction/bottleneck_scale_robustness_v1.csv`
- `manuscript/BOTTLENECK_SCALE_ROBUSTNESS_2026-09-29.md`
- `manuscript/EXPLORATORY_TRANSITION_FILTERING_2026-09-27.md`

The 2026-09-27 carried-rho sensitivity files are retained as provenance but are superseded for main lnRR dependence reconstruction by the 2026-09-29 raw-unit delta audit.

## Submission gate

Journal of Ecology remains the target. The scientific gate is now **closed successfully**: the current full contract passed with the scale-aware manuscript, Figure 4/Table 2, Supplementary Table S4, double-anonymous check and anonymous reviewer package.

The only remaining gate is human administration: final authorship, affiliations, corresponding-author details, contributions, funding/permits, conflicts and all-author approval. `submission_ready=false` remains intentional until those fields are approved.
