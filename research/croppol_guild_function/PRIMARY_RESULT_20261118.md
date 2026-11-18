# CropPol original field observations: guild composition does not improve held-out crop-yield prediction

**18 November 2026 — empirical EGWEE only.** Registered conditional field-level prediction, then explicitly post-outcome quality and split-stability diagnostics. Not a crop-pollination causal intervention, not an independent pollen-quality study, not wild-plant fragmentation evidence, and not the theoretical EGWE programme.

## Source and pre-outcome sequence

Independent author maintained original database: [ibartomeus/CropPol](https://github.com/ibartomeus/CropPol) at immutable commit `99c69dbab4fa7cbdb630ff3e9bd9989b3de9548b`; field source `Final_Data/CropPol_field_level_data.csv` Git blob SHA-1 `cd19a354741ac40428e6b94aa1ec2ee596ff0547`, full SHA256 `ecfa84d1f6a52f24f13b7096347a59f231e8cc77eef8692b0a0183ceca86f879`; sampling source `Final_Data/CropPol_sampling_data.csv` Git blob SHA-1 `b7ab3fd92da0be5e8ec41b6ada50c2da7d4756c2`, SHA256 `aafba5d3dfbab2c93f3a60e31181d2c5b33535cc2c8f33b85495facb42382f30`. Original files are **not** copied into this EGWEE branch.

Original file retrieval and first-row schema checking ([source workflow 44245540061](https://github.com/zuizui0223/egwee/actions/runs/44245540061)) established exactly **3,448 original field-level rows (68 columns)** and **54,191 original insect sampling rows (12 columns)**. The author version notes describe source version 2.1.0 and explicitly changed `study_id2`, visit/abundance semantics and original yield fields. The original data paper is Allen-Perkins et al., *Ecology*, DOI [10.1002/ecy.3614](https://doi.org/10.1002/ecy.3614).

The source-only scientific plan and original source paths were frozen at `SOURCE_PREOUTCOME_PROTOCOL_20261118.md` before inspecting signed joint yield/visitation effects. Then source-only original labels and missingness were audited in `audit_source_field_grain.py` ([CI 44245863262](https://github.com/zuizui0223/egwee/actions/runs/44245863262)). The **exact** Syrphidae-aware eligibility, two prediction models, fold construction, scoring and pass/fail rule were separately frozen at `GUILD_QF_PREDICTION_FREEZE_20261118.md` (commit `6c457ba4a8e5323f68ca4f624a610ae71af01b9e`), **before accessing paired signed outcome associations**. Original source fields were eligible regardless of their effect direction.

### Source-semantic qualification — not a post-result filter

A recorded Syrphidae zero is usable only when the original `taxa_recorded` states that syrphids were actually surveyed (`all visitors`, `bees and syrphids`, `bees, syrphids and wasps`). Explicitly require `use_visits_or_abundance = use visits`, direct focal observations or transects (no pan-trap abundances), all four main guild visit rates numeric, known primary yield and source units, and bee+Syrphidae subtotal >0.

- **2,020/3,448** field rows have finite, nonnegative total visitation-rate entries, **2,491** have finite, nonnegative primary yield entries, and **1,674** have both (source-only availability).
- Of the complete source-unit candidates, **942 fields** passed the row-level conservative guild/survey meaning checks.
- Prospective minimum per source programme × crop × year × primary-yield unit × visitation unit: >=10 independent field records, >=3 bee-positive and >=3 syrphid-positive fields. Retained **591 field records**, **29 matched panels**, **20 distinct author study programmes** and **11 crop taxa**. Source records use **12 different yield unit labels** and **8 visit unit labels** (never pooled in original numeric units). Panels nested within a study are not independent study replicates.
- Two-stage coverage is reproduced in [CI 44246214681](https://github.com/zuizui0223/egwee/actions/runs/44246214681). Every original `study_id/site_id/sampling_year/crop` field key is unique. Missing unexamined guilds are **not filled with ecological zero**.

## Frozen prediction comparison

Response: `log1p(original primary yield)` from the source, converted to **training-only z scores separately for every fivefold split**. Predictions scored as held-out field mean squared error on each split's training-only scale. Every panel uses its own crop, study, year, yield unit and visitation unit. Source-visitation features are log1p(total visit rate) in M0, with the recorded **Syrphidae / (Syrphidae + Bombus + other wild-bee visit rates)** as one addition in M1. Honeybee visitation remains within original total Q; it is not treated as a wild-bee predictor. One fixed source-hash-based fivefold field assignment per panel, lambda=1 regularized ridge, unpenalized intercept, no panel repair or tuning.

Per programme, average held-out panel errors equally, then average original study programme means equally. Primary decision requires **positive** overall M0−M1 gain, whole-original-programme 2,000-bootstrap CI strictly positive and >=70% programme means positive. No independent validation in entirely held-out study programmes is claimed.

| Frozen primary | Reproduced result |
|---|---:|
| Eligible complete prediction panels/fields/original programmes | **29 / 591 / 20** |
| Baseline M0 (total visits) study-equal CV MSE | **1.67072323** |
| M1 (+ observed bee-versus-syrphid composition) CV MSE | **2.11792886** |
| **M0−M1 study-equal predictive gain** | **−0.44720563** |
| Whole-original-programme 95% bootstrap interval | **[−1.23535022, −0.00723172]** |
| Original study programmes with positive incremental gain | **4/20** |
| Panels with positive incremental gain | **6/29** |
| Leave-one-whole-programme gain range | **[−0.49665, −0.07848]** |

**Frozen decision: `NO_RESOLVED_STUDY_GENERAL_GUILD_COMPOSITION_INCREMENT`.** The richer observational visitor model *underperforms* total visitation alone on these within-programme field holdouts. The scale is a train-standardized log-yield MSE, **not** proportional crop harvest loss or percent yield change. Reproduced directly from immutable author-source bytes by [Actions run 44246491668](https://github.com/zuizui0223/egwee/actions/runs/44246491668), with synthetic regression and field-fold tests and derivative-only JSON artifacts.

## After-outcome diagnostics — explicitly secondary

After the negative original primary, `POSTPRIMARY_PREDICTIVE_DIAGNOSTIC_FREEZE_20261118.md` specified two complementary descriptive checks on the **unchanged 591 fields**. Neither supersedes the original primary, substitutes a better comparator after seeing outcomes, or constitutes independent evidence.

1. **No-predictor baseline:** intercept-only train-mean Mnull MSE **1.61464157**, M0 MSE **1.67072323**, Mnull−M0 **−0.05608166**, whole-programme 95% bootstrap **[−0.19340419, +0.08164193]**; **7/20** programmes have total-visit M0 better than constant. Even the single total-visitation feature does not robustly improve this simple programme-specific out-of-field prediction beyond training mean. It does **not** mean pollination biologically has no effect.
2. **50 alternate deterministic field folds:** **47/50** train-only estimable (3 alternative split assignments could not be completed because at least one panel had zero training predictor variance). Of the 47 complete comparisons, **46** have negative study-mean M0−M1 gain; **1** positive. Their median study-mean gain is **−0.52632**, 10th to 90th percentile **[−0.75203, −0.23897]**, full min/max **[−3.44561, +0.02144]**. These are repeated splits of the **same original source data**, not independent replication or a formal uncertainty interval.

Source-hash reproduction and original primary unchanged were verified by [Actions 44246898114](https://github.com/zuizui0223/egwee/actions/runs/44246898114).

### Original source guild-total quality audit (post-outcome, no refitting)

The `audit_original_visitation_guild_totals.py` audit only reads the original 591 predictor fields and checks arithmetic/categorical completeness. It does **not** read yield outcomes or rescore the original model.

- **365/591** fields have at least one missing other guild component among ten possible guild columns and therefore no valid *full ten-guild* recomposition of total visit rate.
- **226/591** have all ten numeric guild values; among these **2** differ from the reported total by greater than the registered tolerance (1% or 1 unit); the full sum/total ratio spans approximately **0.984375–1.000000** where defined.
- **1/591** field has the selected Bombus+other-wild-bees+Syrphidae subtotal exceeding the reported overall visit rate by more than the audit's 1% threshold.

This is a **provenance/comparability warning** rather than after-the-fact grounds to remove any unfavorable field or reselect model variables. The source-derived total and guild measures remain as published, and the original negative result is preserved. Reproduced with the frozen primary by [Actions 44247105438](https://github.com/zuizui0223/egwee/actions/runs/44247105438).

## Ecological interpretation and prior art

**Directly supported:** In an original, geographically broad **agricultural** database, the observed relative contribution of wild bees and syrphid flies does not deliver stable additional within-study predictive information for a primary crop-output variable once total source visitation is included; the models are simple and context-specific. This is an informative **sentinel sufficiency / predictive limitation** check, not evidence that floral guild-use divergence is unimportant.

**Not supported:** intrinsic bee vs syrphid floral selectivity, pollinator species-identity effects, compatible pollen arrival, mating quality, mechanistic crop fertilization, a universal no-pollination-effect claim, wild plant fragmentation causality, or a universal Q→P→F stage law. Baseline visits themselves are not strongly predictive here; unknown cultivar, field management, agronomic stress, sampling time/effort, floral stage and source outcome definition are material alternatives. Within-study field CV does not establish out-of-study transportability. The original authors and previous papers have already documented crop production association with pollinator abundance and diversity; **those are not new findings from EGWEE**.

**Relation to concurrent EuPPollNet results:** PR #72 demonstrated source-corrected **positive guild-specific *plant-use* divergence** across 39 European observational research programmes, with PR #74 showing a narrower same-day source-recorded flower-count discrepancy. CropPol is a distinct original observational corpus showing **no comparable incremental *crop-yield* prediction**, but *not* a matched same-site measurement of that EuPPollNet niche partition. Their comparison supports scientific separation of ecological **interactions** and **downstream functions**, not a causal mechanistic link between the two datasets.

## Publication / repository decision

Retain this negative, outcome-blind-frozen study with all post-result diagnostics openly labeled. The next biological generality test should directly measure same plant/site/year guild-specific visitation, effective conspecific pollen/donor compatibility and seed or recruitment outcomes in multiple genuinely independent natural ecosystems, rather than additional outcome-conditioned respecification of CropPol.

- Code: `audit_source_schema.py`, `audit_source_field_grain.py`, `audit_syrphid_coverage_before_qf.py`, `test_frozen_qf_guild_increment.py`, `audit_postprimary_predictive_stability.py`, `audit_original_visitation_guild_totals.py`.
- Four source/primary workflows and one separate postprimary workflow; all executed successfully with source-verified original file bytes.
- **No** third-party original source rows, individual yield values, individual field IDs, prediction records, pollen/genetic records, or source ZIPs are redistributed.
- No alteration of the separate theoretical `egwe`, frozen five-cluster EGWEE fragmentation synthesis, or draft PR #72/#74.
