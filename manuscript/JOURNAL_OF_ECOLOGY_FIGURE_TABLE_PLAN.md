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


## Figure 4 — Estimand-scale sensitivity

**Purpose:** show why the former separation/bottleneck headline is no longer scale-robust.

Required panels:

- **A. Serapias ordering:** Hedges-g absolute order G > C > F versus lnRR absolute order C > F > G; report C–F lnRR p≈0.605.
- **B. Omit-ML001 Fisher sensitivity:** g primary, lnRR + rho proxy, lnRR + zero covariance, lnRR + Cauchy maximum-variance boundary, with the 0.05 threshold visible.
- **C. Directional consistency:** 17/17 negative effects on both oriented g and oriented lnRR.
- **D. Exploratory ecology:** Brosimum and Eucalyptus socialis attenuation examples plus Spondias adult/offspring contrast, with Chaco explicitly identified as a counterexample to universal attenuation.

Do not place g and lnRR magnitudes on a common numerical axis. The figure compares inferential geometry and qualitative direction, not raw effect-size values across estimands.


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

## Table 2 — Estimand-scale sensitivity summary

One row per primary direct cluster plus FULL and OMIT_ML001 cross-cluster rows. Required columns:

- historical Hedges-g p-value;
- lnRR p under carried rho proxy;
- lnRR p under zero covariance;
- lnRR p under Cauchy maximum-variance boundary;
- interpretation.

The table must show that the omit-ML001 classification crosses the 0.05 threshold across estimand/dependence treatments. It must not imply that lnRR is the uniquely correct scale.

## Supplementary Table S4 — Registered-scale process–function census

Retain the 12-programme process–function catalogue for transparency and hypothesis generation. Explicitly mark it as heterogeneous-scale and non-confirmatory after the estimand audit.


## Supplementary Table S3 — All 17 primary marginal effects

**Purpose:** expose every admitted marginal Hedges-g effect, including the influential extreme standardized ML001 effects, without treating the 17 rows as independent meta-analytic replicates.

For every admitted effect report the cluster/subsystem, biological layer, endpoint, source-defined fragmentation contrast, independent unit, independent group sizes, Hedges g, sampling variance, standard error and marginal 95% confidence interval. The table is regenerated and checked directly against the canonical effect CSVs. Marginal confidence intervals describe individual standardized fragmentation effects; they are not substitutes for the covariance-aware within-cluster layer-separation tests.

## Supplementary Figure S1 — Forest display of all 17 primary marginal effects

**Purpose:** make the complete effect geometry visually inspectable while preventing the extreme ML001 standardized magnitudes from collapsing the display of all other systems.

ML001 *Serapias lingua* uses an explicitly labelled separate horizontal Hedges-g scale. ML002, ML003, ML014 and ML020 share a second scale. Both panels show zero-reference lines, point estimates and marginal 95% confidence intervals. The dual scale is declared in the figure itself and caption; it is a display choice only and does not alter any effect or statistical test.

## Generation contract

`scripts/build_journal_of_ecology_figures.py` is the deterministic source for Figures 1–4 and Tables 1–2. It reads the canonical registry/effect files, the complete process–function census, and `scripts/synthesize_state_separation.py`; it must fail if the five-cluster result, programme censuses or registered response geometry drift from their canonical sources.

`scripts/check_primary_effect_supplement.py` independently reconstructs Supplementary Table S3 from the source effect CSVs and checks all 17 effects, variances, independent-unit counts, standard errors and 95% confidence intervals. `scripts/build_primary_effect_forest.py` then builds Supplementary Figure S1 only from the checked S3 table.