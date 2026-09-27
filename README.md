## Scale-aware revision complete — validation / administration pending

The mandatory Hedges-g versus oriented-lnRR estimand audit has now been integrated into the manuscript, Figure 4, Table 2, claim ceiling and scale-aware submission freeze v4.

Current scientific status:

- the historical Hedges-g primary analysis remains exactly reproducible;
- its relative-magnitude / leave-one-*Serapias* interpretation is not scale-invariant;
- all 17/17 primary direct effects remain negative on both oriented g and oriented lnRR;
- old variable-bottleneck classifications are retained only as exploratory registered-scale audits;
- filtering, buffering and cohort-lag patterns are post hoc hypotheses for prospective validation.

Submission remains conditional on the current full contract being green and the remaining human administrative fields being approved.

Canonical scale audit:
- [`manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-27_ESTIMAND_SCALE.md`](manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-27_ESTIMAND_SCALE.md)
- [`manuscript/ESTIMAND_SCALE_SENSITIVITY_RESULT_2026-09-27.md`](manuscript/ESTIMAND_SCALE_SENSITIVITY_RESULT_2026-09-27.md)
- [`evidence/meta_extraction/estimand_scale_sensitivity_v1.csv`](evidence/meta_extraction/estimand_scale_sensitivity_v1.csv)
- [`evidence/meta_extraction/estimand_scale_cluster_summary_v1.csv`](evidence/meta_extraction/estimand_scale_cluster_summary_v1.csv)
- [`evidence/meta_extraction/estimand_scale_fisher_sensitivity_v1.csv`](evidence/meta_extraction/estimand_scale_fisher_sensitivity_v1.csv)

# EGWEE — empirical multilayer fragmentation synthesis

This repository is the authoritative development home for an **independent natural-data synthesis of multilayer fragmentation responses in flowering-plant systems**.

## Scientific role

The active paper is a cluster-first empirical synthesis. Its questions are defined from natural-system exposures, effect units and biological endpoints rather than from a finite theoretical model:

1. **Which features of cross-process fragmentation responses are robust to effect-size representation: response direction, relative amplitude, or neither?**
2. **Do the recovered systems suggest filtering, buffering or cohort-lag patterns across mating, reproduction and genetic states that deserve prospective ecological tests?**

EGWEE therefore studies how fragmentation responses propagate across plant interaction, mating, reproductive and genetic processes while explicitly separating scale-stable direction from scale-dependent response amplitude. Theory may motivate downstream interpretation, but it is not an admission criterion, estimator, stopping rule or source of empirical endpoint values.

The active manuscript spine is [`manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md`](manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md). The locked protocol is [`manuscript/META_ANALYSIS_PROTOCOL_2026-09-11.md`](manuscript/META_ANALYSIS_PROTOCOL_2026-09-11.md).

## Current empirical conclusion

The historical primary direct analysis contains **five independent programme/study clusters / 17 marginal effects**. On the registered Hedges-g estimand, the five-cluster Fisher synthesis rejects equality of within-system standardized response magnitudes (`p = 0.01212432`), but omitting ML001 *Serapias lingua* gives `p = 0.18194353`.

That robustness classification is **not scale-invariant**.

A mandatory oriented-lnRR sensitivity constructed from the same positive fragmented/reference summaries changes endpoint ordering and leave-one-cluster interpretation:

- under the existing dimensionless dependence proxy carried onto lnRR variances, omit-*Serapias* rejection remains below 0.05;
- under zero covariance, omit-*Serapias* rejection also remains below 0.05;
- under a covariance-free Cauchy maximum-variance boundary, omit-*Serapias* rejection is **not certified**.

The strongest paper-level conclusion is therefore:

> **Fragmentation-associated deterioration is directionally consistent across the primary direct corpus, but relative response amplitude and layer-separation/robustness conclusions depend on the declared effect-size scale and dependence assumptions.**

