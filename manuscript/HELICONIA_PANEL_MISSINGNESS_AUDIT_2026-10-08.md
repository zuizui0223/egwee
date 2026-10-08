# Heliconia individual-census audit: stage interpretation changes with observation state

Status: **exploratory external audit** of another team's archived natural-population data, not a new EGWEE confirmatory result. The empirical project is EGWEE, not the separate mathematical EGWE/NEE theory. The repository's frozen primary analyses and publication claims remain unchanged.

## Source and independent units

[BrunaLab/HeliconiaSurveys](https://github.com/BrunaLab/HeliconiaSurveys), pinned revision `0b999f6bcb47df1c31f0dd0a8b472055b5f81bc0`; archival data `HDP_survey.csv` Git blob `f82a6f241493a979a2923d1c5deef6a1be0ff3ed`, `HDP_plots.csv` Git blob `6fc835fb870d8c43ae4a4fcf04d515f419e6db22`, version 1.0.0, 25 August 2023. Data paper: Bruna et al. (2023), *Ecology*, as described in the authors' `data/survey_archive/README.md`.

The data contain 66,396 plant-year rows, 8,586 plant identities, 3,464 first-recorded seedlings, and 13 permanent plots (seven isolated forest fragments and six continuous-forest plots, all 50 × 100 m). Each fragment plot is nested within a 1- or 10-ha reserve but the census footprint is the same 0.5 ha. We never promote plant-years or seedlings to independent habitat treatments.

All 13 plots were censused in 1999–2006. For 1999–2006, count first-recorded seedlings per plot-year and per 100 contemporaneously observed live-plant records. The second quantity **is not a true birth rate**; its denominator includes newly observed seedlings and changes with standing abundance. For seedlings first recorded in 1999–2005, inspect their one-year-later `census_status` as `measured` (alive), `dead` (confirmed dead), or `missing` (not found in that annual census). All these cohorts have a next-year plot census. A 'missing' observation must not be recoded as confirmed death.

## Independent-plot descriptive results

The numbers below are means across **plots**, not means across pooled individual plant-year records.

| Outcome | Continuous forest, six plots | Fragments, seven plots | Exact unblocked plot-label p | Exact within-ranch plot-label p |
|---|---:|---:|---:|---:|
| Newly recorded seedlings per plot-year, 1999–2006 | 35.0208 | 20.2500 | 0.2657 | 0.2417 |
| New seedlings per 100 measured live-plant records | 6.7408 | 6.2235 | 0.6270 | 0.5833 |
| Next-year alive / (alive + confirmed dead), cohort 1999–2005 | 0.8500 | 0.8582 | 0.6544 | 0.5667 |
| Next-year documented alive / all seedlings | 0.6348 | 0.8035 | 0.0536 | 0.0208 |
| Next-year not found / all seedlings | 0.2523 | 0.0638 | see code artifact | 0.0417 |

Every exact comparison computes the *difference of plot-average rates*, not a pseudoreplicated count test: 1,716 unrestricted selections of seven of 13 labels, or 240 selections preserving the observed fragment numbers within each of three ranches. The exchangeable-label null is **not a randomized habitat-treatment design**. The analyses and choices are exploratory, and no p-value provides causal identification or confirmatory evidence of a new stage law.

Most notably, the *apparently higher documented one-year survival in fragments* tracks missingness: continuous forest has many more 'missing' year-two statuses. Conditional on being found alive or confirmed dead, the fragment/control survival estimates are almost equal. These do not establish equal true survival either: conditioning on known status selects individuals non-randomly if detectability depends on habitat or vigour.

### Direct source contradiction to coding not-found as death

Of the 1999–2005 new-seedling cohorts, 151 continuous-forest and 71 fragment individuals were marked `missing` in the next year's census. **At least 91 and 25, respectively, were found alive in at least one later census.** Follow-up after 2006 is not balanced across all fragment plots; these figures demonstrate reappearance, not comparable detection probabilities. Counting missing as death is demonstrably false for those individuals.

Sensitivity to assigning missing to latent survival is large. Assigning every missing individual to 'dead' yields the documented-alive mean (continuous 0.6348 vs fragment 0.8035); assigning every missing to 'alive' yields upper possible averages (continuous approximately 0.8871 vs fragment 0.8674). Neither extreme is a biological model. The sign of the habitat contrast is therefore **not identified** by one-year alive/dead/missing codes alone.

## Ecological conclusions and why this is not a new natural law

First, total observed recruitment tends to be lower in fragments, but the crude difference in plot means (35.0 versus 20.3) becomes small after normalization by contemporaneous standing stock (6.74 versus 6.22 per 100 measured records). Neither exploratory group contrast is strongly resolved by the 13-plot exact comparison. This does **not** prove that recruitment changes arise from fewer adults, because adult and seedling composition, density dependence, detectability and other mechanisms remain unmeasured.

Second, the observed alive/dead/missing outcomes cannot on their own determine whether fragmentation specifically damages post-emergence survival. The authors' `recorded_sdlg` means a **new seedling found at census**; the archive does not contain initial seed deposition, seed quality, safe-site abundance, seed germination probability or directly synchronized compatible mating. It cannot locate the limiting transition from pollen receipt to seed rain to safe-site recruitment.

Third, a lower mean number of recruits per 0.5-ha permanent plot, a lower true per-seed establishment probability, a weaker mating system and a smaller population growth rate are four distinct hypotheses, not interchangeable descriptions.

The close prior literature matters: Bruna (2002), doi:10.1007/s00442-002-0956-y, experimentally studied fragment–control seed germination and recruitment; Uriarte et al. (2010), doi:10.1890/09-0785.1, modelled seed, dispersal and safe-site limitation; Scott, Uriarte & Bruna (2022), doi:10.1111/gcb.15900, found lagged climatic effects on survival, growth and flowering using this population system. EGWEE does **not** claim these mechanisms or the multi-year design as novel.

The distinctive value for EGWEE is a reproducible **failure-of-inference check**: the same ecological census produces materially different statements about relative survival when 'missing' is conflated with mortality, and absolute recruitment contrasts partly reflect the denominator chosen. This guards the prospective hypothesis: a fragmentation-specific shift in the *limiting biological stage* requires stage-matched biological and observation models, independently replicated habitat units, and interventions evaluated on final recruits rather than on a convenient early indicator.

## Reproduction and limits

Executable source-pinned script: `scripts/analyze_heliconia_census_panel.py`. Separate CI workflow: `.github/workflows/heliconia-external-stage-audit.yml`. Each source blob is checked against its git SHA; the script requires 13 plots, 66,396 rows, 8,586 plants and 3,464 new-seedling flags, refuses duplicate identities and missing follow-up plot censuses, and computes plot-label permutations with ranch restriction as a sensitivity. CI publishes an exploratory JSON artifact, **not a new meta-analysis effect table**.

The university publication and raw repository request acknowledgement of the Bruna data paper, Dryad archive, and a BDFFP Technical Series Number for any new publication. Do not use this note to imply independent biological replication with Uriarte's 2010 seed-arrival experiment, because the study regions overlap.
