# SUPERSEDED DRAFT — historical Phase-2 design only

> Prospective decisions after 2026-09-18 are governed by `manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-18_SYSTEMATIC_COVERAGE_MODERATORS.md` and `manuscript/meta_analysis_phase2_contract.json`. Do not use thresholds or search cutoffs in this draft as active gates.

# Protocol amendment — systematic coverage and moderator expansion

**Date frozen:** 2026-09-17

**Parent protocol:** `META_ANALYSIS_PROTOCOL_2026-09-11.md`

**Frozen scientific base:** `16308cf6d6e4aec274504ba81bbf6e71be465099`

## Purpose

The completed five-cluster state-separation synthesis is retained exactly as reported at the frozen scientific base. This amendment does **not** reopen the corpus to repair significance, strengthen the existing Fisher test, or search for a sixth cluster because the leave-one-ML001 result is non-significant.

The purpose of Phase 2 is different: to recover a reproducible sampling frame broad enough to estimate **which biological response geometries occur under plant fragmentation, which layer pairs diverge, and which independently coded biological conditions are associated with that divergence**.

The original 2026-09-11 protocol already predeclared multilevel layer effects, `I-F`, `C-F`, `G_adult-G_offspring`, cohort/history lag, process-function coupling, and moderators including mating system, reproductive assurance, pollination vector, life history, fragmentation age and fragmentation component. The five-cluster paper did not estimate most of those quantities because the recovered same-frame corpus was too small. Phase 2 therefore resumes the unfulfilled coverage/moderator programme rather than inventing a new hypothesis after inspecting the five-cluster result.

## Frozen Phase-1 boundary

The following Phase-1 quantities are immutable reference results and are never optimization targets for Phase 2 search:

- five independent direct programme/study clusters;
- 17 direct Hedges-g marginal effects;
- canonical paired-dependence Fisher `p=0.01212432`;
- omit-ML001 Fisher `p=0.18194353`;
- zero-covariance Fisher `p=0.03860161`;
- covariance-free Cauchy-Schwarz certification bound `p=0.28061178`;
- ML015 retained as a separate Fisher-z gradient-generalisation family.

No Phase-2 inclusion decision may depend on whether adding a record decreases any of these p-values. Phase 1 remains citable even if Phase 2 later yields a different or weaker scientific conclusion.

## Phase-2 target estimands

### Primary estimand A — paired within-system layer differences

For every eligible study/programme cluster with at least two layers represented on a common direct fragmentation contrast, retain the marginal effects and sampling covariance and define

`Delta_s,ab = g_s,a - g_s,b`

with

`V(Delta_s,ab) = V_s,a + V_s,b - 2 Cov_s,ab`.

The primary layer-pair families are inherited from the original protocol:

1. `I - F`;
2. `C - F`;
3. `G_adult - G_offspring`;
4. `G_adult - mean(I,F)` where I and F are jointly estimable on the same frame.

These contrasts, rather than cluster p-values, are the principal Phase-2 meta-analytic effect sizes. Pair direction is fixed by the order above and is not reversed after outcome inspection.

### Primary estimand B — layer-specific fragmentation response

If the systematic frame supplies sufficient single-layer as well as multilayer studies, fit the predeclared multilevel model family `g_oriented ~ 0 + layer` with study/programme/species dependence. This estimates layer-specific mean standardized response and is secondary to paired within-system contrasts for causal interpretation because between-study differences can confound layer comparisons.

### Primary estimand C — response geometry

A study/programme may show concordant deterioration, layer separation, buffering, or mixed geometry. Phase 2 does not classify geometry from significance alone. Geometry summaries are derived from the signed paired contrasts and their uncertainty; a non-significant pair is not coded as biological equality.

## Systematic sampling frame

The legacy 20-candidate ledger remains provenance only and is not the Phase-2 sampling universe.

Phase 2 constructs the candidate universe outcome-blind from the predefined source frames in `meta_analysis_coverage_frame_v2.csv`:

- major plant pollination/reproduction fragmentation syntheses;
- plant adult-genetic fragmentation syntheses;
- progeny genetic/performance fragmentation syntheses;
- plant fine-scale genetic-structure fragmentation syntheses;
- the updated land-use/pollination/fitness synthesis;
- the recent global pollinator fragmentation synthesis as a discovery index for plant-pollinator fragmentation studies;
- backward/forward citation expansion through 2026-09-17 from records identified in those frames.

A primary publication appearing in more than one source frame is one bibliographic record. Species, campaign, contrast and programme dependence are resolved after deduplication.

### Outcome-blind screening rule

Candidate discovery and first-pass multilayer tagging may use title, abstract, methods, supplementary metadata and variable names. Numeric effect direction, p-values and the magnitude of layer differences must not determine whether a record enters the screening queue.

A record can be excluded before quantitative opening for exposure mismatch, non-plant target, absence of a fragmentation contrast, no eligible layer, duplicate observations, impossible independent-unit recovery, or source inaccessibility. Those reasons are logged regardless of expected direction.

