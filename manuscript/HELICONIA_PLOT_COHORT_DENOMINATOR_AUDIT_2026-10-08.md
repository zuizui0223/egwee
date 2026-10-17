# Heliconia plot-level cohort / denominator / missingness audit (2026-10-08)

**Status:** exploratory post-exposure same-source reanalysis, not a new independent replication. Biological system: *Heliconia acuminata*, BDFFP near Manaus. Empirical EGWEE, **not** the theoretical EGWE/NEE repo.

## Data lineage and independent unit

- Bruna et al. (2023) public demographic data: https://github.com/BrunaLab/HeliconiaSurveys/blob/master/data/survey_archive/HDP_survey.csv
- Original source Git blob: `f82a6f241493a979a2923d1c5deef6a1be0ff3ed`. Associated plot metadata: `data/survey_archive/HDP_plots.csv`. The README documents 66,396 plant-year rows, 8,586 unique plants and 3,464 `recorded_sdlg=TRUE` individuals.
- Thirteen **0.5 ha plot-level units**, not 13 independently randomized landscapes and certainly not 66,396 or 2,590 fragmentation replicates; six continuous-forest plots, four 1-ha-fragment plots and three 10-ha-fragment plots, nested within three ranch/geographic contexts. CF-2 and CF-3 share reserve no. 1501, so landscape exposure independence is **less** than 13 and all permutation p-values remain explicitly descriptive.
- Balanced early cohort frame: newly recorded seedlings in 1999–2005; their *next* census is in 2000–2006, preceding the missing late annual censuses for FF-5/FF-6 (2007) and FF-7 (2007–2009). A later census does not guarantee exact yearly measurement.
- The source-derived 13-row frozen table is `evidence/meta_extraction/heliconia_plot_cohorts_1999_2005_v1.csv`; deterministic source-to-plot calculations are specified by those columns and the source Git blob. Exact audit: `scripts/check_heliconia_plot_recruitment_audit.py`.
- Independent raw-data reconstruction is implemented in `scripts/rebuild_heliconia_plot_cohorts.py`. Download the original `HDP_survey.csv` and `HDP_plots.csv` at the blob revisions noted above and run `python scripts/rebuild_heliconia_plot_cohorts.py --survey /path/HDP_survey.csv --plots /path/HDP_plots.csv`; the script verifies both Git blob hashes and compares all 13 derived rows without overwriting them.
- The input `census_status` labels are `measured` (observed alive), `dead` (observed dead), and `missing` (not found); **missing is not dead**.

## Explicitly competing demographic estimands

These are **distinct questions**, not alternative normalizations of one invariant treatment effect.

| Outcome, equal weight per independent plot | Continuous forest (6) | Fragments pooled (7) | Unstratified label-permutation p | Within-ranch p |
|---|---:|---:|---:|---:|
| Newly recorded seedlings / 0.5 ha plot / year | **36.93** | **21.20** | **0.2646** | **0.2375** |
| Seven-year new seedlings / 1998 baseline live individual | **0.631** | **0.829** | **0.3934** | **0.3042** |
| Newly recorded seedlings / observed living plant-year in 1999–2005 | **0.0688** | **0.0664** | **0.8380** | **0.7958** |
| Next-census survival among seedlings with *known* status, equal plot mean | **0.8500** | **0.8582** | **0.6544** | **0.5667** |
| Next-census alive / all eligible seedlings (all missing assumed dead, extreme lower bound) | **0.6348** | **0.8035** | **0.0536** | **0.0208** |
| (Next-census alive + missing) / all eligible (all missing assumed alive, extreme upper bound) | **0.8871** | **0.8674** | **0.4073** | **0.3500** |
| Next-census unknown fraction | **0.2523** | **0.0638** | **0.0688** | **0.0417** |

**Counts:** 2,590 recruit individuals from 1999–2005 (1,551 continuous, 1,039 fragmented). At the next census, continuous plots: 1,186 measured, 214 dead, 151 missing; fragmented: 829 measured, 139 dead, 71 missing. No missing next-census records were coded as death. Importantly, 116/222 missing next-year individuals (91 continuous; 25 fragmented) were later recorded alive, directly refuting automatic missing=dead coding.

The first two estimands **reverse the sign**: area-based absolute recruitment is higher in continuous forest, whereas cumulative 7-year recruitment *per baseline 1998 live plant* is higher in fragmented plots. However, none of these comparisons provides a resolved habitat difference at the 13-plot level, nor does it identify the causal role of density. The 1998 denominator contains observed living plants of different stages, not necessarily reproductive parents. Likewise, dividing by contemporary live plant-years is a density-standardized descriptive rate, not a causal per-capita fecundity estimate.

