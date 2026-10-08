# Heliconia population census: plot-level recruitment versus detected survival

**Status:** post hoc exploratory reanalysis; **not** a new EGWEE independent programme for the primary direct-effects/IF/SF06 corpus, and not a new causal claim. Source: Bruna et al. (2023) *Ecology* data paper (doi:10.1002/ecy.4174), [Dryad dataset](https://doi.org/10.5061/dryad.stqjq2c8d), [BrunaLab/HeliconiaSurveys](https://github.com/BrunaLab/HeliconiaSurveys), archived [HDP_survey.csv](https://github.com/BrunaLab/HeliconiaSurveys/blob/master/data/survey_archive/HDP_survey.csv) and [HDP_plots.csv](https://github.com/BrunaLab/HeliconiaSurveys/blob/master/data/survey_archive/HDP_plots.csv). Exact Git blob hashes are pinned in `scripts/check_heliconia_plot_demography.py`.

## Biological question and design

Do continuous-forest and fragmented-forest plots differ in observed new seedling detections because of per-area recruitment, pre-existing standing plant abundance, or first-year apparent survival?

The archive has 66,396 plant-year records from 8,586 distinct plotted individuals, including 3,464 marked new seedlings across 1998–2009, in six continuous-forest and seven experimentally isolated-fragment **0.5-ha census plots**. Four fragments are 1-ha habitat remnants and three are 10-ha remnants, but **each actual census plot has the same 0.5-ha area**. The three source ranches are Esteio, Dimona, and Porto Alegre.

Use birth/detection cohorts **1999–2005**, allowing observed subsequent censuses for all 13 plots during **2000–2006**. Exactly 2,590 unique first-observed seedlings qualify. `recorded_sdlg=TRUE` is a **first recorded seedling**, not a denominator-complete germination event. `census_status=missing` is neither confirmed death nor confirmed survival. Distinct plant-year records are not independent plot replicates.

Plot-level metrics:
1. newly detected seedlings per plot-year (seven fully observed recruitment years, 0.5 ha each);
2. detections per 100 lagged `measured` plant-years, using same-plot counts in years 1998–2004 as a **descriptive denominator**, not a treatment-adjusted causal effect;
3. known-status next-year survival `measured/(measured+dead)`;
4. extreme bounds `measured/(measured+dead+missing)` (unknown all dead) and `(measured+missing)/(measured+dead+missing)` (unknown all alive).

The `measured` denominator includes reproductive and nonreproductive plants; it is **not** adult breeding-plant density. No pollen/mating variables are observed on these frames. A group difference between sites within the BDFFP landscape is not automatically the experimental causal fragmentation effect.

## Complete plot-level permutation audit

Means are **equal-plot-weighted**, not pooled proportions over thousands of seedlings. The nominal two-sided test enumerates all C(13,7)=1,716 FF/CF plot assignments. An additional *ranch-constrained* test preserves the number of fragment labels in each ranch (10 x 4 x 6 = 240 assignments). Both treat plots as the inferential unit; neither is a fully randomized-forest experiment design analysis, and all contrasts were inspected post hoc.

| Plot-level estimand | CF mean (n=6) | FF mean (n=7) | Unrestricted p | Within-ranch p |
|---|---:|---:|---:|---:|
| New seedlings per 0.5-ha plot-year | 36.9286 | 21.2041 | 0.26457 | 0.23750 |
| New seedlings per 100 lagged observed plant-years | 7.2518 | 7.1910 | 0.96678 | 0.97083 |
| Next-year survival among known-status seedlings | 0.84996 | 0.85821 | 0.65443 | see generated JSON |
| Next-year survival lower bound (all missing dead) | 0.63480 | 0.80353 | 0.05361 | see generated JSON |
| Next-year survival upper bound (all missing alive) | 0.88708 | 0.86738 | 0.40734 | see generated JSON |

Confirmed status among eligible seedlings:
- CF: 1,186 measured/alive, 214 dead, 151 missing, total 1,551.
- FF: 829 measured/alive, 139 dead, 71 missing, total 1,039.

**Reading the results correctly:** visible per-area recruitment is lower on average in fragments, but not rejected by a coarse 13-plot permutation test. Standardizing by lagged plant abundance makes the plot means very close. That normalization *conditions on standing abundance*, which can itself have been changed by earlier fragmentation and other site conditions; it may eliminate precisely the population-size component of a long-term fragmentation signal. It neither demonstrates unchanged seed-to-seedling transition probabilities nor refutes seed/safe-site effects.

First-year conditional-on-known survival is similarly close. But the missingness fraction is quite heterogeneous, with CF-6 alone having 51 unknown of 72 eligible seedlings. Extreme missing-outcome assumptions change the FF–CF difference from positive (unknown all dead) to negative (unknown all alive). **Do not claim survival is unaffected, or that the conditional comparison identifies a common vital rate.** Outcome ascertainment and year-dependent drought could select the observed individuals.

## Verified reappearance after a missing census

The apparent-survival caveat is not hypothetical. Restricting entry to **1999–2004** makes both the +1 and +2 subsequent census available in every plot through 2006. Of the first-census incident seedlings that were recorded as `missing` at +1, the next census at +2 contains:

| Initial habitat | Incident seedlings 1999–2004 | Missing at +1 | Found alive at +2 | Recorded dead at +2 | Still missing at +2 |
|---|---:|---:|---:|---:|---:|
| Continuous forest (six plots) | 1,437 | 146 | **81** | 22 | 43 |
| Fragmented forest (seven plots) | 932 | 64 | **19** | 10 | 35 |
| **Total** | **2,369** | **210** | **100** | 32 | 78 |

Thus **100/210 (47.6%)** of the initially missing seedlings were *subsequently alive*, demonstrating directly that the `missing` category cannot be mapped to mortality. The raw post-missing reappearance proportions (81/146 versus 19/64) differ across habitats but are conditional on being missing; without a detection model, they are **not estimates of habitat-specific survival or detection probability**. Different plant densities, observer detection and plot conditions can select distinct missing subsets. Even `measured/(measured+dead)` conditions on ascertainment and may be biased. A principled next model requires separating a latent alive state from plot/year observation probability and accounting for recorded deaths and later reappearances.

## Habitat-size and sensitivity warnings

The four 1-ha fragment plots average 12.46 newly detected seedlings per plot-year; the three 10-ha fragment plots average 32.86; continuous plots average 36.93. One-ha-versus-10-ha exact permutation is p=0.0857 (35 assignments), exploratory and extremely low-powered. Lagged-abundance-normalized means are 6.26, 8.43 and 7.25 per 100 plant-years, respectively. These are **three observational groups**, not 13 independently randomized landscapes. In the 13-plot leave-one-plot-out exercise, the sign of the raw mean difference remains negative; the sign of the abundance-normalized difference flips depending on which plot is removed.

## Prior-art boundary and what would actually be new

Bruna (2002; doi:10.1007/s00442-002-0956-y) already reported reduced natural seedling establishment in 1- and 10-ha fragments, with controlled experiments indicating an important germination/microclimate pathway. Bruna (2003; doi:10.1890/0012-9658(2003)084[0932:APPIFH]2.0.CO;2) **already tested recruitment limitation against whole-population persistence with a matrix model using 13 Heliconia populations**, so even linking seedling recruitment to demographic vulnerability is not new for this taxon. Scott, Uriarte & Bruna (2022; doi:10.1111/gcb.15900) already analysed delayed precipitation/climate effects on survival, growth and flowering, finding stronger weather-extreme effects in forest fragments. **Our coarser across-years one-year summary cannot negate those findings** and is not novel proof of a stage-switching mechanism. Also note the data describe 12 annual census labels (1998–2009 inclusive) although the original data paper calls it 11 years of demographic data.

What the reanalysis newly contributes to this *EGWEE audit*, not necessarily to published ecology, is a reproducible distinction between: (a) per-plot recruitment counts, (b) counts conditional on potentially fragmentation-affected standing population, and (c) survival conditional on being subsequently found and classified. A new general ecological result would require replicated measurement of *fragmentation-specific changes in stage transition rates* and a prospective independent prediction of the stage-specific treatment that rescues lifetime recruitment. Current data cannot test pollen-transfer provenance or missing microhabitat availability, so they do not identify an upstream I→E→F mechanism.

## Reproduction and stop rules

Run `python scripts/check_heliconia_plot_demography.py --output build/heliconia_plot_demography.json` from an online environment, or `--local-dir PATH` with both original files. The script verifies upstream Git blob hashes, source row/plant/seedling counts, absence of duplicate plant-years, 13 complete cohort follow-up windows, the nominal exact permutation p-values, and the ranch-restricted new-seedling result. The dedicated workflow produces a JSON artifact.

No new result from this exercise is added to the frozen five-cluster direct-family denominator, the eight matched I–F programmes, the 16-programme translation map, or the external SF06 denominator. The 2002, 2010, 2022 and 2023 Heliconia outputs are linked parts of the **same broader experimental landscape and research programme**, not independent confirmations of the same finding.
