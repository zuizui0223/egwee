# Protocol — multilayer meta-analysis of plant fragmentation responses

**Frozen development date:** 2026-09-11

This protocol replaces the four-gate methodological paper as the active EGWEE publication direction. The previous four-gate analyses remain archived quality-control evidence and may inform admissibility decisions, but they are not the paper's headline result.

## 1. Target population

Empirical studies of flowering plants exposed to habitat fragmentation, habitat isolation, reduced habitat area, or a closely matched landscape-fragmentation contrast, with at least one biological response in the focal layers below.

The primary meta-analysis requires a direct fragmented-versus-reference comparison. Continuous-only fragmentation gradients are retained for a separate correlation-effect stream.

## 2. Response layers

Each extracted endpoint is assigned before effect-size calculation to one layer:

- `D_resource_demography`: plant density, population size, flowering density/resource support, recruitment support;
- `I_interaction`: pollinator visitation, pollen receipt/deposition, interaction strength/effectiveness;
- `C_movement_connectivity`: direct pollen flow, donor movement, mating connectivity, pollinator movement, seed/propagule movement;
- `F_reproductive_function`: fruit set, seed set, seed production, siring success or other realised reproductive function;
- `G_adult`: adult standing genetic diversity/inbreeding/structure;
- `G_offspring`: seed, progeny or juvenile genetic diversity/inbreeding/mating state;
- `T_partner_trait`: functional partner composition or explicit trait matching, retained as a secondary layer unless sample size supports a primary estimate.

An endpoint cannot be moved between layers after seeing its effect size.

## 3. Study eligibility

A study enters the primary Hedges-g stream only if all of the following hold:

1. the fragmentation exposure is defined independently of the biological outcome;
2. fragmented and reference conditions, or an equivalent two-group contrast, are identifiable;
3. an effect size and sampling variance can be calculated or reconstructed without outcome-dependent model selection;
4. the biological endpoint maps unambiguously to a predeclared layer;
5. the experimental/observational unit and sample size are recoverable;
6. duplicate reports of the same biological observations can be linked and not double-counted.

A study does **not** need to measure every layer. However, the primary state-separation claim is estimated from studies with at least two eligible layers under the same study/species fragmentation contrast. Single-layer studies contribute to layer-specific grand means and moderator precision but not to paired within-system contrasts.

## 4. Search and seed corpus

The search starts from prior quantitative syntheses and expands forward/backward:

- Aguilar et al. 2006 — pollination and reproductive susceptibility to fragmentation;
- Aguilar et al. 2008 — plant genetic consequences of fragmentation;
- Aguilar et al. 2019 — progeny genetic/biological quality;
- recent updated land-use meta-analysis of pollination and male/female fitness (Annals of Botany, 2024/2025 volume publication);
- global plant FSGS meta-analysis (AoB PLANTS, 2023);
- global insect-pollinator fragmentation meta-analysis with deposited Dryad data (Journal of Applied Ecology, 2025).

All cited primary studies are deduplicated by DOI/title/species/system. Forward searches extend through 2026-09-11.

Repository-audited systems (*Crepis*, Miyake *Camellia–Zosterops*, *Conospermum*, *Spondias*, Honshu–Izu, Zurich, Chicago *Penstemon*, *Primula*, *Oenothera*, *Eschscholzia*, Mallorca carob, *Campanula americana*) are search seeds rather than automatic inclusions.

## 5. Effect size

### 5.1 Primary two-group stream

Use Hedges' `g` for fragmented minus reference conditions. Raw extraction fields retain means, SD/SE/CI, sample sizes and the original biological direction.

After calculation, orient the effect so:

- `g_oriented < 0` = fragmentation reduces biological support/function;
- `g_oriented > 0` = fragmentation maintains/increases support relative to reference.

For endpoints where an increase represents deterioration (e.g. inbreeding coefficient, genetic differentiation, spatial genetic structure when coded as fragmentation-induced isolation), multiply the standardized effect by `-1` after storing the raw sign and an explicit `orientation_multiplier=-1`.

No sign is changed because an estimate is inconvenient or inconsistent with the hypothesis.

### 5.2 Continuous-gradient stream

For studies reporting only correlations/regression relationships with fragmentation severity, use Fisher's `z(r)` when a correlation can be recovered without strong transformation assumptions. This stream is analysed separately and used as a sensitivity/generalisation analysis.

