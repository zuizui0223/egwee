# Arnica 2020 — frozen maternal HL versus reproductive function pilot result
## Outcome opened only after protocol commit d5eb3b49ef5fb4ca58c9cafd90499681944b3a68

**Scientific status:** one observational plant translocation programme; **NOT** an estimate of causal genetic rescue, not a claim of interaction-dependent pollination function, not a cross-species meta-analysis, not natural validation of any EGC/EGWE coefficient. The source authors previously evaluated genetic monitoring and maternal/site fitness; this is a transparent source-backed standardized re-estimation, not an independent discovery.

## Source, protocol and reproducibility

- Original: Van Rossum F, Hardy OJ, Le Pajolec S, Raspé O (2020), *Molecular Ecology*, DOI [10.1111/mec.15550](https://doi.org/10.1111/mec.15550).
- Published source: [Zenodo 10.5281/zenodo.3881439](https://doi.org/10.5281/zenodo.3881439), `VanRossumetal_Arnica_fitness.xlsx`, SHA256 `052fef893ed6bb3dd00fec4882c77b6f4f48ed85767fa2643a4809505d4e8e62`.
- Pre-outcome locked analysis plan: `research/rescue_coupling/ARNICA_HL_SEED_PILOT_FROZEN_20261115.md`, commit `d5eb3b49ef5fb4ca58c9cafd90499681944b3a68`.
- Source-exact software: `research/rescue_coupling/analyse_arnica_maternal_HL_seed.py`.
- First result-producing GitHub Actions [run 43696889675](https://github.com/zuizui0223/egwee/actions/runs/43696889675), metadata artifact [14154737988](https://github.com/zuizui0223/egwee/actions/runs/43696889675/artifacts/14154737988). Raw XLSX is not redistributed; only derived summaries are exported.
- Analytic unit: **maternal plant**, unique `(Site,source,Code)`; independent programme denominator = **one**. Six source-site strata with at least five mothers each.

## Result from predeclared estimands

| Prespecified outcome | Original maternal N | Eligible N | Missing maternal HL | Missing outcome | Pooled within-site/source centered-rank r | Two-sided stratified permutation p (10,000, seed=20261115) |
|---|---:|---:|---:|---:|---:|---:|
| **Primary viable seed set** | 145 | **135** | 10 | 0 | **−0.0185128592** | **0.8341165883** |
| Secondary seed germination | 145 | **132** | 10 | 3 | **−0.1087567384** | **0.2395760424** |

- **Primary** within-stratum Ns = `17,22,21,26,22,27`; each stratum's unpooled Spearman r, in blinded alphabetical stratum order: `+0.1441,−0.2084,+0.3654,−0.0987,−0.0743,−0.0261`. The pooled statistic ranks HL and seed outcome separately within strata, subtracts stratum means and correlates concatenated centered ranks. It is not identical to a marginal Spearman across all 135 plants.
- **Leave-one-site-source-stratum-out primary** r ranges **−0.07193 to +0.01454**, with direction sometimes reversing. This does not justify a stable negative association, even within this programme.
- Source format/uniqueness checks passed: 145 original maternal rows, no incomplete maternal identifiers, no duplicated complete maternal composite keys, exact source digest.

## Ecology and conservation interpretation

The measured **neutral-marker-derived maternal homozygosity alone** did not discriminate viable-seed output in this conditioned pilot. This is compatible with multiple causes (strong environment or site/source effects, diverse genetic architectures, maternal effects, pollination process differences, and rank-noise); the analysis cannot identify which.

**Do not infer** that increased heterozygosity is useless, that genetic rescue failed, that realized pollen transfer is intact, that individual genetic load was measured, or that conservation translocation is ineffective. The source programme deliberately mixed seed provenances and managed the habitats; it did not randomize maternal HL as an isolated treatment.

The secondary germination association is likewise unresolved. Site-source strata and maternal genealogies could be correlated; the permutation test assumes exchangeability of maternal observations *within* strata after conditioning and is not a landscape-cluster causal test. Three translocation sites are insufficient for broad population-level causal generalization.

## Programme-level decision

1. Retain this as **a single exploratory quantitative evidence row** in the genetic-state × reproductive-phenotype stream, with `effect_metric=pooled_within_stratum_rank_r` and an explicit 135-mother/6-stratum denominator. **Do not** pool it with Clarke's heterozygosity-to-population-size effects or count six strata as six studies.
2. Newly recovered [original genotype source Zenodo 10.5281/zenodo.3881466](https://doi.org/10.5281/zenodo.3881466) has **1,189** genotype records across multiple generations, of which **250** carry the original `juvenile` label. Direct genotype-to-F0 maternal seed string join failed. **Cohort-restricted F1 analysis, not the earlier all-generation comparison, is authoritative:** among **250 juvenile genotype records** and **250 juvenile fitness records**, only **50** individual-name strings match; **0** of those 50 share an identical site-code string. The matched site-code pairs split into two anonymous groups (**47 and 3**), without a one-to-one source-site codebook. The earlier unstratified all-generation tally of **250/250** apparent literal matches was *not* a valid same-cohort molecular–fitness join and must not be used for a G–W association. All raw cross-file correspondence remains at **SOURCE_ID_CROSSWALK_STOP**. The F0 maternal-HL pilot uses the HL value already stored beside its seed outcome, not a guessed direct genotype-file match.
3. Expand the **independent** gene-flow/mating-function source universe, prioritizing matched maternal genotyping and pollination/seed set, and compare stage-specific HL associations only if estimands and covariances are harmonized prospectively.
