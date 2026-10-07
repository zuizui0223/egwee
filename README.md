## Ecological generality promotion — scientific validation pending refresh

The current revision promotes one ecological principle beyond the earlier proxy-failure wording:

> **Fragmentation can be directionally coherent yet diagnostically insufficient: pollination can track reproductive decline on average without uniquely identifying reproductive state in a focal system.**

The promotion gate now requires all of the following to hold simultaneously:

- all **17/17** primary direct effects are negative on both oriented Hedges g and oriented lnRR;
- the frozen **16-programme** interaction→function map remains non-identifying after deletion of every single programme;
- removing all `no_detected_loss` and `mixed` states leaves an **8-programme** explicit-direction map that remains non-identifying after every single-programme deletion;
- restricting to **13 visitation/abundance programmes** still leaves a leave-one-out non-identifying map;
- a corrected external Aguilar et al. public-S1 reanalysis independently generalizes the same structure: **12/54** minimum sign mismatches across habitat-fragmentation pairs, with publication-LOO minimum **8** and species-LOO minimum **11**;
- after deleting every publication overlapping the frozen EGWEE I–F map, **31** external pairs still retain **7** mismatches (publication-LOO minimum **5**, species-LOO minimum **6**);
- in that external subset, pollination effect magnitude is positively associated with female-fitness effect (`beta=+0.190`, `p=0.0053`), yet pollination sign gives **zero incremental binary classification gain** over simply knowing that the system is fragmented (12 vs 12 errors; source-disjoint 7 vs 7);
- the best deterministic interaction-only lookup still leaves at least **5** mismatches in the full map, **2** in the strict map and **1** in the strict quantitative-only subset;
- observed interaction decline is **neither necessary nor sufficient** for observed reproductive decline in the mixed-tier evidence universe, and both logical failures survive every single-programme deletion.

The strongest resolved quantitative surprise is narrower and asymmetric: **false reassurance**. Three independent programmes—*Eucalyptus wandoo*, *Cardiopetalum calophyllum* and Kakamega *Acanthopale pubescens*—show representation-stable downstream mismatch, span three continents and three plant families, and use upstream indicators ranging from visitation/abundance to pollen tubes.

A source-level reliability audit makes a simple measurement-noise explanation less plausible: equal-latent-effect attenuation models misfit all three anchors (descriptive `p<0.01` for each), and the fitted artifact-null probability of a downstream-resolved contrast is <0.03 in each programme. These are post hoc diagnostics, not a joint confirmatory p-value or prevalence estimate.

The mechanistic interpretation remains prospective. All **8/8** quantitative I–F programmes measure interaction/pollen quantity, while **0/8** directly measure compatible mating quality on the same frame. Source-disjoint external mismatches show that one hidden mating layer is too narrow: *Samanea* buffers seed output despite reduced effective pollination, whereas *Tristerix* retains pollination while seed dispersal collapses. The leading biological hypothesis is therefore a **branching reproductive life cycle** in which fragmentation can alter interaction quantity, mating provenance, plant/post-transfer condition, compensatory reproduction and later dispersal/recruitment semi-independently before they converge on reproductive function.

Current scientific files have changed since the last green full-package run, so `submission_ready=false` remains intentional until the refreshed full CI and anonymous reviewer package pass again.

Canonical promotion files:
- [`evidence/meta_extraction/ecological_generality_surprise_promotion_v1.json`](evidence/meta_extraction/ecological_generality_surprise_promotion_v1.json)
- [`manuscript/ECOLOGICAL_GENERALITY_AND_SURPRISE_2026-09-29.md`](manuscript/ECOLOGICAL_GENERALITY_AND_SURPRISE_2026-09-29.md)
- [`manuscript/IF_TRANSLATION_NONIDENTIFIABILITY_2026-10-03.md`](manuscript/IF_TRANSLATION_NONIDENTIFIABILITY_2026-10-03.md)
- [`manuscript/IF_SENTINEL_DETERMINISM_2026-10-05.md`](manuscript/IF_SENTINEL_DETERMINISM_2026-10-05.md)
- [`manuscript/SF06_TRANSLATION_RESIDUAL_RESULT_2026-10-06.md`](manuscript/SF06_TRANSLATION_RESIDUAL_RESULT_2026-10-06.md)
- [`manuscript/SF06_INCREMENTAL_SENTINEL_VALUE_2026-10-07.md`](manuscript/SF06_INCREMENTAL_SENTINEL_VALUE_2026-10-07.md)
- [`manuscript/SF06_SOURCE_DISJOINT_BRANCHING_ANCHORS_2026-10-07.md`](manuscript/SF06_SOURCE_DISJOINT_BRANCHING_ANCHORS_2026-10-07.md)
- [`manuscript/SENTINEL_NOVELTY_BOUNDARY_2026-10-07.md`](manuscript/SENTINEL_NOVELTY_BOUNDARY_2026-10-07.md)
- [`manuscript/SF06_OUTCOME_EXPOSURE_TIMELINE_2026-10-06.md`](manuscript/SF06_OUTCOME_EXPOSURE_TIMELINE_2026-10-06.md)
- [`manuscript/INTERACTION_DECLINE_NECESSITY_SUFFICIENCY_2026-10-03.md`](manuscript/INTERACTION_DECLINE_NECESSITY_SUFFICIENCY_2026-10-03.md)
- [`manuscript/IF_RELIABILITY_SUFFICIENCY_2026-10-06.md`](manuscript/IF_RELIABILITY_SUFFICIENCY_2026-10-06.md)
- [`manuscript/HIDDEN_EFFECTIVE_MATING_LAYER_HYPOTHESIS_2026-10-03.md`](manuscript/HIDDEN_EFFECTIVE_MATING_LAYER_HYPOTHESIS_2026-10-03.md)
- [`scripts/check_ecological_generality_and_surprise.py`](scripts/check_ecological_generality_and_surprise.py)


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

