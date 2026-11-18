# CFTQ0001 / Sevenello 2026 direct I-F recovery contract — 2026-09-25

## Status

Programme identity: `P2_CF01_SEVENELLO_2026`.

Primary source: Sevenello, Walker & Mayfield (2026), *Landscape Ecology* 41:45,
doi:10.1007/s10980-026-02305-2.

Public data: doi:10.6084/m9.figshare.31072189.

This is a **retrospective external recovery**. The published article and qualitative result
directions were visible before this contract. The public Figshare response cells have not been
opened for the EGWEE calculation: only file metadata, headers, source identifiers, exposures,
treatment labels/counts, and supplementary Table S1 were inspected before freezing this rule.

## Source geometry

The article defines fragmentation through:

- remnant area;
- position within the remnant: **Edge < 50 m from crop edge** versus **Core >= 150 m**;
- adjacent crop type is agricultural context, not a fragmentation component.

Across nine physical reserves, two reserves have independently sampled opposite crop sides, yielding
11 source sampling areas. Supplementary Table S1 lists 21 transects.

The public `landscape_bees.csv` contains 20 transects. The structural audit shows that the missing
bee row is the POGN-only **Maya / Wheat / Core** transect present in Table S1 and in the plant table.
That row is source missingness for I and is never imputed.

## Source-identity normalization

Before joining I and F, normalize public identifiers to supplementary Table S1 without using any
response value.

### WA12427 alias family in landscape_bees.csv

The four source Table-S1 WA12427 transects are encoded with four site labels in the bee CSV:

- WA12427 + Canola + Core -> WA12427 + Canola + Core;
- WA12428 + Canola + Edge -> WA12427 + Canola + Edge;
- WA12429 + Wheat + Core -> WA12427 + Wheat/Pasture + Core;
- WA12430 + Wheat + Edge -> WA12427 + Wheat/Pasture + Edge.

### Formatting aliases

- `LathamPrivate` -> `Latham Private`;
- `MayaPrivate` -> `Maya Private`;
- `XantippeEast` -> `Xantippe East`;
- `XantippeTank` -> `Xantippe Tank`.

### Crop coding

The source explicitly treats grass-dominated pasture as analogous to wheat. Public response CSVs
already code that source condition as `Wheat`; Table-S1 `Pasture` is normalized to `Wheat`
for joins.

## Primary fragmentation estimand

Primary direct contrast = **Edge minus Core**.

- Edge is the greater-fragmentation / edge-effect condition.
- Core is the reference condition.
- remnant area is retained as a secondary continuous fragmentation component;
- crop type is retained as context/moderator and cannot replace the primary contrast after values
  are opened.

The primary direct recovery does not select crop, remnant size, or a crop-by-position interaction
from published significance.

## Independent unit

Primary quantitative unit = **transect habitat unit**.

Each source transect has one blue-vane bee sample and one plant-experiment transect context.
Individual plants, quadrats, flowers and seeds are nested below transect and never increase n.

The source site x crop identity is retained as the pairing/blocking provenance for Edge/Core
transects. Marginal EGWEE effects use the canonical direct Hedges-g representation on transect
habitat-unit means.

## Primary species panels

This is **one programme with dependent species panels**, never one programme per species.

Primary panels are fixed to the three species for which the source design gives Edge and Core in
the same site x crop sampling units:

- GORO: 6 Edge/Core site x crop pairs -> 12 transects;
- LARO: 8 pairs -> 16 transects;
- POAR: 6 pairs -> 12 transects.

POGN is **sensitivity only** because the source explicitly states that Edge and Core were not always
in the same remnants. Its plant table has 12 transects and the common I-F public-data frame has 11
after the Maya/Wheat/Core bee-row absence.

No species is promoted/demoted after seeing effect direction.

## Locked I endpoint

Primary I = `all_bees` from `landscape_bees.csv`.

This is the source's combined native-bee plus honeybee abundance per transect and is the broad bee
abundance response used in the primary landscape-context model.

Do not replace it with:

- native bees only;
- honeybees only;
- bee richness/diversity;
- another pollinator guild;

because one gives a clearer fragmentation effect.

## Locked F endpoint

Primary F for each species = **mean total viable seeds per plant under natural open pollination**.

