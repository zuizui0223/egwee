# CFTQ0103 / southern-Thailand orchard I-F recovery contract — 2026-09-24

## Programme

Programme identity: `P2_CF01_THAI_ORCHARD_FOREST_PROXIMITY_2016`.

Primary source: Sritongchuay, Kremen & Bumrungsri (2016), *Journal of Tropical Ecology* 32:269–279,
doi:10.1017/S0266467416000353.

The source studied **10 matched pairs of mixed-fruit orchards**. Each pair contained one orchard
near tropical forest (<1 km from the forest edge) and one orchard far from forest (>7 km). Flower
visitor diversity, visitation frequency and fruit set were measured for rambutan, durian and mango.

This is a **retrospective external recovery**. The published abstract already exposes species-level
qualitative results. Therefore no species, endpoint or exposure may be selected because it gives a
stronger result. The rules below are fixed before any orchard-level numerical response values are
opened for EGWEE.

## Independent unit and blocking

Primary independent unit = **orchard**.

The source matching is retained as 10 orchard-pair blocks:

- reference condition = near-forest orchard (<1 km);
- fragmented/isolated condition = far-from-forest orchard (>7 km);
- expected maximum frame = 10 near + 10 far orchards.

Flowers, flower visits, visitor individuals, observation periods, trees, inflorescences, fruits and
seeds are nested below orchard and never increase fragmentation n.

Pair identity is retained for matching diagnostics and dependence reconstruction, but a pair is not
counted as two independent programmes. The complete source study contributes at most **one** EGWEE
programme.

## Locked primary exposure

Primary direct fragmentation contrast = **far from forest versus near forest**.

This is frozen for all three crop species. Distance to the nearest cave is not substituted as the
primary fragmentation exposure for durian, even though caves are biologically important for bat
pollination. Cave proximity remains source context / secondary mechanistic evidence only.

No continuous forest-distance model, alternative distance threshold, forest-patch-size contrast or
landscape-composition variable is substituted after seeing response values.

## Mandatory species rule

Retain the complete source-defined crop set:

1. rambutan;
2. durian;
3. mango.

The programme is not allowed to select only the crop with the strongest forest-proximity response.
Quantitative admission requires the source-reported orchard-level I and F endpoints to be
reconstructable for **all three crop panels** on their valid source frames.

If one crop is structurally absent from an orchard because it was not present or sampled, preserve
that source missingness. Do not impute it and do not replace the crop with another species. If the
available public source cannot reconstruct the complete declared crop set, the programme remains
quantitatively blocked rather than being reduced post hoc to the apparently strongest crop.

The three crops are dependent outcome panels within one programme and never count as three
independent I-F programmes.

## Locked I endpoint

For each crop, primary I = **flower visitation frequency** using the broadest source-defined visitor
set for that crop.

Visitor diversity/richness is secondary. Crop-specific dominant pollinator taxa may be described
biologically, but taxon-specific visitation is not substituted for the broad visitation-frequency
endpoint because it gives a larger forest-proximity contrast.

Use one orchard-level visitation value per crop per orchard after reproducing the source aggregation.

## Locked F endpoint

For each crop, primary F = **fruit set** on the same orchard and forest-proximity frame used for I.

Use the source's direct fruit-set quantity and its source aggregation. Do not substitute fruit
number, yield, seed set, commercial quality or another reproductive endpoint after effect
calculation.

## Effect-size representation

This programme belongs to the primary direct fragmented-versus-reference Hedges-g family.

For each crop and layer:

1. construct orchard-level values separately for the 10 far and 10 near orchards, preserving genuine
   source missingness;
2. calculate the canonical EGWEE Hedges `g` for `far - near`;
3. use orchard as the variance sample unit;
4. orient negative values as lower interaction or reproductive function under greater isolation
   from forest.

The matched-pair structure is retained as a sensitivity/blocking diagnostic; it does not justify
using flowers, trees or observations as additional n.

## Within-crop I-F dependence

For each crop with the full source-defined I/F orchard frame:

1. group-center I and F separately within near and far conditions;
2. calculate their Pearson residual correlation across the paired orchard-level observations;
3. set `Cov(g_I,g_F) = rho_IF * sqrt(V_I * V_F)`;
4. require the 2x2 working covariance block to be positive definite;
5. require `Var(g_I - g_F) > 0`.

This is a reconstructed working sampling covariance, not an exact design-based covariance.

## Programme-level I-F state-separation statistic

If all three crop panels pass the effect-unit gate, compute the covariance-aware I-F contrast for
each crop.

Because the crops occur in the same 20-orchard programme, they are dependent panels rather than
independent Fisher inputs. The programme receives one conservative cluster p-value:

`p_programme = min(1, 3 * min(p_rambutan, p_durian, p_mango))`.

This rule is fixed before orchard-level effect values are opened. It is not used to select a crop.

## Admission gate

Promote `P2_CF01_THAI_ORCHARD_FOREST_PROXIMITY_2016` to the direct I-F family only if:

1. the 10 near/far orchard pairs are identifiable;
2. orchard-level visitation frequency and fruit set are reproducibly recoverable for all three
   source crop panels;
3. orchard is retained as the independent unit;
4. each crop's I/F working covariance block is valid;
5. the common forest-proximity and endpoint rules above are applied without post-result
   substitution.

Admission is based on design and effect-unit validity, not significance.

If admitted, the programme increments direct I-F coverage by **one programme only**.

## No-rescue rules

Do not:

- retain only rambutan because the published abstract reports a forest-proximity fruit-set effect;
- drop durian or mango because their published forest-proximity fruit-set responses are weaker;
- replace forest proximity with cave proximity for durian;
- switch visitation frequency to visitor richness/diversity or a dominant-pollinator-only endpoint;
- use flowers, visits, trees, fruits or seeds as independent orchard replicates;
- treat the three crop species as three independent programmes;
- digitize figures or reverse-engineer published significance tests unless a later prospective
  amendment explicitly authorizes that recovery method before values are extracted;
- add a continuous-gradient analysis to rescue a failed direct contrast.

## Terminal outcomes

- `thai_orchard_direct_IF_covariance_aware`;
- `thai_orchard_public_orchard_values_not_recoverable`;
- `thai_orchard_pair_identity_not_recoverable`;
- `thai_orchard_complete_three_crop_frame_not_recoverable`;
- `thai_orchard_covariance_not_positive_definite`.

All terminal outcomes are retained.