All **17/17 primary direct effects are negative** on both oriented Hedges g and oriented lnRR. This is descriptive scale-stable evidence for a common direction of deterioration, not a sign test and not evidence that response magnitudes are equal.

### Why the old Serapias bottleneck headline was withdrawn

ML001 *Serapias* illustrates the scale problem directly:

- Hedges-g absolute ordering: `G > C > F`;
- oriented-lnRR absolute ordering: `C > F > G`;
- Hedges-g C–F difference: resolved;
- lnRR C–F difference under the carried rho proxy: unresolved (`p ≈ 0.605`).

Thus the earlier claim that *Serapias* supplies a resolved upstream movement/connectivity bottleneck is not scale-stable.

### Scale-independent qualitative discordance

The primary direct stream contains **no sign reversal** among its 17 effects.

The clearest qualitative process discordance remains outside that primary direct stream in the separate *Eucalyptus wandoo* gradient, where interaction/pollen quantity is positive while reproductive function is negative on the registered Fisher-z scale.

### Exploratory ecological hypotheses

The lnRR sensitivity exposes biologically interesting but post hoc patterns:

- ML002 *Brosimum*: movement/connectivity declines more strongly than one-year progeny vigour;
- ML014 *Eucalyptus socialis*: mating-support decline is much larger than family growth decline;
- ML003 *Spondias*: juvenile and seed H_O decline more strongly than adult H_O.

These motivate a **filtering / buffering / cohort-lag hypothesis**: fragmentation effects may be attenuated, amplified or delayed as they propagate across mating, reproduction and demographic/genetic states.

This is **hypothesis-generating only**. It is not a confirmed macroecological law and is explicitly separated from the scale-stable primary conclusion.

### Canonical scale audit

- [`manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-27_ESTIMAND_SCALE.md`](manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-27_ESTIMAND_SCALE.md)
- [`manuscript/ESTIMAND_SCALE_SENSITIVITY_RESULT_2026-09-27.md`](manuscript/ESTIMAND_SCALE_SENSITIVITY_RESULT_2026-09-27.md)
- [`evidence/meta_extraction/estimand_scale_sensitivity_v1.csv`](evidence/meta_extraction/estimand_scale_sensitivity_v1.csv)
- [`scripts/check_estimand_scale_sensitivity.py`](scripts/check_estimand_scale_sensitivity.py)

The older 12-programme bottleneck census and associated Q → E → F design remain useful exploratory development work, but they are not current submission-headline evidence until they survive scale-aware reanalysis.

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

Separate gradient/generalisation evidence now contains **six programmes / 19 primary Fisher-z marginal effects**:

- `ML015` *Eucalyptus wandoo*: I / F / G_adult on the response-free fragmentation PC;
- `P2_CF01_ZURICH_2026`: four dependent phytometer I/F panels on the Urban_500 gradient;
- `P2_CF01_MILKWEED_URBAN_2023`: population-level I/F responses along the Toronto urbanisation gradient;
- `P2_CF01_ACER_MIYABEI_2014`: retrospective forest-level C/F isolation-gradient recovery;
- `P2_CF01_CARDIOPETALUM_2012`: retrospective fragment-size I/F recovery, including the resolved interaction-persistence / reproductive-collapse contrast;
- `P2_CF01_PRITCHARD_2005`: retrospective nested-frame orchard-isolation I/F recovery with cluster-robust dependence fallback.

These Fisher-z programmes remain separate from the primary Hedges-g Fisher statistic.

Pair-specific Phase-2 direct coverage is currently:

- **I-F: 3/5 independent programmes** — `ML020`, `P2_CF01_SEVENELLO_2026` and `P2_CF01_BERGSDORF_KAKAMEGA_2006`;
- **C-F: 2/5 independent programmes** — `ML001` plus `ML002`;
- **G_adult-G_offspring: 5/5**, so that preregistered pair-specific analysis gate is open.

