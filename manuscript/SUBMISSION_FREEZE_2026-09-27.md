# EGWEE submission state — REOPENED 2026-09-27

> **STATUS: NOT SUBMISSION-READY.** The previous ecology-first submission freeze is superseded by a mandatory estimand-scale revision.

## Why the freeze was reopened

The historical five-cluster Hedges-g synthesis is exactly reproducible:

- full Fisher p = 0.01212432;
- omit-ML001 *Serapias* p = 0.18194353.

However, the biological interpretation is not invariant to effect-size scale. Re-expressing the same positive-valued direct endpoints as oriented lnRR changes endpoint ordering and the leave-one-*Serapias* robustness classification.

In *Serapias*:

- Hedges-g absolute order: G > C > F;
- lnRR absolute order: C > F > G;
- C–F lnRR contrast under the carried endpoint-correlation proxy: p ≈ 0.605.

For the omit-ML001 Fisher sensitivity:

- lnRR + existing rho proxy: p ≈ 2.92e-05;
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

- `manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-27_ESTIMAND_SCALE.md`
- `manuscript/ESTIMAND_SCALE_SENSITIVITY_RESULT_2026-09-27.md`
- `evidence/meta_extraction/estimand_scale_sensitivity_v1.csv`
- `evidence/meta_extraction/estimand_scale_cluster_summary_v1.csv`
- `scripts/check_estimand_scale_sensitivity.py`
- `manuscript/EXPLORATORY_TRANSITION_FILTERING_2026-09-27.md`

## Submission gate

Journal of Ecology remains the target, but submission is reopened.

The scientific gate is satisfied only when the current full CI contract passes with the scale-aware manuscript, scale-aware Figure 4/Table 2, Supplementary Table S4 and anonymous reviewer package.

Human author/declaration approval is a separate later gate. A green CI while `submission_ready=false` means the revision state is internally consistent; it does **not** authorize submission.
