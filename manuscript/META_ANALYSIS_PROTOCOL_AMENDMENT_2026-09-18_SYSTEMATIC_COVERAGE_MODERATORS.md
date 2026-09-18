# Protocol amendment — systematic coverage and moderator expansion

**Locked development date:** 2026-09-18  
**Parent protocol:** `manuscript/META_ANALYSIS_PROTOCOL_2026-09-11.md`  
**Frozen baseline manuscript:** `manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md`

**Canonical Phase-2 protocol amendment:** this file supersedes the two 2026-09-17 coverage/moderator draft amendments for all prospective decisions after 2026-09-18. The canonical machine contract is `manuscript/meta_analysis_phase2_contract.json`; `manuscript/meta_analysis_coverage_frame_v2.csv`, `manuscript/meta_analysis_moderator_schema_v1.csv`, `manuscript/meta_analysis_recovery_priority_v2.csv` and `evidence/meta_extraction/coverage_expansion_pair_coverage_v1.csv` are its registries.

## 1. Purpose and non-significance-repair firewall

The completed five-cluster synthesis is retained as a frozen baseline. It established a bounded result: natural plant fragmentation systems can show either cross-layer separation or concordant deterioration, but the five-cluster Fisher rejection is materially ML001-*Serapias* dependent and is not covariance-free certified.

This amendment does **not** authorize a sixth-cluster search to restore leave-one-cluster-out significance. It reopens the broader multilevel meta-analysis originally specified on 2026-09-11 for a different, prospectively declared objective:

> **estimate the geometry of natural cross-layer fragmentation responses and identify which biological conditions are associated with concordant versus decoupled responses.**

Candidate recovery, search expansion and prioritization must therefore be based on layer coverage, moderator coverage, independent-unit validity and source recoverability, never on whether a candidate's reported result is significant or points toward state separation.

The existing five-cluster Fisher test remains a historical/baseline result. It is not the primary estimand of the expansion phase and is not recomputed repeatedly as new candidates are screened.

## 2. Expansion questions

The expansion phase asks four questions.

1. **Layer effects:** what is the average fragmentation response within each biological layer?
2. **Paired response geometry:** within the same system and fragmentation exposure, how different are prespecified layer pairs?
3. **Cohort/history lag:** when adult and offspring genetic responses are measured, are contemporary offspring responses more strongly coupled to fragmentation than standing adult responses?
4. **Process–function coupling:** when interaction or movement/connectivity and reproductive function are measured in the same system, do their responses covary, and is that coupling modified by reproductive assurance, pollination vector, longevity or fragmentation history?

These questions were already present in the parent protocol but could not be stably estimated from the first admitted corpus. This amendment defines the coverage work required before they are reopened quantitatively.

## 3. Search universe

### 3.1 Seed-synthesis universe

The candidate universe begins from **all primary studies** cited by the quantitative syntheses already named in the parent protocol:

- pollination and reproductive responses to fragmentation;
- plant genetic responses to fragmentation;
- progeny genetic/biological quality under fragmentation;
- plant fine-scale genetic structure under fragmentation;
- recent pollination/fitness synthesis;
- recent insect-pollinator fragmentation synthesis where a flowering-plant system can be linked to plant responses.

Primary-study lists are deduplicated by DOI, title, species, location/programme and campaign year. A study is a candidate if metadata indicate at least one eligible plant response layer; it is not required to be positive or significant.

### 3.2 Forward/backward expansion

For every seed primary study and every already registered EGWEE programme, backward-reference and forward-citation searching is conducted through **2026-09-18**. New records are linked to an existing programme when they reuse the same landscapes, populations, experimental blocks, cohorts or source observations.

Search logging records query/source, date, candidate DOI/title, programme linkage decision and screening status. The candidate-universe ledger must be frozen before newly discovered effect magnitudes are entered into quantitative extraction.

### 3.3 Database/API reproducibility

At least one reproducible public bibliographic route (e.g. OpenAlex/Crossref metadata plus cited-by/reference links where available) is used to materialize the search ledger. Additional publisher/database searches may supplement it, but exact source, date and query are logged. Search-engine ranking is never used as an inclusion criterion.

## 4. Candidate admission

The parent protocol's effect-unit and same-exposure rules remain binding. An expansion candidate contributes to a paired response analysis only when:

1. at least two prespecified biological layers share the same source-defined fragmentation exposure;
2. the fragmentation-level independent unit is recoverable;
3. signed effects and sampling uncertainty can be reconstructed without promoting nested flowers, plants, progeny, loci or repeated measures to independent fragmentation replicates;
4. duplicate or linked campaigns are assigned one programme identity before effect calculation;
5. endpoint-to-layer assignment is fixed before the candidate effect is calculated.

Single-layer studies may contribute to layer-specific grand means and moderator coverage, but never masquerade as paired evidence.

## 5. Primary expanded estimands

The expansion phase does not reduce each cluster to one p-value. It retains effect magnitudes.

For system/programme (s) and layer (l), let (g_{sl}) be the oriented standardized fragmentation response.

### 5.1 Layer-specific means

Where coverage is adequate, estimate layer-specific mean responses with a multilevel random-effects model,

[
g_{sl} = alpha + eta_l + u_s + epsilon_{sl},
]

with programme/study dependence handled by a sampling covariance matrix when reconstructable and cluster-robust/multilevel inference otherwise.

