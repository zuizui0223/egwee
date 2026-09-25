# EGWEE — empirical multilayer fragmentation synthesis

This repository is the authoritative development home for an **independent natural-data synthesis of multilayer fragmentation responses in flowering-plant systems**.

## Scientific role

The active paper is a cluster-first empirical synthesis. Its questions are defined from natural-system exposures, effect units and biological endpoints rather than from a finite theoretical model:

1. **Do interaction, movement, reproduction and genetic responses have exchangeable fragmentation effects within natural systems?**
2. **If not, do separated and concordant response geometries recur across independent systems, and which prespecified biological contexts explain that heterogeneity once replication permits?**

EGWEE therefore estimates the empirical geometry of fragmentation responses. Theory may motivate interpretation, but it is not an admission criterion, estimator, stopping rule or source of empirical endpoint values.

The active manuscript spine is [`manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md`](manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md). The locked protocol is [`manuscript/META_ANALYSIS_PROTOCOL_2026-09-11.md`](manuscript/META_ANALYSIS_PROTOCOL_2026-09-11.md).

## Current empirical conclusion

The primary direct-effect family now contains **five independent programme/study clusters / 17 marginal effects**. The five-cluster Fisher synthesis rejects complete layer exchangeability (`p = 0.01212432`), but the result is **not Serapias-independent**: omitting ML001 *Serapias lingua* gives `p = 0.18194353`.

The fifth cluster, the replicated Aizen–Feinsinger Chaco programme, was admitted regardless of significance and shows fragmentation-associated deterioration in both pollination interaction and reproductive function without detectable I–F separation (`p_ML020 = 1.0`).

The defensible paper-level conclusion is therefore:

> **Fragmented plant systems include both separated and concordant biological response regimes. The present corpus contains strong state separation, but the pooled direct-effect rejection is materially dependent on Serapias and does not support a universal fragmentation state-separation syndrome.**

This is an empirical statement about natural response geometry. It neither tests nor validates the finite NEE operator sequence, warning rules or reserve quantities.

## Meta-analysis architecture

Primary response layers:

- `D_resource_demography`
- `I_interaction`
- `C_movement_connectivity`
- `F_reproductive_function`
- `G_adult`
- `G_offspring`

The primary effect stream uses direct fragmented-versus-reference contrasts represented as Hedges' `g`, oriented so negative values mean lower support/function under fragmentation. Continuous-only fragmentation gradients are retained in a separate Fisher-`z(r)` stream rather than silently mixed with the primary effect scale.

Multiple effects from one study/species remain clustered. Species sharing the same programme landscapes do not become independent systems. Missing layers are not zero effects. Adult and offspring genetic measurements are kept separate.

## Current primary evidence

Primary direct clusters:

- `ML001` *Serapias lingua*: C / F / G_adult;
- `ML002` *Brosimum alicastrum*: C / F;
- `ML003` *Spondias purpurea*: C / G_adult / G_offspring;
- `ML014` *Eucalyptus socialis*: G_mating / F;
- `ML020` Aizen–Feinsinger Chaco programme: three dependent species × I / F, counted once.

Separate gradient/generalisation evidence now contains **five programmes / 17 primary Fisher-z marginal effects**:

- `ML015` *Eucalyptus wandoo*: I / F / G_adult on the response-free fragmentation PC;
- `P2_CF01_ZURICH_2026`: four dependent phytometer I/F panels on the Urban_500 gradient;
- `P2_CF01_MILKWEED_URBAN_2023`: population-level I/F responses along the Toronto urbanisation gradient;
- `P2_CF01_ACER_MIYABEI_2014`: retrospective forest-level C/F isolation-gradient recovery;
- `P2_CF01_CARDIOPETALUM_2012`: retrospective fragment-size I/F recovery, including the resolved interaction-persistence / reproductive-collapse contrast.

These Fisher-z programmes remain separate from the primary Hedges-g Fisher statistic.

The canonical current-state documents are:

- [`manuscript/META_ANALYSIS_CLUSTER_STATUS_2026-09-12.md`](manuscript/META_ANALYSIS_CLUSTER_STATUS_2026-09-12.md)
- [`manuscript/STATE_SEPARATION_SYNTHESIS_RESULT_2026-09-13.md`](manuscript/STATE_SEPARATION_SYNTHESIS_RESULT_2026-09-13.md)
- [`manuscript/AIZEN_FEINSINGER_1994_RECOVERY_RESULT.md`](manuscript/AIZEN_FEINSINGER_1994_RECOVERY_RESULT.md)

