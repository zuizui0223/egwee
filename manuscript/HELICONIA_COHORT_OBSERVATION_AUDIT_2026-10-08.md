# Heliconia stock-standardized recruitment and missing-state sensitivity

**Status:** secondary post hoc reanalysis of one previously published demographic programme. Not a new independent replication, not a causal estimate, and not included in the EGWEE five-direct-cluster or I–F denominators. This is the empirical `egwee` project, not the separate operator-theory `egwe` repository.

## Canonical public input and independent units

The source is BrunaLab/HeliconiaSurveys, `HDP_survey.csv` and `HDP_plots.csv`, archived at GitHub commit `0b999f6bcb47df1c31f0dd0a8b472055b5f81bc0`. The corresponding Git blob SHAs are `f82a6f241493a979a2923d1c5deef6a1be0ff3ed` and `6fc835fb870d8c43ae4a4fcf04d515f419e6db22`. The analysis script refuses changed source blobs. Source documentation: https://github.com/BrunaLab/HeliconiaSurveys/tree/master/data/survey_archive

The archive holds 66,396 individual-year records from 8,586 plants, including 3,464 newly marked seedlings. They occur in 13 permanent 0.5-ha plots: six in continuous forest and seven in fragmented forest, grouped across three ranch locations. We restrict first-observation `recorded_sdlg=TRUE` years to **1999–2005**, so **every plot** has both a preceding living-stock census (1998–2004) and a next-year fate census (2000–2006). This excludes 2007–2009 selectively missing late surveys from the main comparison.

Every record uses `plot_id + plant_id + year` as the unique key. Exactly one `recorded_sdlg=TRUE` mark occurs at a plant's first observed year. There are 2,590 seedlings in the balanced cohorts (1,551 continuous and 1,039 fragmented). Replication and tests are at the **13-plot** level, never 2,590 independent fragmentation landscapes or 66,396 independent effects.

## Two different estimands: total inflow versus observed-stock-normalized inflow

| Plot-mean quantity, 1999–2005 | Continuous (n=6 plots) | Fragmented (n=7 plots) | Difference (fragment − continuous) |
|---|---:|---:|---:|
| New seedlings per 0.5-ha plot per year | 36.929 | 21.204 | −15.724 |
| New seedlings per 100 *previously measured living individuals* | 7.252 | 7.191 | −0.061 |
| Next-year alive fraction among **known** alive/dead cohort fates | 0.850 | 0.858 | +0.008 |
| Next-year missing / absent fraction among cohort individuals | 0.252 | 0.064 | −0.188 |

Exact two-sided label permutations over all `C(13,7)=1716` allocations (equal mean weighting of independent plots) give respectively `p=0.26457`, `p=0.96678`, `p=0.65443`, `p=0.06876` for the four rows. These are **exploratory permutation descriptions conditional on exchangeable plot labels**, not a randomization-based causal test of forest fragmentation. Because plots are situated within three ranch landscapes, the script also computes all 240 ranch-stratified reallocations preserving the number of fragmented plots per ranch. Neither scheme models climate, plot environment, adult stage structure, or spatial correlation fully.

**Interpretation:** the lower raw number of seedlings per equal-area plot is strongly attenuated when expressed per prior observed living stock; the stock-normalized group means are virtually identical in this window. This may reflect smaller existing populations supplying fewer potential recruits, but the living-stock denominator includes juveniles and non-reproductive plants. It is **not** a reproductive-adult fecundity rate, not a direct-effect estimate controlling for an exogenous confounder, and not evidence that fragmentation had no historical or current impact. Conditioning on stock can remove part of fragmentation's mediated total effect.

Importantly, a non-significant test (including a very large p value) is **not equivalence evidence**. Population density, flower production, seed availability, propagule dispersal and seed viability remain unresolved mediating dimensions. The normalized result is a diagnostic against equating absolute recruit counts with a fragmentation-specific per-capita transition deficit.

## Why 'survival is unchanged' is not established

The source defines `census_status` as **measured = alive**, **dead = recorded dead**, and **missing = not found**. For the 1999–2005 new cohorts, 222 seedlings were missing in the following annual census. **116 of those 222** were observed alive in a later available census, so assigning all missing plants to mortality is demonstrably wrong. The 2000–2006 'known alive' fractions above condition on ascertainment, and the status-unknown share varies strongly among plots (one continuous plot has about 70.8% unknown status).

Worst-case endpoint-independent missingness bounds, computed as the difference between averages of plot-specific lower versus upper survival fractions, allow the fragment-minus-continuous survival contrast to lie between approximately **−0.084 and +0.233**. These are deterministic extreme bounds, not confidence intervals; assignment is arbitrary and may be biologically impossible in detail. Their purpose is to demonstrate that an equivalence claim is not identified from a known-fates-only comparison.

The later reappearance of `missing` plants also invalidates naive 'last observed date = death date' survival estimators. Proper multistate/interval-censored or capture-detection methods with plant identity and resurveys are warranted if downstream survival becomes central. For any multi-year endpoint, synchronized observability and a prespecified cohort censoring window are mandatory.

## Nearest prior art and novelty boundary

- **Bruna (2002), doi:10.1007/s00442-002-0956-y:** experimental seed establishment was lower in fragments; naturally occurring seedlings per plot were already shown to differ. EGWEE does not discover a new fragmentation-recruitment effect.
- **Bruna & Oli (2005), doi:10.1890/04-1716:** a life-table response experiment in this same 13-plot field system reported approximately `lambda=1.05` in continuous forest versus `lambda≈1` in fragments, with **different stage contributions in 1-ha and 10-ha fragments**. EGWEE must not present stage-specific causes as novel in this study.
- **Scott, Uriarte & Bruna (2022), doi:10.1111/gcb.15900:** this same long-term system has already been used to demonstrate delayed climate influences on survival, growth and flowering, with stronger drought/wet extremes in fragments for some vital rates.

The newly *audited operational contrast* is narrower: a balanced-cohort sensitivity showing that absolute recruitment differences can be strongly altered by the stock denominator and that a naive first-year survival comparison is underidentified due to the 'missing' observation process. It is **not a new ecological law** or an independent species replication of the Myrtus programme.

## Next falsifiable question

Can landscape-level recruitment deficits be partitioned into (A) fewer pre-existing plants, (B) lower output per reproductive adult, (C) poorer germination/establishment conditional on propagule arrival, and (D) imperfect detectability without circularly conditioning away effects of fragmentation?

The existing census provides plant trajectories and flowering (inflorescence presence), but not complete matched seed rain, viable propagule counts, or detailed safe-site availability for each mother-plot-year. A future reanalysis should use a predeclared demographic / observation model with ranch and plot structure and compare *held-out ranch or plot* predictive performance. Such a model must make explicit that recorded seedlings are observed establishments, not all biological recruits.

The competing interpretations remain stock-mediated demographic legacy, ongoing transition impairment, and observation bias. No one is presently identified as the unique cause.

## Reproduction

Run `python scripts/audit_heliconia_cohort_observation.py --output build/heliconia_cohort_observation_v1.json` to download the commit-pinned, blob-verified public archive and reproduce all 13 plot estimates and exact permutations. For offline data, add `--source-dir <directory>`. GitHub workflow `heliconia-observation-audit.yml` runs this check separately from the frozen EGWEE meta-analysis.