Permutation tests enumerate 1,716 possible six-versus-seven plot assignments; their within-ranch sensitivity holds continuous/fragment totals fixed within each ranch (240 assignments). These are **diagnostic permutations**, not randomized-assignment p-values: plot placement, correlated environment, historical isolation and ranch context constrain exchangeability.

## Strongest usable ecological interpretation

The originally striking per-area reduction in seedling counts does **not** by itself demonstrate a per-existing-plant recruitment defect. A different denominator changes the sign or nearly eliminates the difference, and known-status next-year seedling survival alone does not reproduce a strong fragment penalty.

The unresolved ecological causal fork is:

1. **Fewer pre-existing plants / propagule sources per equal plot area** causing fewer newly observed seedlings, potentially through density and spatial seed delivery;
2. **Lower germination / safe-site availability per propagule**, independent of reproductive-source abundance;
3. **Phenology, earlier vital rates, or detection differences**, especially when `missing` differs strongly among plots;
4. **Later growth/survival bottlenecks** absent from this first-year contrast.

None can be selected from these descriptive ratios alone. The appropriate next diagnostic needs source-seed supply, vegetation/edge and microhabitat covariates and held-out independent landscapes, not a significance search across denominators.

## Post hoc forward prediction: habitat label versus initial census abundance

A separate, minimal **1998→1999–2005** holdout exercise asks a more concrete diagnostic question: how much of the observed seven-year seedling count in an unseen plot can be predicted from just its initial living-plant abundance, versus the forest-fragmentation category? No new predictors are fitted from future individuals.

| Single-variable forecasting rule | Leave-one-plot-out MSE (seedlings² per plot) | Leave-one-ranch-out RMSE (seedlings per plot) |
|---|---:|---:|
| Training overall mean (no covariates) | 32,375 | 235.5 |
| Training mean for same continuous/fragment habitat | 34,939 | 254.1 |
| Training proportional-through-origin model: recruits = coefficient × 1998 living plants | **5,922** | **118.9** |

This is a **post hoc** model comparison. Initial plant abundance is a much better **predictor** of future *absolute count* than the simple fragmentation label in these 13 plots, but there is no independent held-out landscape beyond the same BDFFP programme. The strong result partly reflects an obvious counting constraint: patches with more living plants have more potential seed sources. It does not identify whether seed delivery, germination/safe sites, fecundity or census detection caused the pattern; it does **not** establish a new mechanistic law.

**Causal warning:** fragmentation dates to 1980–1984, years before the 1998 census. Baseline population size is therefore a **post-exposure state**, potentially a mediator of fragmentation's total effect. Conditioning on it answers a different question and may erase real damage through decreased source-population size. The proper contrast is *total recruits per area* for whole-patch population renewal versus *recruits per historical baseline individual* for conditional production accounting; neither alone proves what intervention is optimal.

A local floral-neighbourhood experiment in this species (Bruna et al. 2004, doi:10.1590/S0044-59672004000300012) found no clear individual reproductive-success effect of manipulating nearby flowering-plant density within the tested range. It does not refute the observed plot-level abundance predictor: local per-flower success, absolute numbers of maternal plants and spatial seed deposition are distinct processes.

Code: `scripts/check_heliconia_density_predictive_value.py`. The project already has stronger life-table stage analyses from Bruna & Oli (2005), so none of the predictor results is claimed as discovery of stage-specific fragmentation mechanisms.

## Critical prior art and novelty limits

This is an **existing heavily studied system**, not an independent discovery of stage-specific effects. Bruna (2002; doi:10.1007/s00442-002-0956-y) already identified lower seedling establishment in fragments and suggested lower germination; Bruna & Oli (2005; doi:10.1890/04-1716) estimated population growth rates and showed similar lambda deficits from distinct processes in 1-ha versus 10-ha fragments. Uriarte et al. (2010; doi:10.1890/09-0785.1) explicitly tested seed supply, dispersal and safe-site limitation, and Scott et al. (2022; doi:10.1111/gcb.15900) demonstrated multi-year climatic lag effects on survival, growth and flowering.

Thus this new audit contributes a reproducible **measurement and inferential check**, not a new ecological stage-switch law. It exposes density-denominator sensitivity and unusually consequential census missingness. The evolutionary/ecological claim would become novel only after a prospectively defined, independently replicated mechanism or restoration response is predicted correctly in new settings.

## Registered stop rules

- Do not merge these estimates into existing 5-cluster/17-effect EGWEE direct synthesis, eight matched I–F programmes, 16-programme translation map, or the SF06 external pair denominator.
- Do not upgrade unstratified permutations to a design-based fragmentation causal test. Do not interpret 0.05-level differences between artificial all-missing-dead bounds as survival effects.
- Do not equate observed seedling appearance with seed output, compatible mating, microsite suitability, later recruitment, or population-growth lambda.
- Report every alternate denominator and the missing-data extreme scenarios together, including null outcomes.