- under raw-unit multivariate delta covariance reconstructed from aligned independent units, omit-*Serapias* rejection remains below 0.05 (`p = 8.31e-05`);
- under zero covariance, omit-*Serapias* rejection also remains below 0.05;
- under a covariance-free Cauchy maximum-variance boundary, omit-*Serapias* rejection is **not certified**.

The strongest paper-level conclusion is therefore:

> **Fragmentation-associated deterioration is directionally consistent across the primary direct corpus, but relative response amplitude and layer-separation/robustness conclusions depend on the declared effect-size scale and dependence assumptions.**

All **17/17 primary direct effects are negative** on both oriented Hedges g and oriented lnRR. This is descriptive scale-stable evidence for a common direction of deterioration, not a sign test and not evidence that response magnitudes are equal.

### Strongest ecological lead: interaction quantity can provide false reassurance

Across the current process–function catalogue, the **representation-stable resolved mismatches are asymmetric**. The three programmes that remain clearly downstream function-dominant under their audited representations are:

- *Eucalyptus wandoo* — pollen-tube quantity increases while seed production declines;
- *Cardiopetalum calophyllum* — pollinator abundance changes weakly while fruit set declines strongly;
- Kakamega *Acanthopale pubescens* — visitation occurrence is maintained/slightly elevated while fruit set declines, and the geometry survives g→lnRR re-expression.

These programmes span Western Australia, Brazilian cerrado and western Kenya; Myrtaceae, Annonaceae and Acanthaceae; and very different pollination/mating systems.

At the same time, all **8/8** registered I–F programmes measure interaction/pollen **quantity**, while **0/8** directly measure compatible mating quality on the same frame.

The resulting exploratory generalization is:

> **Observed interaction evidence state is non-identifying for observed reproductive-function state in the frozen matched evidence universe, and the same many-to-many logic persists in a source-publication-disjoint external public-S1 subset.**

A frozen 16-programme translation map now broadens this without changing the quantitative denominator: 8 quantitatively admitted I–F programmes plus 8 non-overlapping qualitative-blocked programmes show that the **same interaction signal can map to multiple reproductive-function states**. The stronger general statement is therefore that interaction quantity is a **non-identifying stand-alone sentinel** of reproductive function across the audited fragmentation contexts. The corrected external SF06 public-S1 analysis now extends this beyond the frozen EGWEE source set: association can remain positive on the continuous effect scale while the upstream sign fails to improve binary diagnosis of downstream impairment. This is an existence/topology and diagnostic-sufficiency result, not a prevalence estimate.

The logical audit contains both counterexample classes at the level of observed evidence states: reproductive decline is observed without detected interaction decline, and interaction decline is observed with more than one reproductive state. Both classes survive every single-programme deletion in the mixed-tier 16-programme map; quantitative-only leave-one-out robustness is not claimed.

This is not a prevalence estimate and does not imply one shared mechanism. The canonical audit is `manuscript/SCALE_STABLE_QUANTITY_FUNCTION_PROXY_FAILURE_2026-09-29.md`.

### Exploratory transition-filtering principle

The current data also motivate a broader non-monotonic propagation hypothesis:

- interaction quantity → F can amplify or invert;
- movement/mating → F shows the same process-more-negative point ordering in all three direct anchors on both g and lnRR, although significance is scale-sensitive;
- adult → offspring genetic lag is **not** general: the preregistered five-programme contrast is +0.129 with 95% CI spanning zero.

