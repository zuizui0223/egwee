# EGWEE submission state — SCIENTIFIC VALIDATION GREEN 2026-10-03

> **STATUS: SCIENTIFICALLY VALIDATED, HUMAN ADMINISTRATION PENDING.** Full CI run `37109896871` reproduces the denominator-frozen qualitative I–F audit, Supplementary Table S6, scale-aware figure/table package, double-anonymous manuscript and anonymous reviewer package. Submission remains unauthorised only until human author/declaration metadata and final approval are complete.

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

## Frozen qualitative external I–F audit

Eight already-screened but quantitatively blocked programmes are now retained as a complete qualitative denominator. Their source-reported geometries are mixed: five show qualitative non-monotonic I–F translation, two show no detected loss in either layer, and one shows a concordant population-size response.

These counts are descriptive only. No detected effect is not coded as zero/equality, the eight rows do not increment the quantitative denominator, and their category frequencies are not prevalence estimates. The audit is reproduced as Supplementary Table S6.
## Submission gate

Journal of Ecology remains the target. The scientific gate is **closed successfully**: full CI run `37089505747` passed with the scale-aware proxy-failure manuscript, uncertainty-aware Figure 3, Figure 4/Table 2, supplementary outputs, double-anonymous check and anonymous reviewer package.

The only remaining gate is human administration: final authorship, affiliations, corresponding-author details, contributions, funding/permits, conflicts and all-author approval. `submission_ready=false` remains intentional until those fields are approved.


## Scale-stable interaction–function sign geometry

The broader matched I–F evidence contains 18 primary panels from 8 independent programmes. Six panels have opposite I/F signs and occur in 5 independent programmes. Both I+,F− and I−,F+ geometries occur. Three of four multi-panel programmes show more than one sign geometry among focal species/panels under the same registered exposure frame.

This is a descriptive existence result, not a prevalence estimate or independent-trial sign test.

Canonical files:
- `manuscript/IF_SIGN_GEOMETRY_2026-09-29.md`
- `evidence/meta_extraction/if_sign_geometry_census_v1.csv`
- `scripts/check_if_sign_geometry.py`


## Scale-stable interaction–function proxy failure

The strongest current cross-context ecological lead is narrower than the full point-sign census.

Three independent matched I–F programmes—*Eucalyptus wandoo*, *Cardiopetalum calophyllum* and Kakamega *Acanthopale pubescens*—retain a resolved downstream function-dominant mismatch under their audited representations. They span three continents and three plant families. No audited I–F programme has an equally representation-stable resolved upstream mismatch.

The broader point-sign audit contains 6 opposite-sign panels across 5 programmes, but 0/6 have both marginal endpoint directions individually resolved at 95%. Those point-sign patterns are therefore supporting, hypothesis-generating topology rather than six confirmed sign reversals.

Canonical files:
- `manuscript/SCALE_STABLE_QUANTITY_FUNCTION_PROXY_FAILURE_2026-09-29.md`
- `evidence/meta_extraction/scale_stable_quantity_function_proxy_failure_v1.csv`
- `scripts/check_scale_stable_quantity_function_proxy_failure.py`
- `manuscript/IF_SIGN_UNCERTAINTY_2026-10-01.md`
- `evidence/meta_extraction/if_sign_uncertainty_v1.csv`
- `scripts/check_if_sign_uncertainty.py`
- `manuscript/IF_PROXY_FAILURE_NOVELTY_AUDIT_2026-10-01.md`