The direct **C-F family is now coverage-closed rather than search-pending**. CF01 screened all
**360/360** candidates, **24 C-F-targeted records reached full-text gating**, and **0** of those
records retain a `pending_*` quantitative status. The direct C-F analysis-opening gate therefore
remains closed at 2/5 because no additional candidate satisfied the frozen common-exposure,
effect-unit and marginal-variance rules. EGWEE does not start a new search merely to force K=5.
See `manuscript/PHASE2_CF01_CF_FAMILY_CLOSURE_2026-09-27.md`.

The direct **I-F family is likewise coverage-closed**. After resolving the remaining dissertation,
estimand, graphical-vector and fragmentation-unit variance gates, the full-text ledger contains
**0 `pending_*` quantitative statuses**. Direct I-F coverage is **3/5 independent programmes**
(`ML020`, `P2_CF01_SEVENELLO_2026`, `P2_CF01_BERGSDORF_KAKAMEGA_2006`), so the preregistered
five-programme pooled-analysis gate remains closed. No new search is opened to force K=5; terminal
programmes may be reopened only if their already-specified missing evidence becomes available.
See `manuscript/PHASE2_CF01_IF_FAMILY_CLOSURE_2026-09-27.md`.

Sevenello was recovered after search completion from public raw data under a frozen Edge-versus-Core contract. Its three primary species panels are dependent outcomes inside one programme, all paired covariance blocks are positive definite, and the internal three-panel Bonferroni p is 1.0.

Bergsdorf's Kakamega dissertation was then recovered retrospectively from source site tables under an all-recoverable-panel rule. Four dependent species×campaign panels were retained; *Dracaena fragrans* remains explicitly blocked rather than coded as zero. The programme-level Bonferroni p is 0.006535, driven by strong Acanthopale interaction–function separation, while the other three recovered panels are individually imprecise. Bergsdorf therefore raises **I-F coverage to 3/5**, but, like Sevenello, it does not add a sixth cluster to the frozen Phase-1 five-cluster Fisher synthesis.

The canonical current-state documents are:

