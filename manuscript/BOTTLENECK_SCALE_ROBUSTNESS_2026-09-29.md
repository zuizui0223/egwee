# Cross-scale process–function geometry audit — 2026-09-29

## Purpose

Re-evaluate the historical 12-programme process–function catalogue after the Hedges-g versus lnRR estimand audit.

## Result

The catalogue is **not scale-invariant at the level of system attribution**.

On the registered g/Fisher-z representations:

- resolved downstream function-dominant: Wandoo, Cardiopetalum, Kakamega;
- resolved upstream process-dominant: Serapias.

After re-expressing all recoverable direct Hedges-g process–F comparisons as lnRR with raw-unit multivariate-delta covariance, while leaving continuous-gradient Fisher-z programmes on their registered scales:

- resolved downstream function-dominant: Wandoo, Cardiopetalum, Kakamega;
- resolved upstream process-dominant: Brosimum, Eucalyptus socialis;
- Serapias becomes unresolved (`p=0.6364`);
- Chaco remains unresolved (`p=0.9381`);
- Sevenello remains unresolved (programme `p=1.0`).

Thus downstream identity is stable across the audited representations, while upstream identity is not.

## Kakamega check

The direct Kakamega programme remains resolved after lnRR reconstruction:

- Acanthopale I lnRR = +0.06444;
- Acanthopale F lnRR = -0.33106;
- I − F = +0.39550;
- panel p = 0.000346;
- four-panel programme Bonferroni p = 0.001384.

This is genuine cross-scale support for a downstream function-dominant geometry in that programme.

## What survives across scale

At the coarse geometry level, both downstream function-dominant and upstream process-dominant resolved contrasts occur under both the registered-scale catalogue and the lnRR-reexpressed direct catalogue.

However, the direct systems supplying the upstream evidence change from Serapias on g to Brosimum and Eucalyptus socialis on lnRR.

Therefore the allowed ecological interpretation is:

> **Transition-specific filtering is plausible across systems, but attribution of a bottleneck position to a specific direct system is effect-scale sensitive.**

This is exploratory because the 12-programme catalogue was assembled after the individual analyses and mixes registered direct and gradient effect families.

## Not authorised

- a scale-invariant system-specific bottleneck catalogue;
- a prevalence estimate for upstream versus downstream regimes;
- choosing g or lnRR because it yields the preferred biological system;
- claiming a universal attenuation or compensation pathway.

## Machine check

- `scripts/check_bottleneck_scale_robustness.py`
- `evidence/meta_extraction/bottleneck_scale_robustness_v1.csv`

Dedicated workflow: `.github/workflows/estimand-scale-robustness.yml`.