Do not convert between Hedges' `g` and Fisher `z` merely to enlarge the primary sample unless the conversion rule is preregistered in a later protocol amendment before outcome synthesis.

## 6. Dependence structure

Multiple endpoints, years, populations and layers from one paper are not independent. The extraction table records `study_id`, `species_id`, `system_id`, `contrast_id`, `population_id`, `year`, `layer` and `endpoint_id`.

Primary inference uses a multilevel random-effects meta-regression with study/species clustering. Cluster-robust variance estimation is used when within-study sampling covariance cannot be reconstructed. If shared-control covariance can be calculated, a multivariate sampling-variance matrix is preferred.

The primary denominator is the number of independent study/species fragmentation contrasts, not the raw number of extracted effects.

## 7. Primary tests

### Test 1 — response-layer heterogeneity

Model `g_oriented ~ 0 + layer` with the predeclared random/dependence structure. Test the omnibus null that eligible biological layers have the same underlying fragmentation effect.

Primary contrasts:

- `I - F`;
- `C - F`;
- `G_adult - G_offspring`;
- `G_adult - mean(I,F)` where jointly estimable.

The NEE Q1 empirical prediction is supported only if layer/paired contrasts show systematic divergence, not merely because total heterogeneity `I²` is high.

### Test 2 — cohort/history lag

Among studies with genetic data, compare adult standing genetic effects against progeny/juvenile effects, with time since fragmentation and life form as moderators where available.

### Test 3 — process–function coupling

Among study/species contrasts measuring both `C` and `F`, test whether the true movement/connectivity effect covaries with the reproductive-function effect. Repeat for `I` and `F`.

Because both axes are estimated with error, use a multivariate/measurement-error model where feasible; otherwise report cluster-robust meta-regression plus a sensitivity analysis restricted to high-precision pairs.

## 8. Moderators

Predeclared moderators:

- self-incompatible / self-compatible / mixed or unknown;
- autonomous reproductive assurance where explicitly measured;
- pollination vector: invertebrate / vertebrate / abiotic / mixed;
- life form and longevity;
- adult vs progeny/juvenile cohort;
- time since fragmentation;
- fragmentation component: area, isolation/connectivity, composite;
- direct process measurement vs proxy;
- biome/region only as secondary moderators after adequate cell counts.

Do not define a `compensated` category using the observed reproductive outcome and then use that same category to explain reproduction. Compensation is tested through independently extracted process effects/moderators.

## 9. Missingness and publication bias

Missing biological layers are not coded as zero effects. The pattern of layer availability is reported explicitly by study and tested descriptively for taxonomic/design bias.

Publication-bias diagnostics are conducted within response layer where sample size permits, not on a mixture of biologically different outcomes. Funnel asymmetry, small-study effects and leave-one-study-out influence are secondary diagnostics rather than automatic correction rules.

## 10. Phylogeny

If species coverage becomes sufficiently large, add a phylogenetic random effect using a reproducible plant phylogeny. The non-phylogenetic multilevel model remains the primary computational baseline; phylogenetic analysis is a sensitivity/extension unless species coverage and matching are adequate before model fitting.

## 11. Pre-specified mechanistic anchors

The following systems are retained for interpretation, not weighted as special observations:

- *Crepis sancta* — interaction limitation;
- Miyake *Camellia japonica–Zosterops japonicus* — movement compensation;
- *Conospermum undulatum* — adult-genetic history lag;
- *Spondias purpurea* — joint interaction/movement/function/offspring-genetic deterioration.

They may appear in an illustrative panel only if their extracted effects pass the same eligibility rules as all other studies.

## 12. Decision boundaries

The meta-analysis may support:

- a global average effect of fragmentation within each response layer;
- systematic cross-layer divergence;
- cohort lag;
- associations between process effects/moderators and function effects.

It may not claim:

- that one finite NEE operator has been directly validated in nature;
- causal mediation from observational cross-study covariance;
- universal equality or ordering of all layers;
- that a missing layer equals biological absence;
- that islandness or urbanisation is itself a mechanistic state.

## 13. Current execution state

Protocol and data schema are fixed before quantitative synthesis. Existing four-gate results remain provenance/QC material. No numerical meta-analytic conclusion should be written into the manuscript until study deduplication, eligibility, effect-size extraction and dependence checks are complete.
