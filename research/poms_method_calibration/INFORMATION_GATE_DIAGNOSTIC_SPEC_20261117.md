# PoMS paired-method informative-event selection audit — 2026-11-17

**Status: retrospective, exploratory diagnostic registered AFTER the signed primary outcome of PR #60 was inspected.** This is deliberately not an outcome-blind preregistration, not a second confirmatory hypothesis, and not an opportunity to select a new significant primary claim.

## Why this diagnostic is necessary

The frozen PoMS FIT-versus-pan flower-context contrast uses the same 972 of 1,221 matched site-dates in which each method observed at least one bee or hoverfly. The other 249 exact matches are uninformative for the corrected log-composition contrast, but conditioning on detectability in **both** observation channels may select a non-representative set of floral environments and sampling effort. This diagnostic quantifies that gate, without modifying the original estimator or its 95% site-bootstrap interval.

## Fixed original observation units and source

Use the exact EIDC 2017–2023 CSV members and SHA256s already pinned in `SOURCE_ID_GATE_RESULT_20261117.md`. Same country/projection/1-km-square/date join (1,221 expected). Reuse the same source-native pan group totals, FIT bee-group and hoverfly counts, and per-station source taxon incidence from `analyze_poms_paired_method_flora.py`. Public FIT is excluded. Zero pan sample flower rows have the same survey-completeness caveat as the primary. No third-party original row is redistributed.

Define `R=1` when **both** methods have positive total bee + hoverfly counts for that exact square-date, otherwise `R=0`. Missing/noninteger group components are `invalid`, excluded from numerical gate models and counted separately, never converted to zeros. Count pan-zero, FIT-zero and both-zero events as nonexclusive totals and mutually exclusive categories. Report pan station samples and FIT 10-minute counts per event as **effort proxies**, not standardized exposure time or true detection probabilities.

## Descriptive diagnostic models

On all exact matched events with valid group counts, let `X` be mean distinct flowering taxon keys per pan sample and `Xz` standardized by **all valid matched events**, not by the original positive-pair subset.

1. Equal-event linear probability slope of `R ~ Xz + site FE + survey year FE + calendar month FE`.
2. As an effort-confounding diagnostic only, `R ~ Xz + pan sample count + FIT count number + site FE + year FE + month FE`.

Estimate whole-site nonparametric bootstrap intervals (1,000 draws, fixed `seed=20261118`) with new bootstrap site identifiers for resampled copies. Include full date/year histories per site. If >5% of replicates are rank-deficient, STOP rather than reporting an interval. Report sample sizes, years, within-site X variation, site-bootstrap 95% percentile CI, descriptive sign stability, and R fractions by year. **No station-level p-values**. Recompute neither the primary D-slope nor its frozen denominator.

## Interpretation

A nonzero association indicates that the **information gate** differs along measured floral-context gradients, not why. This would make extrapolation of the 972-event composition contrast to all 1,221 matched site-dates unsafe. A zero-compatible slope would not prove missing-at-random, method equivalence, or population representativeness. Differences may reflect actual insects, FIT target-flower choices, weather/wind, pan effort and count duration. This audit estimates none of those mechanisms causally.

Keep separate from the five-cluster fragmentation meta, the genetic–fitness rescue programme and the theoretical `egwe`. Preserve draft status of PR #60 regardless of exploratory result.
