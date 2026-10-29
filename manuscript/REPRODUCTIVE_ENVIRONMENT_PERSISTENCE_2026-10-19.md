# EGWEE — retrospective two-year hierarchy and context sensitivity (19 October 2026)

**Status: EXPLORATORY; NOT A NEW ECOLOGICAL REPLICATION OR SUBMISSION RESULT.** This study is in empirical egwee, not theoretical egwe. It follows the existing Wandoo and Cardiopetalum analysis in PR #52. It changes no frozen 5-cluster, 8-matched-I–F, 16-programme or external SF06 denominator; submission_ready remains false.

## Ecological question

Can a persistent population-level reproductive hierarchy coexist with changing year-to-year production, and does environmental context add information beyond measured pollination quantity? We distinguish observed fruit production from seeds per **existing** fruit. These are not equivalent fitness measures.

## Original prior art and what is actually incremental

Llorens et al. (2018, doi:10.3389/fevo.2018.00039) **already discovered** the negative salinity–fruit associations across both years, the increase in pollen tubes in small populations, one-year population-size/seed-filling relationships, and a mean year effect on fruit production (Methods, Results and Discussion; Figures 2–3 and Tables 1, 6). Their discussion already identifies soil conditions, self-pollination and seed abortion as competing causes. Their soil EC hypothesis must never be relabelled as egwee's finding.

The new reanalysis explicitly compares **within-population between-year ranks on a common 11-population frame** with leave-one-population and paired resampling, evaluates source-faithful **log1p fruit responses** against previous raw-scale regressions, and tests whether fragment area in independent Cardiopetalum survives alternative simultaneously measured landscape/context controls. None is a causal demonstration or a fresh confirmatory study.

## Wandoo: persistent spatial hierarchy; temporally variable outputs

Source-locked inputs: evidence/meta_extraction/wandoo_reproductive_stages_20261019_table1.csv and table6.csv. The independent unit is population. Common sample J,K,F,C,E,G,B,I,A,H,D (n=11), with legitimate no-fruit L (n=12) in fruit sensitivity. Of 19 Table 1 populations, seven have no Table 6 reproduction observations. L's seeds per fruit remain **undefined**, not zero.

| Same 11 populations | Pearson correlation across source years | Spearman correlation |
|---|---:|---:|
| Fruits per branch, y2 versus y3 | +0.91933 | +0.91116 |
| Seeds per *existing* fruit, y1 versus y2 | +0.31418 | +0.36364 |

All 11 fruit-producing populations have fewer fruits per branch in y3 than y2. In two populations, J and F, the number of flowers per branch is actually higher in y3 despite the lower fruit number. The median within-population fruits-y3/fruits-y2 ratio is **0.4643**. Seven of 11 have more seeds per fruit in y2 than in y1. Removing each population in turn leaves the fruit correlation +0.8896 to +0.9488, while the seed correlation ranges +0.1183 to +0.4769. The common-population correlation contrast is approximately +0.6052, with a paired 25,000-resample percentile interval approximately +0.14 to +1.31, seed 20261019.

**Do not interpret this as a formal stage-by-year interaction.** Fruit time pairs are y2→y3, seed-fill time pairs y1→y2; differences in timing, sampling of branches in y3, maternal covariance, weather, flowers, and means versus true individual fates remain confounded. Correlated years are **not independent fragments or ecological confirmations**. Also the original paper already reports a mean fruit year effect and salinity associations in both years; the additional rank arithmetic is only a descriptive crosswalk.

## Same populations; changing estimand from raw fruit to log(1 + fruit)

A purely retrospective **stress test**, not outcome-blind model selection. Predictors in each 4-parameter model are intercept + observed pollen tubes in y2 + log10 population size + log10 EC. n=12 (includes L, zero fruits) or common n=11. The source has no pollen measurement in y3, so a y3 model that includes pollen tubes from y2 is **historical-context prediction only**, not synchronized mediation.

