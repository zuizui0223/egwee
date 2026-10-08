# External Heliconia longitudinal audit: recruitment denominator and missingness
Date: 2026-10-08. Status: **post hoc exploratory replication and claim-limit audit**, not an addition to frozen EGWEE quantitative denominators or a confirmed ecological mechanism.

## Data and exact provenance
- Public source: BrunaLab/HeliconiaSurveys, `data/survey_archive/HDP_survey.csv` (Git blob `f82a6f241493a979a2923d1c5deef6a1be0ff3ed`) and `HDP_plots.csv` (`6fc835fb870d8c43ae4a4fcf04d515f419e6db22`).
- Bruna et al. (2023) data paper, *Ecology*, doi:10.1002/ecy.4174.
- The independently verified source has **66,396 plant-year records**, **8,586 distinct tagged plant IDs (within plot)**, **3,464 newly recorded seedlings**, and **13 independent 0.5-ha plots**: six continuous forest, four 1-ha fragments, three 10-ha fragments.
- For a strictly matched one-year follow-up, restrict new-seedling cohorts to **1999–2005** inclusive, with annual next-year states 2000–2006 available for all 13 plots. These **2,590 seedlings** comprise 1,551 in continuous forest and 1,039 in fragmented plots. We never treat seedlings, plant-years, or seasons as independent fragmentation replicates.
- Reproducible verification: `python scripts/audit_heliconia_recruitment_denominators.py`; verifies both upstream immutable Git blob hashes before parsing, enumerates all 1,716 seven-versus-six plot-label partitions, outputs `build/heliconia_external_audit/summary.json` and `per_plot.csv`. CI run 37779531015 passed.

## Exploratory plot-level contrasts (same 1999–2005 cohort window)
| Quantity (equal weight per independent plot) | Continuous (6) | Fragment (7) |
|---|---:|---:|
| New seedlings per plot per year | 36.929 | 21.204 |
| New seedlings / measured plant-year standing stock | 0.068793 | 0.066389 |
| Next-year survival, among known alive/dead records (pooled over seedlings for descriptive rate) | 1186/1400 = 0.8471 | 829/968 = 0.8564 |
| Next-year missing (not dead) | 151/1551 = 0.0974 | 71/1039 = 0.0683 |
| Initially missing, subsequently observed alive at least once (through 2009) | 91 | 25 |

Exact **plot-label enumeration reference**, treating 13 plot summaries as units (two-sided, 1,716 partitions): absolute new-seedling count contrast = -15.7245 per plot-year, `p=0.26457`; new-seedlings-per-measured-stock contrast = -0.002404, `p=0.83800`. This is not a design-randomization p-value nor a causal test; landscape selection, initial density, and environmental heterogeneity may violate label-exchangeability.

### Missingness changes the interpretation
The observed next-year living proportion under a pessimistic coding that treats *all unknowns* as non-survivors is 1186/1551 = 0.7647 in continuous versus 829/1039 = 0.7979 in fragmented habitat. An optimistic treatment of all missing as alive gives 1337/1551 = 0.8620 versus 900/1039 = 0.8662. Both are **simple bounding sensitivities**, not survival estimates. Crucially, at least 91/151 initially missing continuous-forest seedlings and 25/71 initially missing fragment seedlings are documented alive in a later survey; therefore `missing == dead` is demonstrably false. Counts of reappearances have unequal post-cohort surveillance (FF-7 ends 2006, FF-5 and FF-6 lack 2007), so reappearance fractions cannot be directly compared as equal-effort detection probabilities. Prefer a formal multistate observation model if mortality claims become the target.

### Denominators are not interchangeable
The observed contrast in absolute count could follow differences in pre-existing stand size rather than per-capita production. Scaling by *measured stock* removes the contrast in this descriptive audit, but the stock contains all stages including new seedlings, varies through time, and is an endogenous denominator. It does **not** recover plant fecundity, per-seed germination, number of effective maternal plants, seed rain, or opportunity area. In particular this result does not contradict experiment-based evidence of reduced germination under fragmentation.

For transparency, the 1-ha fragment subgroup had 12.46 new seedlings per plot-year and mean per-stock recruitment 0.05813 (four plots); the 10-ha subgroup had 32.86 and 0.07741 (three plots). These exploratory subgroup differences are not an independent second experiment.

## Distinct predictor test: 1998 standing legacy vs fragmentation label

