# Independent external longitudinal audit: Heliconia acuminata (1998–2009)

**Status:** post hoc exploratory, source-pinned, noncausal. This is an external test of the EGWEE *interpretation boundary*, not a sixth primary cluster, not an I–F matched programme, not an independent replication of prior publications using these same plots, and not a proof of stage relocation.

## Data and independent unit

Raw source: [BrunaLab/HeliconiaSurveys](https://github.com/BrunaLab/HeliconiaSurveys), repository revision `0b999f6bcb47df1c31f0dd0a8b472055b5f81bc0`; archived table blob `f82a6f241493a979a2923d1c5deef6a1be0ff3ed`; plot metadata blob `6fc835fb870d8c43ae4a4fcf04d515f419e6db22`. Data paper: Bruna et al. 2023, *Ecology*, doi:10.1002/ecy.4174; Dryad: doi:10.5061/dryad.stqjq2c8d.

CSV records: **66,396 plant-years, 8,586 unique plot/plant IDs, 3,464 marked new seedlings**, across **13 permanent 0.5-ha plots**, 6 continuous forest (CF), 4 in 1-ha fragments, 3 in 10-ha fragments. Plot—not plant-year, seedling, fragment-size group or ranch-year—is the analysis replication unit. The same biological plots were used in earlier demographic publications.

Use **1999–2006**, when all 13 plots have annual censuses, with prior-year 1998–2005 observed plant counts as the denominator. Years 2007–2009 have uneven plot coverage; do not silently treat missing whole-plot years as zero recruitment.

## First derived contrast: density versus recruitment

Means are **equal weight across sites**, not pooled plant-years.

| Derived site-level measure, common window | Continuous (6 plots) | Fragmented (7 plots) | FF / CF |
|---|---:|---:|---:|
| New seedling records per plot-year | 35.02 | 20.25 | 0.578 |
| New seedlings / previous census measured plants | 0.07047 | 0.06667 | 0.946 |
| Newly marked seedling survival next year, conditional on observed alive/dead | 0.84996 | 0.85821 | 1.010 |

The raw new-seedling plot count differs by about 42%, but the plot-level mean `new seedlings / previous year's measured individuals` differs by about 5%. The latter is **not a fecundity, fertilization, germination or per-reproductive-adult rate**: previously measured individuals include nonreproductive stages and other life-history classes. A density-standardized observational ratio is not a causal effect and is not guaranteed to be stable under treatment-induced abundance.

An exhaustive two-sided label-allocation comparison at **13-plot level** (7/6 assignments, 1,716 combinations) gives p≈0.749 for that density-index mean difference. Holding label counts fixed within the three ranches yields 240 allocations and p≈0.721. These are *descriptive allocation sensitivities*, not randomization-based causal p-values; true treatment allocation, fragment size, ranch and baseline density are not fully exchangeable. Non-rejection is not equivalence.

## Hidden censoring: missing is demonstrably not dead

For annual plant records with status `missing` in 1998–2005, **1,339 of 3,169** have status `measured` the next year. Among **210** new seedlings observed as `missing` one year after first recording and followed a further year, **100** were again measured. Thus assigning `missing=dead` would classify later confirmed survivors incorrectly.

The difference in unknown follow-up is itself landscape- and plot-dependent: the one-year missing fraction among newly observed seedlings is especially large in CF-4, CF-5 and CF-6 (approximately 32%, 34% and 71%, respectively, for the 1999–2005 birth window). The above *known-status* survival values condition on ascertainment and must **not** be read as unbiased survival estimates. Report plot-wise lower bound `confirmed_alive / total` and upper bound `(confirmed_alive + missing) / total` and consider observation/survival modeling in any formal analysis. Presence after a missing year shows non-absorbing observations, not absence of genuine mortality.

## Temporal contrast: suggestive reversal, not established

The site-mean density-index ratio changes from early (1999–2002) to late (2003–2006):

- Continuous forest: **0.10812 → 0.04151**.
- Fragmented forest: **0.08234 → 0.05498**.

This switches which treatment class has the higher raw site-mean index, yet the *difference in period changes* is only ≈ +0.0393 per previous measured plant; unstratified 13-site exhaustive-label p≈0.217, ranch-conditioned p≈0.242. These were selected after inspecting the series; they are not predeclared change points. The trends may be affected by changing population size, source/sink dynamics, climate, time-since-isolation, density dependence or yearly observation. No abrupt ecological shift or causally identified demographic bottleneck switch is claimed.

## Closest prior art — prevents misleading novelty

- **Bruna (2002)**, doi:10.1007/s00442-002-0956-y: experimentally compared seedling recruitment and reported lower natural seedling counts in fragments and strongly reduced seed establishment after sowing; key earlier fragmentation observation is already known.
- **Bruna & Oli (2005)**, doi:10.1890/04-1716: life-table response experiments on overlapping Heliconia plots estimated similar lambda near one for both 1-ha and 10-ha fragments while resolving *different component contributions* to reduced lambda. Thus **'similar demographic outcomes arise from different stages' is already demonstrated in this species**.
- **Uriarte et al. (2010)**, doi:10.1890/09-0785.1: modeled seed supply versus safe-site limitation in this same species/landscape. This is related provenance, not an independent species replication.
- **Scott, Uriarte & Bruna (2022)**, doi:10.1111/gcb.15900: identified climate effects delayed up to 36 months on demographic vital rates, with fragmentation modifying environmental sensitivity. A time contrast without weather history cannot establish a new biological mechanism.
- **Bruna et al. (2023)**, doi:10.1002/ecy.4174: source data paper, same long-term series.

## Next defensible ecological test

Use a *source-disjoint* population series from another species and biome with both marked cohorts and survey effort (or explicit detection observations), and predeclare: (1) baseline attrition, (2) the fragmentation-associated change in a transition and (3) actual recruit gains from intervention as separate estimands. Try to predict external patch-level recruitment trajectories **out of publication**, not merely fit the Heliconia outcome already in hand.

All results here are hypothesis-generating external data-context checks and do **not** change the five direct clusters, eight quantitative I–F systems, 16-programme translation topology, SF06 pair denominator, or submission-ready flag.

## Reproduction

Run `python scripts/audit_heliconia_longitudinal_external.py --out build/heliconia_longitudinal_external.json`. Script downloads the immutable public CSV/plot metadata, verifies both Git blob SHAs, checks duplicate plot/plant/year keys, and outputs per-plot series and exhaustive allocation sensitivities. The isolated GitHub Actions workflow produces the JSON artifact without bypassing any current publication freeze.
