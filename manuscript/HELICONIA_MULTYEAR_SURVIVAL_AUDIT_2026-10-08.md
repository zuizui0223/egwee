# Heliconia: absorbing-death and multiyear ascertainment audit

**Status:** post hoc reanalysis of the same BrunaLab/HeliconiaSurveys programme used by the previous [first-year cohort audit](HELICONIA_COHORT_OBSERVATION_AUDIT_2026-10-08.md). The original authors published these data and prior demographic studies. This does not add to EGWEE quantitative denominators and is not a fragmentation causal effect.

## Problem and protocol

A seedling reported dead in year t+1 may have no record in t+2 or t+3; the archive does not keep a dead row every subsequent year. Missing seedlings can later be found alive. A naive survival denominator using only alive and dead rows at exactly t+h omits deaths in intervening years. Instead, classify a new seedling as dead if a death was recorded in any year t+1 through t+h (absorbing death); alive if no earlier death and alive at t+h; and unknown if neither is established. Never convert unknown to dead.

For equal observability across 13 plots, use newly flagged seedlings from 1999–2005 for h=1, 1999–2004 for h=2, and 1999–2003 for h=3. Count source-verified plant identities, then calculate within-plot known-fate survival. The group estimand is the unweighted mean over six continuous-forest or seven fragmented-forest plots, not a pooled individual-level survival statistic.

## Corrected results

| Horizon | Continuous plot mean | Fragment plot mean | Unblocked plot permutation p | Ranch-blocked permutation p |
|---|---:|---:|---:|---:|
| 1 year | 0.84996 | 0.85821 | 0.6544 | 0.5667 |
| 2 years | 0.74345 | 0.76795 | 0.3986 | 0.3917 |
| 3 years | 0.69455 | 0.69265 | 0.9534 | 0.9542 |

The 3-year birth cohorts comprise 1,298 plants from continuous forests (767 confirmed alive, 411 previously dead, 120 unknown) and 748 from fragments (477 alive, 199 previously dead, 72 unknown). Missingness is not zero.

**Crucial bookkeeping falsification:** the invalid endpoint-only calculation gives 3-year plot-mean apparent survival of 0.90949 (continuous) versus 0.94697 (fragment), creating a false +3.75 percentage-point fragment advantage. Including *all deaths recorded since first entry* yields 0.69455 versus 0.69265, a −0.19 percentage-point difference. The contrast reversal arises from failure to carry forward death status, not from a demonstrated biological mechanism.

The original first-year audit found 116 of 222 seedlings missing one year after recruitment were seen alive in some later observation. Re-detection means unknown fates cannot be coded as death. None of the known-fate estimates identifies true unconditional survival without additional detection/dormancy assumptions.

The p-values enumerate all 1,716 unblocked allocations or 240 ranch-stratified label reallocations. The plots were not assigned treatment by these procedures; these are descriptive small-sample comparisons, not a randomized-causal experiment or equivalence demonstration.

## Implication and prior-work boundary

If missing rows or extinct records are converted into apparent biological vital-rate gains, a multistage fragmentation model can mistakenly localize the bottleneck. The observation process must be modelled separately from recruitment, survival, growth and reproduction. This conclusion is an audit of a known demographic system; general detection bias, the established stage structure and the 2005 and 2022 Heliconia findings are not claimed as new discoveries.

Relevant prior work: Bruna & Oli 2005 (doi:10.1890/04-1716) and Scott, Uriarte & Bruna 2022 (doi:10.1111/gcb.15900). The remaining biological question needs independent systems with compatible pollen/seed supply, safe-site availability and population growth recorded in the same frame.

## Reproducible script

Run: python scripts/audit_heliconia_multiyear_survival.py --output build/heliconia_multiyear_survival_v1.json

The script verifies the pinned upstream files, counts absorbingly recorded death and reversible non-detection, and checks the plot and ranch inference units. The original five-cluster EGWEE meta-analysis is not changed.
