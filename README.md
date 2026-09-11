# EGWEE — empirical multilayer fragmentation synthesis

This repository is the authoritative development home for the **natural-data empirical counterpart to the NEE eco-genetic fragmentation theory**.

## Scientific role

The active paper is now a multilevel meta-analysis rather than a methodological four-gate paper.

The NEE theory asks:

1. **Does fragmentation produce one biological deterioration state?**
2. **If not, which cross-layer processes and remaining functional reserve determine divergent futures?**

EGWEE tests the empirical counterpart across flowering-plant systems:

1. **Do resource/demographic support, pollinator interaction, movement/gene flow, reproductive function, adult genetics and offspring genetics show the same fragmentation effect within natural systems?**
2. **Is cross-layer discordance structured by mating system, pollination/movement mode, reproductive assurance, cohort identity and fragmentation history?**

The active manuscript spine is [`manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md`](manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md). The locked protocol is [`manuscript/META_ANALYSIS_PROTOCOL_2026-09-11.md`](manuscript/META_ANALYSIS_PROTOCOL_2026-09-11.md).

## Target conclusion

The paper does **not** seek another grand mean showing that fragmentation is harmful. Existing meta-analyses already establish negative average effects for pollination/reproduction, genetic diversity/progeny quality, and pollinator abundance in many systems.

The new target is whether those biological layers move together. The empirical hypothesis is:

> **Fragmentation is generally detrimental, but it does not act as one biological deterioration state: interaction, movement, reproduction and genetic responses can differ systematically in magnitude and timing, with process compensation and cohort history explaining part of the discordance.**

This is the natural-data analogue of NEE state separation. It does not claim that the finite NEE operators are literally validated in nature.

## Meta-analysis architecture

Primary response layers:

- `D_resource_demography`
- `I_interaction`
- `C_movement_connectivity`
- `F_reproductive_function`
- `G_adult`
- `G_offspring`

The primary effect stream uses direct fragmented-versus-reference contrasts represented as Hedges' `g`, oriented so negative values mean lower support/function under fragmentation. Continuous-only fragmentation gradients are retained in a separate Fisher-`z(r)` stream rather than silently mixed with the primary effect scale.

Multiple effects from one study/species remain clustered. Missing layers are not zero effects. Adult and offspring genetic measurements are kept separate.

## Search basis

Screening starts from major existing meta-analysis datasets/reference lists and then extends forward through 2026-09-11. See [`manuscript/meta_analysis_seed_sources.md`](manuscript/meta_analysis_seed_sources.md).

Repository-audited systems such as *Crepis sancta*, Miyake-jima *Camellia japonica–Zosterops japonicus*, *Conospermum undulatum* and *Spondias purpurea* are pre-specified mechanistic anchors, not the full sample. The seed candidate ledger is [`manuscript/meta_analysis_candidate_ledger.csv`](manuscript/meta_analysis_candidate_ledger.csv).

## Role of the previous four-gate programme

The seven locked natural-data analyses and the four-gate workflow are retained as **quality-control/provenance material**, not the active paper-level claim. They remain useful for enforcing:

- endpoint-relevant measurement;
- information-preserving representation;
- correct ecological holdout units;
- explicit `not_identifiable` / access-STOP outcomes;
- no post-result proxy repair.

They should inform eligibility and extraction decisions but should not make EGWEE read as a methods paper.

The historical spine is [`manuscript/natural_data_ecological_indicators_spine.md`](manuscript/natural_data_ecological_indicators_spine.md).

## Repository map

- `manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md` — active empirical meta-analysis paper spine.
- `manuscript/META_ANALYSIS_PROTOCOL_2026-09-11.md` — frozen screening/effect/model protocol before synthesis.
- `manuscript/meta_analysis_effect_schema.json` — extraction and dependence schema.
- `manuscript/meta_analysis_seed_sources.md` — prior syntheses and seed literature.
- `manuscript/meta_analysis_candidate_ledger.csv` — first-pass natural-system candidates.
- `evidence/` — historical locked system-level natural-data analyses; retained as QC/provenance.
- `background/` — natural mechanism audits and measurement crosswalk.

## Relationship to EGC / EGWE

[`zuizui0223/egc`](https://github.com/zuizui0223/egc) provides the state-separation evidence used as Question 1 of the active NEE theory paper. [`zuizui0223/egwe`](https://github.com/zuizui0223/egwe) owns the active NEE manuscript and Question 2 operator/reserve theory.

EGWEE is the **empirical synthesis**: it asks whether comparable natural systems actually show cross-layer state separation and whether biological process/cohort moderators explain that heterogeneity.

The repositories remain separate evidence/provenance units. EGWEE may support or challenge the NEE predictions, but it is not allowed to manufacture agreement by selecting only illustrative systems or by pooling incompatible effect measures.
