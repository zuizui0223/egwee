# SUPERSEDED DRAFT — historical Phase-2 design only

> Prospective decisions after 2026-09-18 are governed by `manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-18_SYSTEMATIC_COVERAGE_MODERATORS.md` and `manuscript/meta_analysis_phase2_contract.json`. Do not use thresholds or search cutoffs in this draft as active gates.

# Protocol amendment — systematic coverage and moderator expansion

**Frozen development date:** 2026-09-17  
**Parent protocol:** `META_ANALYSIS_PROTOCOL_2026-09-11.md`  
**Status:** prospective coverage/moderator expansion; no new outcomes opened under this amendment at freeze

## 1. Why this amendment exists

The first executable multilayer synthesis closed with five independent direct Hedges-g programme/study clusters and 17 marginal effects. Its canonical global Fisher result is `p=0.01212432`, but the result is materially dependent on ML001 *Serapias* (`omit ML001 p=0.18194353`). A zero-covariance sensitivity gives `p=0.03860161`, whereas the covariance-free Cauchy–Schwarz certification bound gives `p=0.28061178`.

Those results remain frozen as the current Journal of Ecology baseline. They do not justify searching for a sixth direct cluster merely to restore leave-one-cluster-out significance. The current amendment opens a different scientific phase: systematic coverage and moderator recovery for the layer-contrast and process-coupling analyses already preregistered on 2026-09-11 but not estimable from the first recovered corpus.

This amendment therefore changes the **coverage objective**, not the existing result.

## 2. Frozen baseline that this phase may not rewrite

The baseline direct family remains:

- `ML001` *Serapias lingua*;
- `ML002` *Brosimum alicastrum*;
- `ML003` *Spondias purpurea*;
- `ML014` *Eucalyptus socialis*;
- `ML020` Aizen–Feinsinger Chaco programme.

Frozen numerical state:

- independent direct clusters: `5`;
- primary marginal Hedges-g effects: `17`;
- canonical Fisher `p=0.01212432`;
- omit-ML001 `p=0.18194353`;
- zero-covariance full Fisher `p=0.03860161`;
- covariance-free certification bound `p=0.28061178`.

`ML015` *Eucalyptus wandoo* remains a separate Fisher-z gradient/generalisation cluster and is never pooled into the direct Hedges-g Fisher denominator.

No later coverage result may be back-projected into this baseline as though it had been part of the original terminal robustness test.

## 3. New target population and search universe

The expansion targets flowering-plant fragmentation studies contributing one or more predeclared response layers, with special priority to systems that can identify within-system layer contrasts.

The declared candidate universe is generated from the six prior synthesis domains already frozen in `meta_analysis_seed_sources.md`:

1. pollination and reproductive success under fragmentation;
2. adult plant genetic consequences of fragmentation;
3. progeny genetic and biological quality under fragmentation;
4. fine-scale spatial genetic structure under fragmentation/degradation;
5. updated land-use/fragmentation effects on pollination and male/female fitness;
6. insect-pollinator abundance/richness responses to fragmentation.

For every seed synthesis, recover the full feasible primary-study list or study-level dataset before using outcome direction to decide which studies receive detailed extraction. DOI, title, species, system, campaign and source-observation identifiers are normalized and deduplicated across domains.

Repository-curated systems remain search seeds only. Their prior prominence, outcome direction or mechanistic appeal does not guarantee admission.

**Search cutoff:** 2026-09-17. Studies published after this date require a later dated amendment.

## 4. Search-completion stopping rule

The expansion stops when the declared search universe has been processed to a terminal state, not when a statistical threshold is crossed.

Every candidate must end in one of:

- `admitted_effect`;
- `admitted_multilayer_cluster`;
- `admitted_gradient_generalisation`;
- `closed_recoverability`;
- `closed_structural`;
- `awaiting_author_data`.

The following are explicitly forbidden stopping/continuation triggers:

- restoring leave-one-cluster-out significance;
- reducing the global Fisher p-value;
- replacing a null or concordant cluster after outcome inspection;
- continuing search because a moderator coefficient is non-significant;
- stopping early because a moderator coefficient becomes significant.

If the declared universe is exhausted and an estimand remains underidentified, the result is `not_estimable_at_frozen_information_threshold`.

## 5. Evidence streams remain separate

### 5.1 Direct Hedges-g family

The primary direct estimand remains fragmented minus reference conditions, standardized using source-supported independent fragmentation units. Nested plants, flowers, fruits, progeny, repeated measurements or loci cannot be promoted to fragmentation replicates.

### 5.2 Continuous-gradient family

Fisher-z effects remain a separate generalisation family. No Hedges-g/Fisher-z conversion is introduced by this amendment.

### 5.3 Single-layer studies

Single-layer studies may contribute to layer-specific average fragmentation effects, sampling-variance estimation and moderator precision. They do **not** by themselves identify cross-layer state separation.

### 5.4 Multilayer studies

Same-system studies with two or more eligible layers are the primary identification set for response geometry. Cross-layer conclusions must be anchored in within-system contrasts or multilevel estimands whose layer differences are actually informed by multilayer systems.

## 6. Restored preregistered estimands

The expansion implements, rather than replaces, the primary tests frozen on 2026-09-11.

