# Journal of Ecology figure/table package

## Principle

The figures should visualize the **claim**, not reward the most extreme standardized effect. In particular, ML001 *Serapias* has very large Hedges-g magnitudes because between-population SD within its source-defined groups is small. Putting all 17 marginal effects on one ordinary linear forest axis would compress the remaining systems and make the paper look like a study of one extreme dataset. The main figures therefore emphasize evidence geometry, cluster influence and the independent ML020 negative robustness result.

## Figure 1 — Primary evidence geometry

**Purpose:** show what each independent direct cluster contributes to the multilayer test.

Rows are the five independent programme/study clusters. Columns are biological layers (`I`, `C`, `F`, `G_adult`, `G_mating`, `G_offspring`). Filled cells indicate admitted primary layers. Cell labels identify the number/type of marginal effects where needed (for example ML003 has adult plus two offspring cohorts; ML020 has three dependent species sharing one programme).

The figure must make two design facts visually explicit:

1. the denominator is five independent programme/study clusters, not 17 independent effects;
2. the layer coverage is incomplete and heterogeneous, so the paper tests within-system non-exchangeability rather than a fully crossed universal layer ordering.

## Figure 2 — Cross-cluster influence determines the claim ceiling

**Purpose:** put the decisive robustness result in the centre of the paper.

Plot the full five-cluster Fisher p-value and each leave-one-primary-cluster-out p-value on a log-scaled p axis, with a reference at 0.05.

Canonical values:

- full: `0.01212432`;
- omit ML001 *Serapias*: `0.18194353`;
- omit ML002 *Brosimum*: `0.01276794`;
- omit ML003 *Spondias*: `0.01407214`;
- omit ML014 *Eucalyptus socialis*: `0.02116199`;
- omit ML020 Chaco programme: `0.00384724`.

The caption states that only omission of ML001 removes rejection. This is the graphical reason the manuscript concludes **conditional state separation** rather than a universal syndrome.

## Figure 3 — Coupled decline versus quantity–function decoupling

**Purpose:** make the paper's ecological result visible without merging incompatible effect families.

Use four panels, each preserving its registered effect scale:

- **A. Chaco / ML020, Hedges g:** three dependent species with both pollen-tube support and fruit set lower in small fragments; programme Bonferroni `p=1.0`.
- **B. *Eucalyptus wandoo*, Fisher z:** pollen tubes `+0.69029123`, seed production `-0.87593080`; I–F `p=0.0008565`.
- **C. *Cardiopetalum calophyllum*, Fisher z:** pollinator abundance `-0.24516531`, fruit set `-1.68379787`; I–F `p=0.00316`.
- **D. Kakamega *Acanthopale pubescens*, Hedges g:** pollinator occurrence `+0.34890186`, fruit set `-2.84788614`; I–F `p=0.00163`.

Use an open circle for interaction/pollen quantity and a filled square for reproductive function. Each panel has its own x-axis and clearly states Hedges g or Fisher z. **Never place Hedges-g and Fisher-z values on one common numerical axis.** The intended comparison is response geometry: coupled deterioration versus quantity–function decoupling.

The figure must retain Chaco as the counterexample so the manuscript does not visually select only decoupling systems.


## Table 1 — Admitted primary clusters

One row per independent primary programme/study cluster. Columns:

- cluster ID;
- system/programme;
- independent fragmentation unit;
- direct contrast;
- admitted primary layers;
- marginal effect count;
- covariance/dependence treatment;
- cluster p-value;
- interpretation.

ML020 appears once, with its three species described as dependent subsystems. ML015 is excluded from Table 1 and described separately as gradient generalisation evidence.

## Table 2 — Complete registered I–F programme census

**Purpose:** expose the full denominator behind the ecological direction claim rather than showing only the three resolved examples.

One row per independent registered programme with eligible I and F information. Required columns:

- programme/system;
- source identifier (DOI / thesis ID);
- effect family;
- number of dependent I–F panels;
- whether a registered within-programme I–F comparison is possible;
- programme-adjusted p-value where applicable;
- census result: resolved mismatch / unresolved mismatch / not testable;
- direction when resolved;
- ecological interpretation.

The table must contain exactly **8 programmes**: 7 pair-testable, 3 resolved, 4 unresolved and 1 not testable. All 3 resolved rows must read **F more negative than I**; no row may be assigned the opposite resolved direction.

Do not pool Hedges-g and Fisher-z values in Table 2. The table is a direction/status census, not a common-effect meta-analysis.

## Supplementary Table S3 — All 17 primary marginal effects

**Purpose:** expose every admitted marginal Hedges-g effect, including the influential extreme standardized ML001 effects, without treating the 17 rows as independent meta-analytic replicates.

For every admitted effect report the cluster/subsystem, biological layer, endpoint, source-defined fragmentation contrast, independent unit, independent group sizes, Hedges g, sampling variance, standard error and marginal 95% confidence interval. The table is regenerated and checked directly against the canonical effect CSVs. Marginal confidence intervals describe individual standardized fragmentation effects; they are not substitutes for the covariance-aware within-cluster layer-separation tests.

## Supplementary Figure S1 — Forest display of all 17 primary marginal effects

**Purpose:** make the complete effect geometry visually inspectable while preventing the extreme ML001 standardized magnitudes from collapsing the display of all other systems.

ML001 *Serapias lingua* uses an explicitly labelled separate horizontal Hedges-g scale. ML002, ML003, ML014 and ML020 share a second scale. Both panels show zero-reference lines, point estimates and marginal 95% confidence intervals. The dual scale is declared in the figure itself and caption; it is a display choice only and does not alter any effect or statistical test.

## Generation contract

`scripts/build_journal_of_ecology_figures.py` is the deterministic source for Figures 1–3 and Table 1. It reads the canonical registry/effect files plus `scripts/synthesize_state_separation.py`, and must fail if the five-cluster result or ML020 values drift from the canonical synthesis.

`scripts/check_primary_effect_supplement.py` independently reconstructs Supplementary Table S3 from the source effect CSVs and checks all 17 effects, variances, independent-unit counts, standard errors and 95% confidence intervals. `scripts/build_primary_effect_forest.py` then builds Supplementary Figure S1 only from the checked S3 table.