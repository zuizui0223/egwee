# Public Heliconia cohort sentinel audit — 2026-10-08

## Status

**Completed source-hash-gated exploratory reanalysis; no pooled fragmentation inference or causal stage-switch claim.** Reproducible script: `scripts/analyze_public_heliconia_cohort_sentinel.py`. GitHub Actions run: https://github.com/zuizui0223/egwee/actions/runs/37765358003 (successful; CSV artifact `public-heliconia-cohort-audit`). The audit was run on the public authors' source files, not on synthetic data.

Source: Bruna et al. (2023), Dryad doi:10.5061/dryad.stqjq2c8d; authoritative public data repository https://github.com/BrunaLab/HeliconiaSurveys at `data/survey_archive/HDP_survey.csv`, Git blob `f82a6f241493a979a2923d1c5deef6a1be0ff3ed`, paired with `HDP_plots.csv`. No data from this audit enters the locked EGWEE five-cluster meta-analysis, the eight matched I–F programmes, or the SF06 external sign subset.

## Source integrity and sampling frame

- Exactly **66,396** plant-year records and **3,464** rows marked as newly recorded seedlings.
- **13 independent permanent plots** of 50 × 100 m: six continuous forest (`forest`), four 1-ha isolated fragments (`one`), three 10-ha isolated fragments (`ten`).
- Survey year field ranges from 1998 to 2009. It is not a fully balanced 12-year panel: FF-5 and FF-6 lack 2007; FF-7 has records only through 2006. All denominators below use each plot's *observed post-1998 census years*.
- A seedling is counted only when `recorded_sdlg == TRUE`. The one-year comparison links precisely `plot_id × plant_id × (year+1)`; `dead` is death, `missing` is unknown observation state, and lack of the next census record is **not** imputed as death.
- Plot is the comparison unit; thousands of plant-years are repeated, dependent observations.

## Descriptive plot-balanced findings

| Habitat | Independent plots | Mean recorded new seedlings per observed plot-year | Mean new seedlings per 100 individuals present in 1998 per year | Mean next-year survival among new seedlings with known next status |
|---|---:|---:|---:|---:|
| Continuous forest | 6 | 32.9 | 8.45 | 0.865 |
| 1-ha fragments | 4 | 12.1 | 9.58 | 0.883 |
| 10-ha fragments | 3 | 27.5 | 11.33 | 0.861 |

Each row is an **unweighted mean of plot-level ratios**, not a pooled plant-level regression or a model-adjusted estimate. The numerator and follow-up cohort come from the public audit artifact. Ratios are descriptive and not significance tests.

The striking warning is a *denominator reversal*: continuous forest has the largest **absolute** new-seedling count per observed plot-year, but dividing by the number of plants present in each plot in 1998 no longer yields that same ordering. The baseline denominator itself reflects history, plant density and age structure; **these normalized figures do not show that fragmentation benefits recruitment**. They show how easily a statement about the "worst" stage can change with a defensible but different biological quantity.

Post-recording seedling survival is also similar across habitats *conditional on a next-year status being observed*. This is not a null effect on survival in nature. Germination failure, initial establishment losses, missing censuses and observations marked `missing` are not included in that conditional survival probability. The entry filter is *before* the first recorded seedling and cannot be reconstructed from these records alone.

## Prior art and causal interpretation ceiling

Bruna (2002; doi:10.1007/s00442-002-0956-y) already found much lower natural and experimental seedling establishment in fragments, with a seed-germination rather than post-germination mechanism implicated in that study. Uriarte et al. (2010; doi:10.1890/09-0785.1) found that safe-site limitation and heterogeneous light environments were important in separate mapped plots; **do not assume its 10 plots are automatically row-identical with these 13 demographic plots**. Scott, Uriarte & Bruna (2021/2022; doi:10.1111/gcb.15900), using related long-term demography, found climate lags up to 36 months and stronger extreme-precipitation impacts on some vital rates in fragments. Thus this audit is neither a novel discovery of early-stage fragmentation effects nor an independent replication of those publications.

The current dataset lacks compatible pollen or parentage, seed output, seed rain, safe-site footprint, and all seeds that failed before the first successful seedling census. Its **longitudinal strength is post-entry fate and delayed size/flowering transitions, not identifying which unobserved pre-entry process caused an entry deficit**.

## The discriminating next analysis

Predefine two non-interchangeable targets: (1) seedling entries per physical plot-year and (2) entry per actual maternal reproductive opportunity; the latter must be aligned by biological season (the same-year and one-year-lag interpretations must be declared, not selected based on fit). Use a full-plot holdout, with ranch, year and missing-year structure explicitly represented. Compare predictions based on adult occupancy/size/flowering histories versus prior seedling recruitment; test whether earlier-stage observations change prediction of later patch recruitment.

The analysis may fail to improve prediction. It must not infer seed supply, pollen quality, microsite availability or causality from the absence of such measurements. Before claiming a transferable recruitment-sentinel result, check against Bruna (2002), Uriarte et al. (2010) and Scott et al. (2021) for source and biological overlap.