| Frame / response | Conditional EC slope (log1p fruit scale) | Nominal OLS p | HC3 t-reference p |
|---|---:|---:|---:|
| 12 populations, fruit y2 | −4.160 | 0.00025 | 0.01553 |
| 12 populations, fruit y3 | −3.326 | 0.01923 | 0.01103 |
| Exclude L, fruit y2 | −3.054 | 0.00964 | 0.06571 |
| Exclude L, fruit y3 | −2.722 | 0.16265 | 0.07473 |
| Exclude L and G, fruit y2 | −2.144 | 0.10356 | 0.11607 |
| Exclude L and G, fruit y3 | −2.205 | 0.41142 | 0.39462 |

These p values are **unadjusted exploratory model sensitivities**, not a new familywise-significant discovery. Because L is a no-fruit/high-EC extreme and the adjusted uncertainty weakens once L or G is omitted, a transformed-response advantage must not be sold as representation-stable support for an environmental mechanism. Raw-scale 11-population joint-model Holm EC p-values were 0.06981 (fruits) and 0.05891 (fruit:flower), with HC3 fruit-number p=0.05634. That remains the primary pre-existing model scale; log1p is merely a sensitivity.

## Cardiopetalum: local density, area and isolation are not interchangeable

Elias et al. (2012) Table 1 values from evidence/meta_extraction/phase2_cf01_cardiopetalum_table1_v1.csv. Forest fragment n=10, responses are source fruit-set means, interaction is source beetles per flower. The area effect and fragmentation mismatch were **already** established by the original authors and EGWEE's previous gradient recovery.

| Fixed model of fruit set | In-sample R² | Leave-whole-fragment-out RMSE | Nominal p for ln(area) | HC3 t-reference p |
|---|---:|---:|---:|---:|
| Beetles alone | 0.080 | 0.11562 | — | — |
| Beetles + ln(area) | 0.875 | 0.04654 | 0.000286 | 0.000390 |
| Beetles + ln(area) + ln(distance) | 0.882 | 0.0488 | 0.03389 | 0.02479 |
| Beetles + ln(area) + ln(local plant density) | 0.879 | 0.0560 | 0.00076 | 0.00341 |
| Beetles + ln(area) + ln(distance) + ln(density) | 0.883 | 0.0633 | 0.07482 | 0.19933 |

All fragment-deletion area slopes remain **positive** in the indicated nested models, but positive slopes are not necessarily statistically resolved in every deletion. Area–nearest-distance correlation r=−0.867; the models have 10 fragments and as many as five fitted coefficients. The data contain a 13.46-fold area gap between fragments of 33.8 and 455 ha, so no ecological breakpoint can be inferred from this series. Local plant density is not a replacement for area, but area can stand for multiple unmeasured environmental processes. Whole-fragment LOO is *within-study* validation and not future-landscape transport.

## Corrected ecological claim and generality ceiling

The **positive** result is narrow: in two independent observational landscapes, measured interaction quantity does not exhaust information about realized female reproduction; environmental / spatial context helps in some model representations. Wandoo's local soil chemistry and Cardiopetalum's forest fragment area are **different moderators**. They do not support a common causal post-pollination filter.

New here: the cross-year *rank* contrast quantifies persistence of Wandoo population-level reproductive hierarchy; an explicitly complete scale/influence audit shows that environmental effects vary with response transformation and influential populations; joint landscape controls put limits on Cardiopetalum's area inference. These are retrospective statistical insights, not new biological observations.

The biologically interesting follow-up is a synchronized design, within independent landscapes, measuring pollen/visitation quantity Q, **compatible pollen provenance** E, maternal water/nutrient/salinity environment, fruit initiation, seed number and subsequent recruitment. It should factorially manipulate pollen addition and environmental conditions when possible; only such data can distinguish pollen insufficiency from abiotic post-transfer or sampling explanations. Existing 8/8 EGWEE quantitative interaction–function studies measure quantity but 0/8 measure compatible mating on the exact same matched frame. Sevenello's raw pollen-supplementation data remain blocked by source HTTP 500, so no treatment contrast is inferred.

## Reproduction and boundary

Reproducible checker: scripts/audit_reproductive_environment_persistence_20261019.py, fixed-source CSVs above. The standalone Actions workflow reproducibly exports JSON with all fitted coefficient tests and whole-landscape omissions. Uncertainty is descriptive and the simple OLS models for fruit set need not obey [0,1] bounds. No implicit zero imputation, independent-study inflation, exposure substitution or change to manuscript submission freeze is authorized.