A further **post hoc** comparison predicts mean annual observed new seedlings in 1999–2005 from the *pre-outcome* 1998 number of alive/measured plants in each 0.5-ha plot, the fragment/continuous label, or both. Plot-level Pearson correlation between 1998 standing stock and later annual seedlings is **r=0.9047 (13 plots)**. On ordinary untransformed observed-seedling-count scale, with equal plot weights, linear regression gives:

| Predictor | Leave-one-plot-out MSE | Leave-one-ranch-out MSE |
|---|---:|---:|
| Intercept only | 660.72 | 1132.08 |
| Fragment label only | 713.03 | 1318.11 |
| 1998 standing stock only | **131.36** | **248.89** |
| 1998 standing stock + fragment label | 150.63 | 280.36 |

The leave-one-ranch-out design holds out **all plots** within each of three geographically defined ranch groups (Esteio, Dimona and Porto Alegre); it is a more stringent transfer sensitivity than leaving out one neighbouring plot, but comprises only three held-out groups. A ranch-preserving plot-label enumeration fixes the observed count of fragments per ranch (Esteio 2/5, Dimona 3/4, Porto Alegre 2/4). Across **240** possible within-ranch assignments, the mean absolute-new contrast gives a descriptive two-sided label probability of **0.2375**, and the stock-normalized contrast **0.79583**.

**Critical causal warning:** the 1998 stock was surveyed many years **after** experimental forest isolation in the 1980s, so it is *not* a pre-fragmentation covariate. Stock can be an ecological **mediator of historical fragmentation effects**, as well as a predictor of later seedling abundance. Adjusting for it can remove real long-run fragmentation effects. Therefore, the stock-only predictive advantage does **not** establish zero fragmentation effect or justify adjusting it away in causal analyses. The improved out-of-ranch MSE is an exploratory prediction comparison, not a causal intervention or predeclared generalization test. Counts also conflate reproductive adults, seed input, safe-site availability, year effects, and detection.

**Sharper forward question:** across comparable fragmented systems, what fraction of observed recruitment deficit is attributable to (a) legacy reproductive-plant supply, (b) conditional seed-to-seedling establishment and (c) safe-site coverage? With maternal identity, seed counts, safe-site mapping and randomised stage-specific supplementation, ask whether a source-population-based predictive model gains independent, held-landscape accuracy from current stage physiology and whether that improvement identifies the treatment that increases recruits. The Heliconia observational census alone cannot partition these causal contributions.

## Nearest prior work and actual novelty ceiling
- **Bruna (2002), doi:10.1007/s00442-002-0956-y**: an experimental seed recruitment comparison reported 3–7 times lower establishment in fragments; lower germination implicated. This is *stronger causal evidence of a process* than our observational annual seedling count.
- **Bruna & Oli (2005), doi:10.1890/04-1716**: LTRE already demonstrated that approximately similar reductions in population growth rate can be attributable to *fertility* in 10-ha fragments and *fertility plus plant growth* in 1-ha fragments. We cannot claim to discover habitat-dependent demographic bottlenecks in Heliconia.
- **Uriarte et al. (2010), doi:10.1890/09-0785.1**: explicit seed supply / dispersal / safe-site models found safe-site limitation central.
- **Scott, Uriarte & Bruna (2022), doi:10.1111/gcb.15900**: delayed climatic effects on survival, growth and flowering and fragmentation-specific climate sensitivity were already identified with the long-term record.

**No novel ecological conclusion is certified by this reanalysis.** The nontrivial finding is a *denominator and observation-process warning within a linked original field dataset*: fewer observed new seedlings per plot, roughly equal new-per-standing-stock and known-status first-year survival, and substantial subsequent reappearance of seedlings initially recorded as missing. A mechanistic claim about why this occurs requires separate measures of seed production, seed arrival, germination safe sites, detection probability, and maternal identity.

## Forward falsifiable target, not a retrospective result
The distinct EGWEE target remains whether the **most severe standing life-stage attrition**, the **fragmentation-associated alteration in transition rates**, and the **stage-specific intervention with maximal net recruitment payoff** are the same. Existing Heliconia evidence demonstrates the first two can differ and offers useful priors; it does *not* independently randomize the rescue interventions on a common downstream recruits-per-area denominator. A genuinely novel ecological test would factorially improve mating/provenance, seed arrival and microsites in replicated landscapes; measure propagule-level fate and the area of each safe-site state; hold out entire landscapes; and precommit comparisons against simpler single-limitation models.

## Corpus protection
No observation from this archive is added to the five direct EGWEE clusters, the eight matched I–F programmes, the 16-programme qualitative map or the external SF06 sign-pair denominator. All results remain explicitly post hoc. Any paper title asserting a novel universal stage switch is disallowed.
