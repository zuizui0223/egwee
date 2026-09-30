# Journal of Ecology figure/table package

## Principle

The figures should visualize the **scale-aware claim**, not reward the most extreme standardized effect. In particular, ML001 *Serapias* has very large Hedges-g magnitudes because between-population SD within its source-defined groups is small, yet its proportional lnRR ordering differs sharply. The main package therefore separates historical Hedges-g evidence from estimand-scale sensitivity and from qualitative sign geometry. No figure may present g-only magnitude ordering, leave-one-*Serapias* failure, or the registered-scale bottleneck catalogue as a scale-independent ecological result.

## Figure 1 — Primary evidence geometry

**Purpose:** show what each independent direct cluster contributes to the multilayer test.

Rows are the five independent programme/study clusters. Columns are biological layers (`I`, `C`, `F`, `G_adult`, `G_mating`, `G_offspring`). Filled cells indicate admitted primary layers. Cell labels identify the number/type of marginal effects where needed (for example ML003 has adult plus two offspring cohorts; ML020 has three dependent species sharing one programme).

The figure must make two design facts visually explicit:

1. the denominator is five independent programme/study clusters, not 17 independent effects;
2. the layer coverage is incomplete and heterogeneous, so the paper tests within-system non-exchangeability rather than a fully crossed universal layer ordering.

## Figure 2 — Historical Hedges-g leave-one-cluster-out influence

**Purpose:** reproduce the registered primary g-scale influence result without presenting it as scale-invariant.

Plot the full five-cluster Hedges-g Fisher p-value and each leave-one-primary-cluster-out p-value on a log-scaled p axis, with a reference at 0.05.

Canonical historical values:

- full: `0.01212432`;
- omit ML001 *Serapias*: `0.18194353`;
- omit ML002 *Brosimum*: `0.01276794`;
- omit ML003 *Spondias*: `0.01407214`;
- omit ML014 *Eucalyptus socialis*: `0.02116199`;
- omit ML020 Chaco programme: `0.00384724`.

The figure title/subtitle must explicitly say **Hedges g / historical primary estimand** and direct readers to Figure 4 for the lnRR sensitivity. It must not call the g-only leave-one-out result the manuscript's scale-independent claim ceiling.

## Figure 3 — Complete interaction–function sign geometry

**Purpose:** make the main scale-stable ecological result visible across the complete matched I–F denominator rather than through selected examples.

Use one row per primary I–F panel, grouped by programme. Required columns:

- programme;
- focal taxon/panel;
- sign of I;
- sign of F;
- qualitative geometry.

Required denominator and checks:

- exactly **18 primary panels**;
- exactly **8 independent programmes**;
- **6 sign-discordant panels** in **5 programmes**;
- both discordant directions represented: I+/F− and I−/F+;
- exactly **4 multi-panel programmes**, of which **3** contain more than one sign geometry.

Do not report 5/8 or 6/18 as prevalence estimates or run sign/binomial tests. Direct signs are invariant under g→lnRR for the positive-valued endpoints; gradient panels remain on their registered Fisher-z representations.

The previous four-example response-regime display is no longer a main figure. Its individual examples remain traceable in Supplementary Table S5 and source-specific Results text.


## Figure 4 — Estimand-scale sensitivity

**Purpose:** show why relative-amplitude / separation claims require an explicit effect-size scale.

Required panels:

- **A. Serapias ordering:** Hedges-g absolute order G > C > F versus lnRR absolute order C > F > G; report raw-delta C–F lnRR `p=0.6364`.
- **B. Omit-ML001 Fisher sensitivity:** historical g primary; lnRR + raw-unit multivariate delta covariance; lnRR + zero covariance; lnRR + Cauchy maximum-variance boundary, with the 0.05 threshold visible.
- **C. Directional consistency:** 17/17 negative effects on both oriented g and oriented lnRR.
- **D. Exploratory ecology:** Brosimum and Eucalyptus socialis upstream-dominant lnRR examples plus Spondias adult/offspring contrast, with Chaco explicitly identified as a counterexample to universal attenuation.

Do not place g and lnRR magnitudes on a common numerical axis. The figure compares inferential geometry and qualitative direction, not raw effect-size values across estimands. Label the raw-unit lnRR covariance as a delta-method approximation.


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
- lnRR p under raw-unit multivariate delta covariance;
- lnRR p under zero covariance;
- lnRR p under Cauchy maximum-variance boundary;
- interpretation.

The table must show that the omit-ML001 classification crosses the 0.05 threshold across estimand/dependence treatments. It must not imply that lnRR is the uniquely correct scale. The former carried-rho sensitivity is provenance only and is not shown as the authoritative lnRR covariance reconstruction.


## Supplementary Table S5 — Scale-stable I–F sign geometry

**Purpose:** expose the scale-stable qualitative interaction→function result without treating dependent panels as independent studies.

Required content:

- exactly 18 primary I–F panels from 8 independent programmes;
- interaction and F signs on the registered representation;
- one of four descriptive geometries: I−/F−, I+/F+, I+/F−, I−/F+;
- explicit panel/program identifiers so multi-species shared-exposure heterogeneity is auditable.

The table must reproduce:

- 6 sign-discordant panels;
- sign-discordant panels in 5 independent programmes;
- 2 panels with I+,F−;
- 4 panels with I−,F+;
- 4 multi-panel programmes, of which 3 contain more than one sign geometry.

Do not report 5/8 as a prevalence estimate or run a sign/binomial test across dependent panels/programmes.

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