The proposed general principle is **transition-specific filtering**, not one universal bottleneck or one monotonic upstream→downstream gradient. See `manuscript/TRANSITION_SPECIFIC_FILTERING_AUDIT_2026-09-29.md`.

Canonical synthesis: `manuscript/ECOLOGICAL_GENERALITY_AND_SURPRISE_2026-09-29.md`.


ML020 Chaco remains the key same-direction low-power counterexample: its registered programme difference test gives `p_ML020=1.0`. With four independent habitat units per condition, this means **the I–F magnitude difference is unresolved**, not that the true interaction and reproductive effects are demonstrated equal or biologically coupled.

### Why the old Serapias bottleneck headline was withdrawn

ML001 *Serapias* illustrates the scale problem directly:

- Hedges-g absolute ordering: `G > C > F`;
- oriented-lnRR absolute ordering: `C > F > G`;
- Hedges-g C–F difference: resolved;
- lnRR C–F difference under raw-unit multivariate delta covariance: unresolved (`p = 0.6364`).

Thus the earlier claim that *Serapias* supplies a resolved upstream movement/connectivity bottleneck is not scale-stable.

### Supporting point-sign topology — uncertainty matters

The broader matched I–F evidence contains **18 primary panels from 8 programmes**. Six panels have opposite I/F **point-estimate** signs across five programmes, in both directions.

However, the uncertainty audit changes how this result is described:

- both marginal endpoint directions individually resolved opposite at 95%: **0 / 6**;
- one endpoint resolved and the other unresolved: **2 / 6** (*Eucalyptus wandoo*; Kakamega *Acanthopale*);
- both endpoints unresolved: **4 / 6** (Sevenello ×2; Zurich *Onobrychis*; Toronto milkweed).

Three of four multi-panel programmes also contain more than one point-sign topology under one registered exposure frame, but species-specific fragmentation responses are already known and these categories are often imprecise. This is therefore **supporting descriptive topology**, not six confirmed sign reversals and not the sole novelty claim.

Canonical uncertainty audit:
- [`manuscript/IF_SIGN_UNCERTAINTY_2026-10-01.md`](manuscript/IF_SIGN_UNCERTAINTY_2026-10-01.md)
- [`evidence/meta_extraction/if_sign_uncertainty_v1.csv`](evidence/meta_extraction/if_sign_uncertainty_v1.csv)
- [`scripts/check_if_sign_uncertainty.py`](scripts/check_if_sign_uncertainty.py)

### Exploratory ecological hypotheses

The lnRR sensitivity exposes biologically interesting but post hoc patterns:

- ML002 *Brosimum*: movement/connectivity declines more strongly than one-year progeny vigour;
- ML014 *Eucalyptus socialis*: mating-support decline is much larger than family growth decline;
- ML003 *Spondias*: juvenile and seed H_O decline more strongly than adult H_O.

These motivate a **filtering / buffering / cohort-lag hypothesis**: fragmentation effects may be attenuated, amplified or delayed as they propagate across mating, reproduction and demographic/genetic states.

This is **hypothesis-generating only**. It is not a confirmed macroecological law and is explicitly separated from the scale-stable primary conclusion.

### Canonical scale audit

Authoritative 2026-09-29 files:

- [`manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-29_EFFECT_SCALE.md`](manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-29_EFFECT_SCALE.md)
- [`manuscript/ESTIMAND_SCALE_ROBUSTNESS_2026-09-29.md`](manuscript/ESTIMAND_SCALE_ROBUSTNESS_2026-09-29.md)
- [`manuscript/BOTTLENECK_SCALE_ROBUSTNESS_2026-09-29.md`](manuscript/BOTTLENECK_SCALE_ROBUSTNESS_2026-09-29.md)
- [`evidence/meta_extraction/estimand_scale_robustness_v1.csv`](evidence/meta_extraction/estimand_scale_robustness_v1.csv)
- [`evidence/meta_extraction/bottleneck_scale_robustness_v1.csv`](evidence/meta_extraction/bottleneck_scale_robustness_v1.csv)
- [`scripts/check_estimand_scale_robustness.py`](scripts/check_estimand_scale_robustness.py)
- [`scripts/check_bottleneck_scale_robustness.py`](scripts/check_bottleneck_scale_robustness.py)

The earlier 2026-09-27 estimand sensitivity and registered-scale bottleneck files remain provenance. The 12-programme process–function catalogue is now **exploratory registered-scale evidence**: downstream identity is stable across the audited representations, but upstream system attribution changes with effect scale.

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