### 5.2 Prespecified paired contrasts

For two layers (a,b) in the same system,

[
Delta_{s,ab}=g_{s,a}-g_{s,b},
]

with

[
V(Delta_{s,ab})=V_{s,a}+V_{s,b}-2operatorname{Cov}(g_{s,a},g_{s,b}).
]

Primary contrast families are inherited from the 2026-09-11 protocol:

- (I-F);
- (C-F);
- (G_{adult}-G_{offspring});
- (G_{adult}-operatorname{mean}(I,F)) when all required layers share the same exposure frame.

Secondary descriptive contrasts may be stored, but no new headline pair is selected because it yields a large difference.

### 5.3 System-wide severity is not state separation

A system may have strongly negative responses in every layer and little cross-layer separation. Conversely, moderate average deterioration may coexist with strong layer discordance. Therefore overall mean deterioration and paired layer contrasts are reported as distinct quantities.

No single “separation score” based on the largest observed layer difference is used as a primary outcome.

## 6. Moderator hypotheses

Moderator extraction is outcome-independent. The following variables are frozen before the expansion extraction opens new effect magnitudes:

- mating system: self-incompatible / self-compatible / mixed / unknown;
- autonomous reproductive assurance: explicit quantitative measure / present qualitatively / absent / unknown;
- pollination vector: invertebrate / vertebrate / abiotic / mixed / unknown;
- life form and longevity class;
- adult versus progeny/juvenile genetic cohort;
- time since fragmentation/disturbance where source-supported;
- fragmentation component: area / isolation-connectivity / composite / edge / source-defined binary contrast;
- direct process measurement versus proxy;
- study design: observational / experiment;
- biome and region as secondary descriptors.

A category such as “compensated” may **not** be defined from the observed reproductive response and then reused as its own explanatory moderator.

## 7. Quantitative opening gates

To prevent unstable moderator fitting, analyses open only after the following coverage gates are met.

### 7.1 Pair-specific meta-analysis gate

A prespecified layer-pair contrast is promoted from descriptive reporting to a random-effects/meta-regression estimate only with:

- at least **5 independent programme/study clusters**, and
- at least **3 independent clusters contributing to each level** of any categorical moderator used in that pair-specific model.

### 7.2 Moderator gate

A categorical moderator interaction with layer/pair response opens only with:

- at least **10 independent programme/study clusters** in the relevant analysis family, and
- at least **4 clusters per non-reference category** after unknown values are separated.

A continuous moderator opens only with at least **10 independent clusters** spanning at least three distinct source programmes/regions and no single cluster contributing more than 25% of the effective precision.

If these gates are not met, moderator patterns remain descriptive and are not promoted through exploratory p-value searching.

### 7.3 Cohort-lag gate

The adult-versus-offspring genetic contrast opens quantitatively with at least **5 independent same-exposure programme/study clusters** containing both cohorts. Time-since-fragmentation interaction requires the moderator gate above.

## 8. Recovery priorities

Existing closed clusters may be reopened only for coverage goals defined in the machine-readable recovery registry. Priority is determined from:

1. number of prespecified layer pairs potentially unlocked;
2. whether the candidate fills an underrepresented pair;
3. whether it contributes an independently defined moderator contrast;
4. whether the missing source object is finite and recoverable;
5. independent-unit validity.

Reported effect direction or significance is excluded from priority scoring.

Structural one-landscape/one-reference failures remain closed unless genuinely new independent fragmentation units become available; lower-level observations cannot repair that design.

## 9. Search and extraction stop rules

The expansion phase stops candidate discovery when all of the following are true:

1. every primary study from the frozen seed-synthesis universe has a screening decision;
2. forward/backward citation expansion through 2026-09-18 has a logged screening decision;
3. every high-priority recoverable existing cluster has either been admitted or has a documented terminal blocker;
4. no unresolved duplicate/programme linkage remains.

The search **does not stop early because a target p-value is achieved**, and it **does not continue because a target p-value is missed**.

After the candidate universe is frozen, effect extraction proceeds for all eligible candidates regardless of expected direction.

## 10. Supersession gate for the current Journal of Ecology baseline

The current five-cluster manuscript remains submission-valid and frozen during this development phase.

The expanded manuscript supersedes the baseline only if, before manuscript rewriting:

- the complete candidate-universe ledger is frozen;
- at least one primary pair-specific family reaches the quantitative gate;
- the expanded estimand can be reported as effect magnitude + uncertainty rather than only a Fisher/global-null test;
- no admission decision depends on effect direction/significance;
- all newly admitted clusters pass the existing independent-unit and dependence checks.

If these conditions are not met, the baseline manuscript remains the submission version and the expansion is reported as an incomplete development programme rather than used to delay or distort the existing result.

## 11. Claim ceiling

The expanded meta-analysis may estimate layer-specific average responses, repeated same-system layer contrasts and adequately supported moderator associations.

It may not claim:

- direct validation of the finite NEE operators;
- causal mediation from observational cross-study associations;
- a universal ordering of all layers;
- prevalence of separated systems unless the final search universe supports that estimand;
- that nonsignificant layer differences prove exchangeability;
- that missing/inaccessible layers are biological zeros;
- that added systems “rescue” or “repair” the original Serapias-dependent Fisher result.