- [`manuscript/META_ANALYSIS_CLUSTER_STATUS_2026-09-12.md`](manuscript/META_ANALYSIS_CLUSTER_STATUS_2026-09-12.md)
- [`manuscript/STATE_SEPARATION_SYNTHESIS_RESULT_2026-09-13.md`](manuscript/STATE_SEPARATION_SYNTHESIS_RESULT_2026-09-13.md)
- [`manuscript/AIZEN_FEINSINGER_1994_RECOVERY_RESULT.md`](manuscript/AIZEN_FEINSINGER_1994_RECOVERY_RESULT.md)
- [`manuscript/PHASE2_CF01_CF_FAMILY_CLOSURE_2026-09-27.md`](manuscript/PHASE2_CF01_CF_FAMILY_CLOSURE_2026-09-27.md)
- [`manuscript/PHASE2_CF01_IF_FAMILY_CLOSURE_2026-09-27.md`](manuscript/PHASE2_CF01_IF_FAMILY_CLOSURE_2026-09-27.md)
- [`manuscript/ECOLOGICAL_RESPONSE_REGIMES_2026-09-27.md`](manuscript/ECOLOGICAL_RESPONSE_REGIMES_2026-09-27.md) — ecology-first synthesis of coupled decline, quantity–function decoupling and unresolved I–F regimes.
- [`manuscript/ECOLOGICAL_IF_DIRECTION_CENSUS_2026-09-27.md`](manuscript/ECOLOGICAL_IF_DIRECTION_CENSUS_2026-09-27.md) — complete 8-programme I–F direction census and claim ceiling.
- [`manuscript/ECOLOGICAL_IF_MEASUREMENT_GAP_2026-09-27.md`](manuscript/ECOLOGICAL_IF_MEASUREMENT_GAP_2026-09-27.md) — complete 8/8 quantity-level versus 0/8 effective-mating measurement audit.
- [`manuscript/ECOLOGICAL_BOTTLENECK_POSITION_AUDIT_2026-09-27.md`](manuscript/ECOLOGICAL_BOTTLENECK_POSITION_AUDIT_2026-09-27.md) — secondary 4-programme audit showing that bottleneck position is not fixed; current auxiliary programmes are burned for fresh H2 validation.
- [`manuscript/ECOLOGICAL_PROCESS_FUNCTION_CENSUS_2026-09-27.md`](manuscript/ECOLOGICAL_PROCESS_FUNCTION_CENSUS_2026-09-27.md) — canonical unified 12-programme denominator: 11 testable, 4 resolved (3 downstream F-dominant, 1 upstream process-dominant), 7 unresolved, 1 not testable.
- [`manuscript/ECOLOGICAL_BOTTLENECK_DIRECTION_INFLUENCE_2026-09-27.md`](manuscript/ECOLOGICAL_BOTTLENECK_DIRECTION_INFLUENCE_2026-09-27.md) — leave-one-programme-out claim ceiling: the upstream resolved direction is ML001-dependent.
- [`manuscript/ECOLOGICAL_QUANTITY_FUNCTION_MECHANISM_AUDIT_2026-09-27.md`](manuscript/ECOLOGICAL_QUANTITY_FUNCTION_MECHANISM_AUDIT_2026-09-27.md) — evidence-graded mechanism audit separating source-supported pollen-quality/mating constraints from unresolved mechanism.
- [`manuscript/ECOLOGICAL_NEAREST_NEIGHBOR_NOVELTY_AUDIT_2026-09-27.md`](manuscript/ECOLOGICAL_NEAREST_NEIGHBOR_NOVELTY_AUDIT_2026-09-27.md) — novelty firewall: prior syntheses establish average pollination–reproduction coupling; EGWEE contributes paired within-programme response geometry and the complete direction census.
- [`manuscript/FRESH_ECOLOGICAL_IF_VALIDATION_PREREGISTRATION_2026-09-27.md`](manuscript/FRESH_ECOLOGICAL_IF_VALIDATION_PREREGISTRATION_2026-09-27.md) — future-only validation of the downstream reproductive-bottleneck hypothesis; all current eight I–F programmes are burned discovery systems.
- [`manuscript/FRESH_ECOLOGICAL_IF_VALIDATION_AMENDMENT_2026-09-27_BOTTLENECK_LOCALIZATION.md`](manuscript/FRESH_ECOLOGICAL_IF_VALIDATION_AMENDMENT_2026-09-27_BOTTLENECK_LOCALIZATION.md) — prospective H2-v2 amendment: effective mating localizes the bottleneck; primary fresh contrast is ΔQE = Q−E rather than mandatory recoupling.
- [`manuscript/FRESH_ECOLOGICAL_IF_SYNCHRONIZED_FIELD_MODULE_V1.md`](manuscript/FRESH_ECOLOGICAL_IF_SYNCHRONIZED_FIELD_MODULE_V1.md) — synchronized quantity → effective mating → reproductive-function field design for genuinely fresh systems.
- [`manuscript/SUBMISSION_FREEZE_2026-09-27.md`](manuscript/SUBMISSION_FREEZE_2026-09-27.md) — ecology-first submission freeze and remaining human-only blockers.
- [`manuscript/SUBMISSION_ADMIN_HANDOFF_2026-09-27.md`](manuscript/SUBMISSION_ADMIN_HANDOFF_2026-09-27.md) — exact human-only fields to complete before submission; anonymous scientific files should remain identity-free.
- [`manuscript/REVIEWER_RISK_AUDIT_2026-09-27.md`](manuscript/REVIEWER_RISK_AUDIT_2026-09-27.md) — red-team audit of novelty, post-hoc integration, effect-family heterogeneity, bottleneck terminology and Serapias influence.

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
