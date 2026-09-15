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

## Figure 3 — Independent Chaco programme shows concordant decline

**Purpose:** show what the fifth cluster adds biologically rather than statistically.

For each of the three source-explicit four-site ML020 species, plot the Hedges-g fragmentation effect on pollen-tube interaction support (`I`) against the effect on fruit set (`F`). Add the `F = I` line.

Canonical points:

- *Atamisquea emarginata*: I `-0.71280256`, F `-1.00477681`;
- *Cercidium australe*: I `-0.63733120`, F `-1.13852812`;
- *Prosopis nigra*: I `-0.48057139`, F `-1.13549676`.

All points are in the lower-left deterioration quadrant. Species-specific covariance-aware I–F contrasts are non-significant and the programme Bonferroni gate is `p_ML020=1.0`. Thus fragmentation affects both layers but does not produce detectable state separation in this programme.

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

## Supplementary Table S3 — All 17 primary marginal effects

**Purpose:** expose every admitted marginal Hedges-g effect, including the influential extreme standardized ML001 effects, without treating the 17 rows as independent meta-analytic replicates.

For every admitted effect report the cluster/subsystem, biological layer, endpoint, source-defined fragmentation contrast, independent unit, independent group sizes, Hedges g, sampling variance, standard error and marginal 95% confidence interval. The table is regenerated and checked directly against the canonical effect CSVs. Marginal confidence intervals describe individual standardized fragmentation effects; they are not substitutes for the covariance-aware within-cluster layer-separation tests.

## Supplementary Figure S1 — Forest display of all 17 primary marginal effects

**Purpose:** make the complete effect geometry visually inspectable while preventing the extreme ML001 standardized magnitudes from collapsing the display of all other systems.

ML001 *Serapias lingua* uses an explicitly labelled separate horizontal Hedges-g scale. ML002, ML003, ML014 and ML020 share a second scale. Both panels show zero-reference lines, point estimates and marginal 95% confidence intervals. The dual scale is declared in the figure itself and caption; it is a display choice only and does not alter any effect or statistical test.

## Generation contract

`scripts/build_journal_of_ecology_figures.py` is the deterministic source for Figures 1–3 and Table 1. It reads the canonical registry/effect files plus `scripts/synthesize_state_separation.py`, and must fail if the five-cluster result or ML020 values drift from the canonical synthesis.

`scripts/check_primary_effect_supplement.py` independently reconstructs Supplementary Table S3 from the source effect CSVs and checks all 17 effects, variances, independent-unit counts, standard errors and 95% confidence intervals. `scripts/build_primary_effect_forest.py` then builds Supplementary Figure S1 only from the checked S3 table.