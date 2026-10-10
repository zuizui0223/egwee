# Heliconia 2002–2003 reproduction-to-recruitment pulse: observation and weather timing falsification (2026-10-10)

## Status and ecological question

**Empirical egwee**, not theoretical egwe. Exploratory source-audited reanalysis of **one previously published** BDFFP / *Heliconia acuminata* study system (Bruna et al. 2023, *Ecology*, doi:10.1002/ecy.4174, https://doi.org/10.5061/dryad.stqjq2c8d). **No added programme** to the frozen five-cluster direct effects, eight matched I–F programmes, 16-programme evidence map, or the SF06 external corpus. Neither a new universal biological law nor a causal analysis is claimed.

Previous source-hash-verified analysis found that earlier living plant stock predicted recruitment across held-out ranches in the same year but **failed in forward-year prediction**. A repeated-panel pulse was visible between **2002 and 2003**, even though existing living stock increased. The present follow-up tests two simpler competing explanations: **lower detection of previously tagged individuals**, and **lower documented flowering in the preceding year**; it also checks the **time order** of public regional meteorological data rather than inadvertently explaining an early census with precipitation falling later in the year.

## Source pin and unit of analysis

Annual source archive: `BrunaLab/HeliconiaSurveys` Git commit `0b999f6bcb47df1c31f0dd0a8b472055b5f81bc0`, 66,396 individual-year records, 13 plots across three ranch contexts, 8,586 plant IDs, 3,464 first-recorded seedlings across 1998–2009. The read function validates the pinned upstream blob SHA for both original CSVs, and the analysis additionally audits unique plant × plot × year observations.

Ten plots have admissible census coverage throughout the five-year comparable window: `CF-1`, `CF-2`, `CF-3`, and `FF-1` through `FF-7`. `CF-4/CF-5` in 2000 and `CF-6` in 2003 have wholly `missing` plant-status rows and remain excluded from overlapping lagged exposure/outcome windows. The ten plots (and their three ranches) are the repeated units; hundreds of measured plants are **not extra spatial replicates**.

## Exact repeated-site descriptive result

For year `t` outcome, the reproductive proxy is the number of plants with **recorded positive inflorescence counts in t-1**. A missing `infl` field is not a certified zero; this proxy is not realized pollen transfer, seed set, individual mother–seedling linkage, or fecundity.

| Same ten plots | 2002 newly recorded seedling outcome (2001 exposure) | 2003 outcome (2002 exposure) |
|---|---:|---:|
| Previously measured living plants per plot | 455.0 | 498.8 |
| Documented flowering plants per plot in t-1 | 23.6 | 11.6 |
| Documented inflorescences per plot in t-1 | 26.6 | 12.7 |
| First-recorded new seedlings per plot | 44.5 | 14.1 |
| Previously living plants with a next-year *verified status* (alive or recorded dead; pooled) | 4420 / 4550 = **97.143%** | 4787 / 4988 = **95.970%** |
| Recorded seedlings / previously documented flowering plant (aggregate bookkeeping only) | 1.8856 | 1.2155 |

- Positive inflorescence/flowering-individual counts declined in **10/10** identical plots, and newly recorded seedlings declined in **9/10**.
- The flowering count fell **50.85%**; seedlings recorded fell **68.31%**; previously measured total living stock rose **9.63%**.
- Previously tagged individuals' measured-or-dead **status ascertainment** slipped by **1.17 percentage points** pooled, with declines in 6/10 plots. This does **not** quantify detection of first-appearing seedlings, but a universal across-plots old-plant detection collapse is not evident.
- As an observational *algebraic* factorization, `R_03/R_02 = (Fl_02/Fl_01) * [(R_03/Fl_02)/(R_02/Fl_01)] = 0.4915 * 0.6446 = 0.3169`. This is **not an estimated 50.8% flowering-caused loss and 35.5% downstream-caused loss**. Maternal cohorts and survey effort are unmatched, dispersal and seed banks exist, and the ratios do not identify stage-specific vital rates.

### Crucial cross-context heterogeneity

Across the **same ten plots** partitioned by ranch:

| Ranch | Plots | Flowering ratio (t-1): 2002/2001 | New recruits ratio: 2003/2002 | Recruits-per-flower bookkeeping ratio |
|---|---:|---:|---:|---:|
| Dimona | 3 | 0.400 | 0.571 | **1.429** |
| Esteio | 5 | 0.470 | 0.313 | **0.666** |
| Porto Alegre | 2 | 0.569 | 0.260 | **0.457** |

**Both flowering and recruit records fell in all three regions, but their *relative* change is not a single universal coupling.** The conditional bookkeeping ratio rises in Dimona and falls in Esteio and Porto Alegre. This is a candidate for within-stage reproductive/establishment heterogeneity **or** different phenology/observation lags, not a confirmed physiological transition.

A strong local falsification of simple old-plant ascertainment explains the continuous-forest subset: in its three retained plots, verification of previously measured live individuals is **97.576% → 97.665%**, essentially unchanged, whereas newly recorded recruits are **96.33 → 26.33** and prior documented flowering falls **46.67 → 19.33** per plot. Newly appearing seedling detection could still change independently of tagged-plant detection. Never promote this to proof of a biological recruitment decline free from detection bias.

## Independent regional climate lookup: enforce observation chronology

A separate live NASA POWER/MERRA-2 **monthly grid point**, **latitude −2.5, longitude −60.0** (approximate BDFFP area rather than exact ranch/plot location), gives the following *regional proxy*:

| Calendar year | Full annual precipitation, mm | Jan–May precipitation, mm | Annual mean air temperature, °C |
|---|---:|---:|---:|
| 2001 | **2261.59** | **1386.97** | **25.707** |
| 2002 | **2249.81** | **1425.28** | **25.940** |
| 2003 | **1877.14** | **997.25** | **25.938** |
| 2004 | 1802.84 | 1081.69 | 26.071 |
| 2005 | 1479.03 | 845.21 | 27.322 |

POWER's `PRECTOTCORR` is provided as average daily monthly precipitation; the extraction integrates each monthly value by its correct number of calendar days. The raw downloaded JSON SHA-256, point and parameter units are retained in the archived machine-readable result, rather than claiming this is direct on-plot rain gauge data. Source/API documentation: https://power.larc.nasa.gov/docs/services/api/temporal/monthly/.

**Strictly previous calendar-year exposure for the two compared recruit years** is 2001 versus 2002 rainfall: **2261.59 vs 2249.81 mm**, just **−0.52%**; previous year's Jan–May precipitation actually rose **1386.97 → 1425.28 mm (+2.76%)**. Thus the 68% recruit-entry drop cannot be directly relabelled as a corresponding simple **previous-calendar-year annual rainfall shortage**. That does **not** refute microclimate, SPEI, drought extremes, season-specific windows, nonlinear thresholds, source location differences, earlier lags, or other climate controls.

The lower **full-year 2003** rainfall **is not a valid “before the 2003 census” predictor** unless exact source site/year survey dates show that all those months precede the observations. Scott, Uriarte & Bruna (2022, *Global Change Biology*, doi:10.1111/gcb.15900) refer to a **February census** in this system and reported climate effects with lags up to 36 months. This archive supplies *year labels but no plot-specific dates*, so there is a potentially severe **temporal information leakage** if a 2003 January–December (or January–May) climate metric is used to explain/predict a February 2003 demographic outcome. We therefore present current-year rainfall as **context only**, not a prospective exposure. The full 2003–2005 climate trajectory is **not** new evidence of a climate cause of that year's censused recruits.

## Relation to prior biological literature

- Bruna (2002, *Oecologia*, doi:10.1007/s00442-002-0956-y) already experimentally implicated altered germination/establishment under fragmentation. Our reanalysis does not discover that safe-site pathway.
- Scott, Uriarte & Bruna (2022, *Global Change Biology*, doi:10.1111/gcb.15900) already demonstrated delayed climate effects on *Heliconia* survival, growth and flowering in this system. Thus neither climate sensitivity nor phenological memory is newly established here.
- The new **project-specific evidence qualification** is precise: the same-site reduction in recorded recruits overlaps a universal reduction in previously documented flowering, *not* an equally large reduction in old-plant fate verification; the observed translation is ranch-heterogeneous; and same-year gridded climate contains months not assured to precede the field census.

## What would decisively discriminate the explanations

An **independent prospective**, same-plot-year and cohort-level design must observe:
1. Actual census date, flowering survey effort and fraction of initial/new seedlings detected, ideally with repeated visits/mark–recapture.
2. Number of reproductive adults, viable pollen/donor provenance, seeds and dispersal/arrival opportunity; link mother cohorts or experimentally marked seeds to recruit outcomes.
3. Measured seed safe-site abundance, germination microsite properties and regional **pre-census** weather at biologically specified lags (SPEI and extreme events, not only annual rainfall).
4. Previously declared prediction at independent landscape and future-year levels, plus randomized stage interventions when feasible, with whole-patch recruit yield as fixed conservation endpoint.

**Do not claim** independent natural replication, a unique climatic cause, true recruitment detection equivalence, a causal 2-stage decomposition, seed-bank duration, or a universal stage-switch law from these ten correlated plots.

## Reproducibility

- Plant individual-ID fate confirmation: `scripts/audit_heliconia_recruitment_detection_competitor.py` — source-hash-verified, GitHub Actions PASS: https://github.com/zuizui0223/egwee/actions/runs/38057773889.
- NASA public-region climate time gate: `scripts/audit_heliconia_regional_climate_context.py` — point and response SHA-256 recorded, GitHub Actions PASS: https://github.com/zuizui0223/egwee/actions/runs/38058005341.
- Prior held-future-year baseline: `scripts/audit_heliconia_forward_lag_prediction.py`, https://github.com/zuizui0223/egwee/actions/runs/38046390486.
- These exploratory audits **do not alter the frozen EGWEE denominators, claimed universal mechanisms, preregistered tests or submission readiness**.