## Search stop and claim discipline

The primary five-cluster direct-effect corpus remains frozen. A sixth primary cluster is **not** sought merely because removal of ML001 eliminates significance.

The separately preregistered Phase-2 CF01 coverage expansion is now **search-complete: 360/360 target-pair candidates screened, pending screen = 0**. This satisfies the coverage programme's stopping rule because the deterministic candidate queue is exhausted—not because any pair reached a desired K or significance threshold.

Search completion does **not** mean every full-text/effect-unit gate is resolved. Design-valid candidates with access, variance, common-frame, publication-identity or estimand blockers remain explicitly open/STOPped under their frozen rules and may be reopened only when the stated missing evidence becomes available.

The current evidence does not yet support headline claims for a universal cohort/history lag or a general process-compensation law. Those remain secondary hypotheses until the number of independent same-frame clusters is sufficient.

## Search basis

The initial synthesis search started from major existing meta-analysis datasets/reference lists through 2026-09-11. Phase-2 then expanded the CF01 citation graph under the separately frozen coverage contract through its 2026-09-18 cutoff. The resulting target-pair queue contains **360 candidates and is fully screened**. See [`manuscript/meta_analysis_seed_sources.md`](manuscript/meta_analysis_seed_sources.md), [`manuscript/CF01_CANDIDATE_SCREENING_CONTRACT_2026-09-23.md`](manuscript/CF01_CANDIDATE_SCREENING_CONTRACT_2026-09-23.md), and [`manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE36_2026-09-25.md`](manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE36_2026-09-25.md).

Repository-audited systems such as *Crepis sancta*, Miyake-jima *Camellia japonica–Zosterops japonicus*, *Conospermum undulatum* and *Spondias purpurea* remain mechanistic anchors, not automatic quantitative inclusions. The candidate ledger is [`manuscript/meta_analysis_candidate_ledger.csv`](manuscript/meta_analysis_candidate_ledger.csv).

## Role of the previous four-gate programme

The seven locked natural-data analyses and the earlier four-gate workflow are retained as **quality-control/provenance material**, not the active paper-level claim. They remain useful for enforcing:

- endpoint-relevant measurement;
- information-preserving representation;
- correct ecological holdout/effect units;
- explicit `not_identifiable` / access-STOP outcomes;
- no post-result proxy repair.

The historical spine is [`manuscript/natural_data_ecological_indicators_spine.md`](manuscript/natural_data_ecological_indicators_spine.md).

## Repository map

- `manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md` — active results-bearing manuscript spine.
- `manuscript/META_ANALYSIS_PROTOCOL_2026-09-11.md` — frozen screening/effect/model protocol.
- `manuscript/META_ANALYSIS_CLUSTER_STATUS_2026-09-12.md` — canonical cluster-first evidence state.
- `manuscript/STATE_SEPARATION_SYNTHESIS_RESULT_2026-09-13.md` — canonical cross-cluster synthesis and leave-one-out result.
- `manuscript/meta_analysis_effect_schema.json` — extraction and dependence schema.
- `manuscript/meta_analysis_seed_sources.md` — prior syntheses and seed literature.
- `evidence/` — locked quantitative evidence and historical natural-data analyses.
- `background/` — natural mechanism audits and measurement crosswalk.

## Hard boundary with EGC / EGWE

[`zuizui0223/egc`](https://github.com/zuizui0223/egc) and [`zuizui0223/egwe`](https://github.com/zuizui0223/egwe) belong to the NEE theory/mechanism programme. In particular, `egwe` owns the finite-model operator and functional-reserve claims.

EGWEE owns the **natural-data empirical synthesis**. It does not import simulated endpoint values, operator outputs or theoretical success criteria into screening or estimation. Candidate ordering, effect-unit admission, endpoint assignment, Phase-2 stopping and promotion are fixed by empirical contracts independently of whether a result agrees with NEE.

The permitted connection is downstream interpretation: EGWEE can constrain which empirical phenomena a useful theory must explain, and NEE can cite EGWEE as external natural evidence. Neither repository may relabel EGWEE results as validation of a specific finite operator sequence.
