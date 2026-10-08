# Heliconia recruitment and detection-state audit (2026-10-08)

**Status:** Post hoc independent-plot reanalysis of a public longitudinal source; not an additional EGWEE primary study/cluster, not prospective replication and not a new stage-switch law. This is `egwee` empirical ecology, not the `egwe` NEE theoretical operator project.

## Exact source and biological units

- Bruna et al. (2023), *Ecology* data paper, doi:10.1002/ecy.4174; Dryad doi:10.5061/dryad.stqjq2c8d.
- Public [BrunaLab/HeliconiaSurveys](https://github.com/BrunaLab/HeliconiaSurveys) archival tables `data/survey_archive/HDP_survey.csv` and `HDP_plots.csv` pinned to upstream commit `830f9092f1a6906c66455f6c4dd916c0160d2fbc`. Source Git blob SHA-1 `f82a6f241493a979a2923d1c5deef6a1be0ff3ed`; plot-descriptor Git blob `6fc835fb870d8c43ae4a4fcf04d515f419e6db22`.
- Raw unit: plant × year, 66,396 rows (1998–2009), 8,586 unique `plot_id|plant_id` combinations and 3,464 individuals first recorded as seedlings after the baseline survey; 13 independently sampled 0.5-ha plots: 6 continuous-forest `CF` and 7 experimentally isolated `FF`.
- Independent landscape unit for descriptive effects and exact tests: **plot (n=13)**, with ranch (`esteio`, `dimona`, `porto alegre`) preserved as a blocking variable. Repeated plant-year records and many seedlings are not independent exposure assignments.
- Comparable one-year cohort window: new `recorded_sdlg=TRUE` at annual censuses 1999–2005; next-census status in 2000–2006. This omits 1998 baseline enumeration and avoids missing 2007 surveys in some fragments and subsequent censoring of FF-7.

Both programmatic source-integrity and result checks are in [`scripts/check_heliconia_longitudinal_recruitment.py`](../scripts/check_heliconia_longitudinal_recruitment.py), with [locked 13-plot table](../evidence/meta_extraction/heliconia_cohort_1999_2005_plot_v1.csv). No sensitive raw records or individual locations are copied into EGWEE.

## Plot-balanced, ranch-blocked results

| Metric | Continuous forest (6 independent plots) | Fragments (7 independent plots) | Difference F − C | Exact within-ranch two-sided p |
|---|---:|---:|---:|---:|
| Annual new seedlings / 0.5-ha plot, equal-plot mean | 36.929 | 21.204 | −15.724 | 0.2375 |
| New seedlings / 100 measured plant-year records, mean of plot-specific ratios | 6.879 | 6.639 | −0.240 | 0.7958 |
| Next-year survival *among alive/dead-classified* first-year seedlings, equal-plot mean | 0.8500 | 0.8582 | +0.0082 | 0.5667 |
| Fraction classified alive if all `missing` were **wrongly** called dead, equal-plot mean | 0.6348 | 0.8035 | +0.1687 | 0.0208 |
| Fraction classified missing next year, equal-plot mean | 0.2523 | 0.0638 | −0.1884 | 0.0417 |

The two-sided exact permutation enumerates 240 within-ranch relabellings (Esteio choose 3 of 5 reference plots; Dimona 1 of 4; Porto Alegre 2 of 4). Equal-plot means are intentionally different from seedling-weighted frequencies.

The 1999–2005 eligible cohorts include **2,590 newly recorded seedlings**: 1,551 continuous, 1,039 fragmented. Their next census yielded continuous 1,186 `measured`, 214 `dead`, 151 `missing`; fragmented 829 `measured`, 139 `dead`, 71 `missing`. Among seedlings with a resolved alive/dead state, observed fractions are 1,186/1,400 = 84.7% and 829/968 = 85.6%, respectively. These are *descriptive detected-state frequencies*, not unbiased survival probabilities.

**A missing plant is not necessarily dead.** Of the 151 continuous seedlings reported `missing` at one-year follow-up, **83 were measured again the following census**. Among fragments the corresponding number is 19/71, with some second-follow-up years not surveyed. The paper's status definitions explicitly identify `missing` as “not found during census,” not death. Treating that state as dead creates an apparently strong advantage for fragments at the plot level; excluding it almost eliminates that contrast. Both extremes can misrepresent the biological truth, so the effect of habitat on true annual survival is **not identified** by either simple shortcut.

## Biological interpretation and failure to replicate a stronger claim

The observed landscape-group mean of new seedlings per equal-size plot is lower in fragments, but between-plot heterogeneity is large and the ranch-blocked exact test is not compelling. Standardising by measured stock makes this difference small; **new seedlings / measured plant-year records is not true per-capita fecundity**, and the denominator may itself respond to fragmentation. Likewise, flowering status and seedling entry are not proven to be linked to the same parents or fruit-production year.

The measured window misses any germination or mortality occurring before each year's new seedling census. It therefore cannot by itself identify the seed-versus-safe-site allocation in experimental sowing trials, the reproductive-to-recruitment conversion function or habitat effects on unseen annual transitions.

Important prior art:
- Bruna (2002), doi:10.1007/s00442-002-0956-y, already documented reduced natural seedling recruitment in fragments and experimentally lower germination/establishment of sown seeds.
- Uriarte et al. (2010), doi:10.1890/09-0785.1, already studied seed supply versus safe-site limitation in this same landscape/taxon.
- Scott, Uriarte & Bruna (2022), doi:10.1111/gcb.15900, already showed delayed climate effects on vital rates and greater effects of precipitation extremes in fragments.
- These reports share biological provenance; do **not** count them as independent cross-species or cross-landscape replications.

The reanalysis therefore **does not confirm** the proposed novel universal stage-relocation mechanism. It demonstrates why the stage of an apparent bottleneck can be changed by (1) conditioning on post-entry observation, (2) changing the numerator denominator, and (3) converting non-detection into death. Those are measurement effects that must be disentangled before attributing a stage transition to ecology.

## What new test would advance ecological mechanism?

On new data, predefine three distinguishable quantities for each same-site reproductive episode:

1. **Source** — absolute compatible-seed production and donor quality (not merely flowering plant count).
2. **Opportunity** — seed arrival and fraction/quality of truly recruitable microsites on the entire plot footprint, including zero-availability area.
3. **Fate and detection** — repeated fate assessments, including dormant/non-emergent and temporarily missed individuals, preferably with an explicit state-observation model.

Evaluate whether source, opportunity and detection jointly predict independent held-out plot recruitment **better than** a seed/flower-count-only baseline. An experimental randomised seed addition × safe-site restoration remains necessary to distinguish causal intervention leverage. If the richer model does not improve held-out predictions, the stage-shift story must not be promoted.

## Integrity and publication boundary

The registered EGWEE direct 5-cluster/17-effect denominator, matched 8-programme I–F corpus, 16-programme qualitative map and external SF06 dataset remain unchanged. This is a retrospective data audit, not a new independent ecological discovery. The BrunaLab README asks research users to inform the authors and obtain a BDFFP Technical Series Number for any eventual publication; that administrative step is outside this computational audit. Submission freeze hashes are not overwritten to accommodate a post hoc appendix.