Mechanically:

1. use `landscape_seeds.csv`;
2. retain `treat == OP` only;
3. within each species x normalized site x crop x transect, average `total_seeds` across OP plants;
4. do not divide by flower number for the primary F endpoint.

This matches the source's primary total seed-production-per-plant response. Pollen limitation,
open-supplemented treatments, bagged treatments, seeds-per-flower and local-floral predictors are
not substituted into primary F.

## Marginal direct effects

For each primary species panel separately:

1. join the transect-level I value to the species-specific transect-level F value using normalized
   site + crop + transect;
2. require the exact structural panel count frozen above;
3. calculate canonical EGWEE Hedges g for **Edge - Core** for I;
4. calculate the same Edge - Core Hedges g for F;
5. use the canonical LS variance
   `1/n_edge + 1/n_core + g^2/[2(n_edge+n_core)]`;
6. orient negative g as lower biological support/function at the edge.

Do not pool plant-level seed counts directly into Hedges g.

## Within-panel I-F dependence

For each primary species panel:

1. retain the same transect rows used by both I and F;
2. group-center I and F within Edge and Core;
3. calculate Pearson `rho_IF` across those paired transect habitat units;
4. set `Cov(g_I,g_F) = rho_IF * sqrt(V_I * V_F)`;
5. require a positive-definite 2x2 working covariance block;
6. require `Var(g_I-g_F) > 0`.

The covariance is a reconstructed working proxy, not exact analytic sampling covariance.

## Programme-level dependence and count

GORO, LARO and POAR share landscape transects and the same bee table. They are dependent panels
inside **one programme**.

If all three primary panels are admissible:

- direct I-F programme increment = **1**;
- primary direct I-F coverage changes from 1/5 to 2/5;
- within-programme species-specific I-F p-values may be summarized with the same internal
  Bonferroni rule used for other dependent multi-panel programmes:
  `p_programme = min(1, 3 * min(p_GORO, p_LARO, p_POAR))`.

Programme admission is based on effect-unit validity, not that p-value.

The programme does **not** enter or modify the frozen Phase-1 five-cluster Fisher synthesis.

## POGN sensitivity

POGN may be reconstructed only after the three primary panels are complete.

- use the 11 common transects with both public I and F;
- retain the source's unmatched Edge/Core remnant structure;
- report its marginal I/F effects and dependence as sensitivity;
- never count it as another programme or use it to rescue primary-panel admission.

## Remnant-size sensitivity

A remnant-area Fisher-z analysis may be added later under a separately written rule. It is not
allowed to replace the Edge/Core primary contrast because its result is stronger.

## Admission gate

Admit `P2_CF01_SEVENELLO_2026` to the direct I-F pair-specific family only if:

1. the WA12427 alias normalization reproduces supplementary Table S1;
2. GORO, LARO and POAR reproduce exactly 12, 16 and 12 common transect rows;
3. I is one `all_bees` value per transect;
4. F is one OP mean-total-seeds value per species x transect;
5. all six primary marginal Hedges-g effects are finite with positive variance;
6. all three I/F covariance blocks are positive definite;
7. no plant/quadrat/flower/seed count is used as fragmentation n.

## No-rescue rules

Do not:

- use the missing Maya/Wheat/Core bee value by imputation;
- treat WA12427-30 as four independent reserves;
- use 2080 plants, 520 quadrats or seed counts as fragmentation n;
- choose native bees rather than all bees because the edge effect is larger;
- choose pollen limitation or seeds per flower rather than total OP seed production because the
  I-F separation is clearer;
- select only one crop type;
- switch from Edge/Core to remnant area after seeing results;
- count GORO/LARO/POAR as three independent programmes;
- promote POGN to primary after seeing its result;
- modify the frozen Phase-1 Fisher synthesis;
- interpret the natural-data result as validation of an EGWE/NEE finite operator.

## Terminal outcomes

- `sevenello_direct_IF_three_panel_covariance_aware`;
- `sevenello_alias_or_structural_frame_mismatch`;
- `sevenello_primary_species_common_frame_mismatch`;
- `sevenello_marginal_effect_not_reconstructable`;
- `sevenello_IF_covariance_not_positive_definite`.

All outcomes are retained.
