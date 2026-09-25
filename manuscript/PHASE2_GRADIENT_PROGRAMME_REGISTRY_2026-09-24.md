# Phase-2 gradient programme registry — 2026-09-24

## Purpose

Continuous fragmentation / landscape-alteration gradients remain separate from the primary fragmented-versus-reference Hedges-g family.

The registry now contains **6 gradient/generalisation programmes**:

1. **ML015 — Eucalyptus wandoo**: I/F/G_adult on the response-free fragmentation PC.
2. **P2_CF01_ZURICH_2026 — Zurich BetterBlooms**: four dependent phytometer I/F panels against the source-defined Urban_500 impervious-surface gradient.
3. **P2_CF01_MILKWEED_URBAN_2023 — common milkweed**: population-level I/F responses along the Greater Toronto urbanization gradient.
4. **P2_CF01_ACER_MIYABEI_2014 — Acer miyabei**: retrospective forest-level C/F responses along the source Table-1 isolation gradient.
5. **P2_CF01_CARDIOPETALUM_2012 — Cardiopetalum calophyllum**: retrospective fragment-level I/F responses along the fragment-area gradient.

Across the registry there are **19 primary Fisher-z admissible marginal effects**: 3 from ML015, 8 from Zurich, 2 from common milkweed, 2 from Acer miyabei, and 2 from Cardiopetalum. Sensitivity analyses are not counted as additional marginal effects or programmes.

## Zurich admission

Zurich contributes **8 Fisher-z admissible marginal effects** inside one programme:

- 4 interaction/visitation effects;
- 4 reproductive-function effects;
- 4 positive-definite within-phytometer I/F covariance blocks.

The four phytometer species are repeated outcomes from one 24-garden experiment and cannot be counted as four independent programmes.

## Common milkweed admission

Common milkweed contributes **2 primary Fisher-z marginal effects** inside one natural observational programme:

- I: population-level pollinator abundance per surveyed plant;
- F: mean follicles per inflorescence;
- primary source-code-faithful common frame: **31 populations** in 2019;
- prespecified zero-pollinator-retaining sensitivity: **38 populations**.

On the primary urbanization exposure (greater urbanization = negative distance to Toronto center), I declines while F changes weakly in the opposite direction. The covariance-aware I-F interval crosses zero. Retaining zero-pollinator surveyed populations strengthens the negative I-F contrast slightly but does not reverse the qualitative geometry and still crosses zero.

The sensitivity is an alternate analysis of the same programme, not a fourth programme.

## Acer miyabei admission

Acer miyabei contributes **2 primary Fisher-z marginal effects** inside one retrospective natural programme:

- C: negative mean seed kinship, so higher values mean greater gene-flow support;
- F: viable seed density, derived deterministically as source seed density × viable-seed proportion;
- primary exposure: log distance to nearest forest;
- common source-table frame: **9 forest fragments** with non-missing kinship and reproductive components.

The covariance-aware C-F contrast is `+0.181` with 95% CI `[-0.543, +0.906]` and `p=0.624`, so this programme does not resolve a precise C-F separation. Source seed density and viable proportion show opposite endpoint-definition sensitivities and are retained without allowing either to replace the primary derived F post hoc.

This is explicitly **retrospective generalisation evidence** because Table 1 values were visible before the deterministic recovery rule was written.

## Cardiopetalum admission

Cardiopetalum contributes **2 primary Fisher-z marginal effects** inside one retrospective natural programme:

- I: fragment-level beetle-pollinator abundance per flower;
- F: fragment-level fruit set per flower;
- primary exposure: negative log fragment area, so higher values mean smaller fragments;
- source-table frame: **10 forest fragments**.

The covariance-aware I-F contrast is **+1.439** with 95% CI **[+0.483, +2.394]** and **p=0.00316**. The interaction layer changes only weakly with fragment area (I z = -0.245), whereas reproductive function declines sharply toward smaller fragments (F z = -1.684).

Follicle set, seed set and nearest-fragment isolation retain the same qualitative geometry and remain sensitivities rather than replacements for the frozen primary endpoints.

This is explicitly **retrospective generalisation evidence** because the Table 1 values were visible before the deterministic recovery rule was written.

6. **P2_CF01_PRITCHARD_2005 — custard apple**: retrospective nested-frame I/F responses along orchard distance from rainforest, retained with cluster-robust dependence fallback.

## Pritchard admission

Pritchard contributes **2 primary Fisher-z marginal effects** inside one retrospective observational programme:

- I: total floral visitor abundance from the source nine-orchard log-abundance versus log-distance regression; Fisher z = **−0.989**, n=9;
- F: open-pollinated fruit initiation from the five source-explicit orchard means; Fisher z = **−1.490**, n=5;
- the five F orchards are an explicit subset of the nine I orchards;
- paired covariance is not reconstructable because the numeric nine-orchard I vector is not public.

The two effects remain in one cluster with the frozen **cluster-robust fallback**. No within-programme I−F p-value is calculated, covariance is not set to zero, and Figure 3.2 is not digitized.

The source explicitly cautions that distance to rainforest is observational and can covary with rainfall and broad geographic position. EGWEE therefore treats this as landscape-position generalisation evidence, not causal proof of a rainforest-distance mechanism.

## Family boundary

Current primary direct I-F coverage remains **1/5** (ML020 only).

Zurich, common milkweed, Acer miyabei, Cardiopetalum and Pritchard increase the explicitly recoverable gradient/generalisation multilayer programme set from **1 to 6 programmes** (ML015 + Zurich + milkweed + Acer miyabei + Cardiopetalum). They contribute **0** to the primary Hedges-g programme denominator and do not alter the frozen Phase-1 state-separation synthesis.
