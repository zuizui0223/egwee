# EGWEE systematic coverage and moderator expansion — design

## Goal

Extend EGWEE from the current five-cluster global exchangeability test into the originally preregistered multilayer meta-analysis of response geometry, without reopening the current result for significance repair and without weakening the pseudo-replication/dependence firewall.

## Frozen baseline

The current Journal of Ecology package remains a frozen baseline analysis:

- five independent direct Hedges-g programme/study clusters (`ML001`, `ML002`, `ML003`, `ML014`, `ML020`);
- 17 marginal effects;
- Fisher `p=0.01212432`;
- omit-ML001 `p=0.18194353`;
- zero-covariance `p=0.03860161`;
- covariance-free certification bound `p=0.28061178`;
- ML015 remains a separate Fisher-z gradient family.

The baseline search-stop remains binding: no sixth direct cluster may be sought merely to restore leave-one-cluster-out significance.

## New scientific target

The expansion asks a different question:

> Which response geometries occur under plant habitat fragmentation, and which independently measured biological conditions are associated with concordant versus decoupled responses across layers?

The expansion therefore targets effect magnitudes and within-system layer contrasts, not a smaller Fisher p-value.

## Search universe

The candidate universe is constructed outcome-blind from the six prior synthesis domains already named in `manuscript/meta_analysis_seed_sources.md`:

1. pollination/reproductive success;
2. adult plant genetic consequences;
3. progeny genetics/performance;
4. fine-scale spatial genetic structure;
5. updated land-use/pollination/fitness synthesis;
6. insect-pollinator fragmentation synthesis.

For each seed synthesis, recover the full primary-study list or study-level data table, normalize DOI/title/species/system identifiers, and deduplicate across domains before opening primary-study outcomes for new extraction. Repository-curated systems are search seeds only and receive no automatic admission.

The expansion search cutoff is 2026-09-17. Future papers after that date require a new dated amendment rather than silent rolling inclusion.

## Evidence streams

### Direct Hedges-g stream

Preserve the existing direct fragmented-versus-reference estimand and effect-unit rules. Every endpoint is oriented so negative values mean lower biological support/function under greater fragmentation.

### Continuous-gradient stream

Preserve Fisher-z as a separate generalisation family. Do not convert effect families solely to increase sample size.

### Single-layer studies

Single-layer studies may contribute to layer-specific average fragmentation effects and moderator precision. They do not, by themselves, identify state separation.

### Multilayer studies

Same-system studies with at least two eligible layers are the primary identification set for cross-layer response geometry. State-separation conclusions must be supported by within-system layer contrasts or models whose cross-layer estimand is identifiable from multilayer systems.

## Primary estimands

The expansion restores the original 2026-09-11 preregistered estimands:

1. multilevel layer model `g_oriented ~ 0 + layer` with study/species/system dependence;
2. `I - F` within-system contrast;
3. `C - F` within-system contrast;
4. `G_adult - G_offspring` within-system contrast;
5. `G_adult - mean(I,F)` when jointly estimable;
6. process-function coupling for `C` with `F` and `I` with `F`, with measurement error/dependence represented where feasible.

The Fisher cluster-combination statistic remains a frozen baseline diagnostic and is not the primary expansion estimand.

## Moderator hypotheses

The original protocol moderators remain authoritative. The expansion records them in a machine-readable contract and makes the opening gates explicit.

Priority moderators:

- mating/self-compatibility system;
- explicitly measured autonomous reproductive assurance;
- pollination vector (`invertebrate`, `vertebrate`, `abiotic`, `mixed`, `unknown`);
- life form and longevity;
- cohort (`adult`, `offspring/juvenile`);
- time since fragmentation;
- fragmentation component (`area`, `isolation/connectivity`, `composite`);
- direct process measurement versus proxy.

Biome/region remains secondary.

A moderator must be defined independently of the response it is used to explain. In particular, a system cannot be labelled `compensated` from observed reproductive success and then use that label to explain reproductive success.

## Moderator opening gates

To reduce overfitting, moderators are opened one at a time.

- Pair-specific categorical moderator: at least 10 independent informative systems for that layer pair, with at least 4 systems in every compared category retained in the model.
- Pair-specific continuous moderator: at least 10 independent informative systems with non-missing moderator values.
- Multivariable moderator model: not opened until at least 20 independent multilayer systems contribute to the relevant estimand.
- If a gate is not met, report `not_estimable_at_frozen_information_threshold`; do not relax the gate after seeing effect directions.

These are analysis-opening thresholds, not claims that 10 or 20 studies guarantees adequate power.

## Coverage targets

Coverage expansion is driven by information geometry, not significance. Priority cells are the preregistered contrasts with the thinnest current independent-system coverage:

1. `I-F`;
2. `G_adult-G_offspring`;
3. `C-F`;
4. `G_adult-mean(I,F)`.

Existing closed candidates may be reopened only when the documented blocker changes (for example public raw data become available, an author supplies the missing table, or a valid same-frame effect representation becomes recoverable). Outcome direction is never a valid reopening reason.

Structural non-identifiability cases `ML009` and `ML013` remain closed unless genuinely new independent landscape/reference replication becomes available; lower-level mothers, progeny or loci cannot repair the design.

## Search and stopping rule

The expansion is complete when all six seed-domain primary-study lists have been recovered to the feasible extent, deduplicated, screened under the frozen eligibility rule, and every eligible candidate has reached a terminal state (`admitted`, `closed_recoverability`, `closed_structural`, or `awaiting_author_data`).

Stopping is therefore based on completion of the declared search universe, not on p-values, confidence intervals, leave-one-out results, or the number of admitted systems.

If the declared universe yields too few informative systems for a contrast or moderator, the result is reported as underidentified/not estimable rather than followed by significance-motivated candidate hunting.

## Claim ownership relative to NEE

EGWEE owns empirical natural-system quantities:

- layer-specific fragmentation effects;
- within-system response geometry;
- frequency/distribution of concordant and separated response patterns only if the systematic universe permits such an estimand;
- cohort/history lag associations;
- process-function coupling;
- moderator associations and their uncertainty.

NEE owns the constructive representation result and finite sorting/buffering/recoupling/failure-gate mechanisms. EGWEE must not describe an observational moderator association as validation of a finite NEE operator.

## Deliverables

The implementation adds:

- a dated coverage/moderator protocol amendment;
- a machine-readable expansion contract;
- an amended effect schema carrying moderator fields without invalidating existing extracted effects;
- a frozen recovery-priority ledger for already registered closed clusters;
- a frozen current pair-coverage snapshot;
- a CI checker that enforces the no-significance-repair firewall, moderator gates, structural closures and frozen baseline values;
- the new files to the existing `Multilayer meta-analysis contract` workflow.

No expansion result is inserted into the Journal of Ecology manuscript until the declared search universe has been screened and the expansion analysis passes its own contract.