### 6.1 Response-layer model

Fit the predeclared multilevel model family beginning with:

`g_oriented ~ 0 + layer`

with the frozen study/species/system dependence rules and reconstructed sampling covariance where available. Cluster-robust variance is used when within-study sampling covariance cannot be fully reconstructed and the required conditions are met.

Layer-specific grand means describe average fragmentation response by biological layer. They are not alone interpreted as state separation when they are identified only across different study compositions.

### 6.2 Primary within-system layer contrasts

Priority contrasts remain:

- `I - F`;
- `C - F`;
- `G_adult - G_offspring`;
- `G_adult - mean(I,F)` when jointly estimable.

The corresponding effect for a direct pair is the difference of oriented standardized effects under the same study/system exposure, with sampling variance including within-system covariance when recoverable.

### 6.3 Process-function coupling

For systems measuring both process and function, estimate:

- `C` with `F` coupling;
- `I` with `F` coupling.

Because both axes contain sampling error, a multivariate/measurement-error representation is preferred when feasible. A cluster-robust meta-regression may be used as a sensitivity analysis when the exact joint sampling model is unavailable.

The observational association is not causal mediation.

## 7. Moderator hypotheses retained from the parent protocol

Priority moderators are:

1. self-incompatible / self-compatible / mixed / unknown mating or compatibility system;
2. autonomous reproductive assurance, only when independently and explicitly measured;
3. pollination vector: invertebrate / vertebrate / abiotic / mixed / unknown;
4. life form;
5. longevity class;
6. adult versus offspring/juvenile cohort;
7. time since fragmentation;
8. fragmentation component: area / isolation-connectivity / composite;
9. direct process measurement versus proxy.

Biome and region remain secondary moderators.

A moderator must be defined independently of the outcome used as the response. In particular, `compensated` may not be defined from observed reproductive success and then used to explain reproductive success.

## 8. Moderator opening gates

These gates prevent outcome-driven overfitting. They are not claims that the resulting models are automatically well powered.

### Pair-specific categorical moderator

Open only if:

- at least `10` independent informative systems contribute to the relevant layer-pair estimand; and
- every category retained in the comparison contains at least `4` independent systems.

### Pair-specific continuous moderator

Open only if at least `10` independent informative systems have non-missing moderator values for the relevant layer-pair estimand.

### Multivariable moderator model

Do not open until at least `20` independent multilayer systems contribute to the relevant estimand.

Moderators are first fitted one at a time. Category collapsing after viewing response effects is forbidden. If a gate is not met, retain the moderator descriptively and report `not_estimable_at_frozen_information_threshold`.

## 9. Coverage priorities

Coverage is prioritized by missing information geometry rather than by favorable effect direction.

Current highest-priority cells are:

1. `I-F`;
2. `G_adult-G_offspring`;
3. `C-F`;
4. `G_adult-mean(I,F)`.

The existing registered recovery queue is reopened only where the documented blocker can genuinely change. Priority order and blocker-specific reopening requirements are frozen in `evidence/meta_extraction/coverage_expansion_recovery_priority_v1.csv`.

### Structural hard stops

`ML009` and `ML013` remain structurally non-identifiable for the direct fragmentation estimand unless genuinely new independent landscape/reference replication appears. Additional mothers, progeny, loci or within-landscape observations cannot satisfy this requirement.

## 10. Reopening rule for previously closed candidates

A closed candidate may be reopened only when at least one of the following changes:

- public raw or supplementary data become accessible;
- an author supplies the missing source-defined table/data;
- a previously unavailable same-frame effect estimate and uncertainty become recoverable;
- genuinely new independent fragmentation-level replication is published.

The following do **not** justify reopening:

- favorable published wording;
- a large descriptive difference;
- a need for more clusters after an adverse sensitivity result;
- the possibility that a candidate could change a p-value.

## 11. Expansion outputs

If coverage is adequate, the expanded paper may estimate:

- layer-specific mean fragmentation responses;
- within-system layer differences;
- distributions of concordant versus decoupled response geometry, subject to a defensible systematic denominator;
- cohort/history-lag associations;
- process-function coupling;
- preregistered moderator associations.

If coverage is inadequate, the paper reports the corresponding estimand as not estimable rather than weakening admission, dependence or moderator gates.

## 12. Relationship to NEE

This empirical expansion does not validate the finite NEE operators.

EGWEE owns natural-system estimates of fragmentation response geometry, cohort lag, process-function coupling and moderator associations. NEE owns the constructive representation result and finite sorting, buffering, recoupling, density-gate and reserve mechanisms.

Any similarity between an EGWEE moderator pattern and an NEE operator is an interpretation/hypothesis unless independently tested in a design capable of causal identification.

## 13. Manuscript firewall during expansion

The current Journal of Ecology manuscript and its five-cluster numerical result remain unchanged while the new search universe is incomplete. Expansion results may enter a revised manuscript only after:

1. the declared six-domain search universe reaches terminal screening states;
2. the expansion contract checker passes;
3. the expanded effect/dependence dataset is frozen;
4. the relevant analysis-opening gates are evaluated without relaxing them after outcome inspection.

Until then, the current manuscript is a reproducible frozen baseline rather than a rolling-analysis document.