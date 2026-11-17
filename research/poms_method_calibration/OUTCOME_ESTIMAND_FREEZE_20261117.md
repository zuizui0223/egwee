# PoMS same-date pan/FIT signed-outcome analysis freeze — 2026-11-17

**This file was registered after the outcome-blind ID gate (95 sites, 1,221 matched events) and before opening any numeric bee, hoverfly or floral-context values.** The ID-gate witness is `SOURCE_ID_GATE_RESULT_20261117.md`.

## Event and endpoints

Read the SHA-pinned original PoMS pan **samples**, pan **flowers**, and **1-km FIT** source CSVs. Never use public/self-selected FIT observations. Match exact source (`country`, `sample_projection`, `x1km_square`, `date`). Pan insect occurrence table is not additionally summed because the pan sample file already provides verified source-native `bees` and `hoverflies` group totals; doing both would double count.

At each matched site-date: `B_pan=sum(pan.samples.bees)`, `H_pan=sum(pan.samples.hoverflies)`, `B_fit=sum(FIT.bumblebees+honeybees+solitary_bees)`, `H_fit=sum(FIT.hoverflies)`. FIT `other_flies` is **not** relabelled as hoverflies. All count fields must be nonnegative whole numbers; any missing numeric value in a component for an event triggers **event exclusion and an exclusion count**, not zero-filling or silently dropping that row. A pan trap event can comprise 1–6 station samples; a FIT event can comprise 1–10 counts. No station or FIT count is an independent ecological replicate.

Exclude site-dates with `B_pan+H_pan=0` or `B_fit+H_fit=0` from **relative-composition** estimation; retain them as noninformative in the full sampling coverage table. No zero in one category is deleted, but use fixed Haldane–Anscombe 0.5 correction for finite log ratios. The same source crop applies to both methods; never admit different date sets to the primary comparison.

## Shared floral predictor

For each pan `sample_id`, count distinct floral taxon keys from the pan **flowers** source. Key hierarchy fixed before outcomes: source `source_taxon_version_key` if nonempty, otherwise `taxon_source` if nonempty; a blank pair cannot be a taxon. Any row with unknown sample ID (known 11 original flower records) is excluded, never matched approximately. For a matched site-date, predictor `X` = sum of per-sample taxon richness / number of pan sample records; this is **mean observed flowering taxon incidence per sampled station**, not true total flower number, floral cover, diversity of nectar, or pollen accessibility. Zero source flower rows at a surveyed pan sample are coded zero **conditionally on the dataset's complete survey protocol**, with mandatory zero-flower-record sensitivity because missing survey completion cannot be proven from schema alone. No use of FIT target-flower count as a substitute.

Standardize `X` by mean and population SD among retained information-bearing matched site-dates (one event = one unit), so all coefficients are per one SD of `X`.

## Primary observation-mode interaction

For each same-site same-date event, define:
```
Y_pan = log((B_pan + 0.5)/(H_pan + 0.5))
Y_fit = log((B_fit + 0.5)/(H_fit + 0.5))
D = Y_fit - Y_pan
```

Regress `D ~ X_z + site FE + survey year FE + calendar month FE` with **one equal-weight record per matched site-date**. The slope on `X_z` is `delta = beta_FIT - beta_pan` in units of log-odds-ratio contrast per SD of site-date floral incidence. Report separate `beta_pan` and `beta_fit` fitted with identical event set/design, and verify arithmetic identity `delta=beta_fit-beta_pan` within tolerance.

Estimate site-level uncertainty by **1,000 nonparametric whole-site bootstrap replicates**, frozen RNG seed 20261117, retaining all years/dates per resampled site. In each replicate create new bootstrap site labels to avoid convolving original repeated selections in site FE. Compute percentile CI 2.5–97.5%. Present descriptive coefficient and CI, not pseudo-replicated station-level p-values. If a bootstrap design becomes rank deficient, report failed replicates and STOP if >5% failed (do not fill zeros). Also report leave-one-original-site-out and leave-one-year-out delta ranges/signs, and X variance within sites.

Implementation may use exact algebraic demeaning (Frisch–Waugh–Lovell) for site FE and ordinary least squares for remaining month/year dummies. Year and month are not interchangeable; month parsed from the source date string. No alteration of model selection, predictors or outcome grouping by observed significance.

**Minimum post-outcome information threshold:** >=20 distinct sites and >=80 same-date events with positive bee+hoverfly observation totals in both methods, >=3 years, nonzero within-site variation of X. Otherwise output coverage and `UNIDENTIFIABLE` but no primary delta.

## Locked sensitivity and claim bounds

1. Repeat with only matched events where at least one flowering taxon was recorded at some pan trap (tests ambiguous zero flower surveys).
2. Repeat using total count-weighted event regression only as a **secondary** estimator (never replace equal-event primary); report if weighting reverses sign.
3. Partition annual 2017–2023 and each of the 95 sites in leave-one-out checks; do not interpret one-year or one-site fragility as stability.

Prior UK PoMS method comparison and flower effects have been published (2026 PoMS environmental paper, `10.1002/2688-8319.70327`; Westerberg 2021, `10.1002/ece3.7252`; Krahner 2024, `10.1002/ece3.11157`). This model's target is a **same-day method×shared floral incidence interaction**. A nonzero delta indicates disagreement between two observation channels and is **not** a causal estimate of sampling bias, true abundance, fitness, ecosystem function or genetic rescue. It does not independently validate prior v0.9, whose exposure and fly-group definitions differ.

The frozen historical five-cluster fragmentation meta, genetic-state pilots, and theoretical `egwe` are separate.