## Recovery priority

Existing closed attempts are reprioritized in `meta_analysis_recovery_priority_v2.csv` solely by information gain for underrepresented layer pairs and by whether the blocker is potentially recoverable.

Priority does **not** mean expected support for state separation. In particular, a candidate expected to show concordant deterioration is equally valuable if it fills a sparse layer pair.

Structural one-landscape/one-reference failures remain closed unless genuinely new independent fragmentation units become available; lower-level plants, mothers, offspring, loci or flowers may never be promoted to repair that design.

## Moderator hypotheses

Moderator coding is fixed in `meta_analysis_moderator_schema_v1.csv` before new Phase-2 numeric outcomes are opened.

### H2a — cohort/history lag

Recent fragmentation and long-lived life histories should permit stronger discordance between contemporary process/function layers and `G_adult`, because standing adults can retain pre-fragmentation genetic state. The direct paired target is `G_adult - G_offspring`; secondary contrasts compare `G_adult` with contemporary I/C/F when measured on the same system frame.

### H2b — reproductive assurance

Autonomous reproductive assurance or self-compatibility can buffer F relative to interaction loss. Therefore I-F separation may be larger when independently documented reproductive assurance is available. Mating system and reproductive assurance are coded from source biology, not inferred from the observed F effect.

### H2c — movement / pollination context

Pollination vector and direct-versus-proxy process measurement may modify I-F and C-F coupling. This is an association/moderator hypothesis, not a claim that pollinator guild is itself a mechanistic state.

### H2d — fragmentation history

Time since fragmentation and fragmentation component (area, isolation/connectivity, edge, composite) may alter the response geometry. Time since fragmentation is used only when source-explicit or defensibly dated; no midpoint is imputed from vague historical language.

## Model-opening gates

Moderator analyses are deliberately fail-closed.

- A univariable moderator coefficient is not fitted unless at least 10 independent programme/study clusters contribute the relevant estimand.
- A categorical moderator level must have at least 4 independent clusters; otherwise it remains descriptive or is combined only by a predeclared biological collapsing rule.
- A continuous moderator requires at least 10 independent clusters and non-degenerate support across the observed range.
- A multivariable moderator model is not opened unless there are at least 20 independent clusters and at least 10 clusters per fitted moderator degree of freedom.
- Phylogenetic random effects remain sensitivity analyses and are not opened unless species coverage is sufficient to construct a reproducible tree without outcome-based taxon filtering.

Failure to meet a gate is a result about information limits, not a reason to relax the gate.

## Dependence and synthesis

The independent denominator remains the programme/study fragmentation cluster. Repeated endpoints, species sharing the same landscapes, years sharing biological units, progeny stages and loci do not become independent studies.

Where sampling covariance is reconstructable, retain the multivariate variance matrix. Otherwise use the frozen cluster-robust fallback specified in the parent protocol. Phase 2 may not choose a covariance method based on which version produces stronger separation.

Direct Hedges-g and continuous Fisher-z streams remain separate. Gradient studies may contribute to a parallel generalisation analysis but are never converted to direct effects merely to increase the direct denominator.

## Search completion and stop rule

Phase 2 search stops when all predefined source frames have been materialised to their primary-study lists, deduplicated, screened under the frozen criteria, and the predefined backward/forward citation expansion has been completed through 2026-09-17.

The search does not stop when a p-value crosses 0.05, and it does not continue merely because a p-value fails to cross 0.05.

Any later expansion requires a dated amendment that names a coverage, taxonomic, geographic or moderator purpose **before** numeric outcomes from the new source frame are opened.

## Promotion rule for the Journal of Ecology manuscript

The current submission-ready five-cluster manuscript remains the frozen fallback publication state.

Phase 2 replaces the submission version only if the systematic frame is completed and at least one of the following outcome-independent information conditions is met:

1. at least two of the predeclared primary layer-pair families contain 5 or more independent programme/study clusters each; or
2. at least one moderator analysis reaches its frozen model-opening gate; or
3. the systematic frame materially changes the study-flow denominator such that a targeted-recovery description is no longer an accurate account of the evidence universe.

Promotion never depends on obtaining a smaller combined p-value than Phase 1.

## No-rescue rules

Do not:

- search for a sixth direct cluster solely to repair omit-ML001 significance;
- retain only new studies that strengthen state separation;
- exclude concordant or null clusters after effect inspection;
- code missing layers or non-significant outcomes as zero;
- define `compensated`, `buffered` or another moderator from the same outcome it is later used to explain;
- pool direct Hedges-g and Fisher-z effects into one mean;
- promote nested biological units to fragmentation replicates;
- relax moderator cell-size gates after seeing estimates;
- choose covariance assumptions, endpoint variants or moderator codings because they produce smaller p-values;
- reinterpret the systematic expansion as validation of NEE finite operators.
