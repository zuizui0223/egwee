# EGWEE scale-aware submission freeze — 2026-09-27

## Status

This freeze supersedes the earlier variable-bottleneck submission freeze.

The current Journal of Ecology package is **scale-aware**. The registered Hedges-g analysis remains reproducible, but no biological claim about relative response amplitude, layer separation, bottleneck position or leave-one-cluster robustness is treated as scale-invariant unless it survives the mandatory estimand-scale audit.

## Scientific base

`5046c7f2bd793b36303ea85f887b4dec25e98d70` is the scale-aware scientific/package base immediately before this freeze update.

## Manuscript identity

**Habitat fragmentation across plant reproductive life cycles: directional consistency and scale-sensitive response amplitudes**

Target: *Journal of Ecology* Research Article.

## Historical registered primary analysis

- five independent direct programme/study clusters;
- 17 primary marginal Hedges-g effects;
- full Hedges-g Fisher p = **0.01212432**;
- omit-ML001 *Serapias* Hedges-g Fisher p = **0.18194353**.

These values remain part of the paper for protocol fidelity and reproducibility.

## Mandatory estimand-scale sensitivity

Using oriented lnRR from the same positive fragmented/reference summaries:

| estimand / dependence | full Fisher p | omit ML001 p |
|---|---:|---:|
| Hedges g / registered rho proxy | 0.01212432 | 0.18194353 |
| lnRR / carried endpoint-correlation proxy | 1.1787e-10 | 2.9182e-05 |
| lnRR / zero covariance | 1.7228e-09 | 0.00434418 |
| lnRR / Cauchy maximum-contrast-variance boundary | 9.9460e-05 | 0.111379 |

The correct inference is **not** that lnRR proves robust separation. The leave-one-*Serapias* classification itself depends on estimand scale and dependence assumptions.

## Serapias scale reversal

- Hedges-g absolute ordering: `G > C > F`;
- oriented-lnRR absolute ordering: `C > F > G`;
- Hedges-g C–F difference is resolved;
- lnRR C–F difference under the carried endpoint-correlation proxy is unresolved (`p ≈ 0.605`).

Therefore the former claim that *Serapias* supplies a scale-stable upstream bottleneck is withdrawn from the submission headline.

## Scale-stable result

All **17/17 primary direct effects are negative** on both oriented Hedges g and oriented lnRR.

This supports a common direction of fragmentation-associated deterioration across the primary direct corpus. It does **not** establish equality, separation or ordering of response magnitudes.

The clearest qualitative sign discordance remains outside the primary direct stream in the separate *Eucalyptus wandoo* gradient, where interaction/pollen quantity is positive while reproductive function is negative on its registered Fisher-z representation.

## Exploratory ecology

lnRR suggests post hoc patterns worth prospective testing:

- *Brosimum*: movement/connectivity ≈ -0.54 versus one-year progeny vigour ≈ -0.20;
- *Eucalyptus socialis*: mating support ≈ -0.90 versus family growth ≈ -0.06;
- *Spondias*: adult H_O ≈ -0.15, juvenile ≈ -0.54, seed ≈ -0.40.

These motivate filtering, buffering and cohort-lag hypotheses. They are hypothesis-generating only. Chaco provides a counterexample to any simple universal attenuation gradient.

## Status of the former 12-programme bottleneck census

The registered-scale process–function census is retained as **Supplementary Table S4 / exploratory transparency only**. Its bottleneck classifications are heterogeneous-scale and are not scale-invariant manuscript conclusions after the estimand audit.

## Main submission figures/tables

- Figure 1: primary evidence geometry;
- Figure 2: historical Hedges-g leave-one-cluster-out influence, explicitly labelled scale-specific;
- Figure 3: registered-scale I–F examples; unresolved differences are not treated as equality;
- Figure 4: estimand-scale sensitivity and exploratory ecology;
- Table 1: admitted primary direct clusters;
- Table 2: estimand-scale sensitivity summary;
- Supplementary Table S4: exploratory registered-scale bottleneck census.

## Canonical scale-audit files

- `manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-27_ESTIMAND_SCALE.md`
- `manuscript/ESTIMAND_SCALE_SENSITIVITY_RESULT_2026-09-27.md`
- `evidence/meta_extraction/estimand_scale_sensitivity_v1.csv`
- `evidence/meta_extraction/estimand_scale_cluster_summary_v1.csv`
- `evidence/meta_extraction/estimand_scale_fisher_sensitivity_v1.csv`
- `scripts/check_estimand_scale_sensitivity.py`

## Claim ceiling

Allowed:

- exact reproduction of the historical Hedges-g primary analysis;
- estimand/dependence sensitivity of magnitude-separation and leave-one-*Serapias* conclusions;
- 17/17 negative direct primary effects on both g and lnRR;
- separate registered-scale sign discordance in *Eucalyptus wandoo*;
- exploratory filtering/buffering/cohort-lag hypotheses, clearly labelled post hoc.

Not allowed:

- a scale-invariant global layer-separation syndrome;
- a scale-invariant variable bottleneck ordering;
- a universal attenuation/compensation pathway;
- a confirmed cohort lag;
- treating p=1.0 in ML020 as evidence that true effects are equal;
- claiming lnRR is the uniquely correct scale;
- direct empirical validation of EGWE/NEE theory.

## Remaining human-only blockers

- final author list;
- affiliations;
- corresponding-author details;
- author contributions;
- funding / permits / acknowledgements;
- conflict declaration;
- final all-author approval.
