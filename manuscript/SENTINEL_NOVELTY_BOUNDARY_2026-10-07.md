# Novelty boundary: from ecological association to sentinel sufficiency — 2026-10-07

## What is already known

The broad warning that ecological correlation does not guarantee useful surrogacy is not new.

- Heino (2010; Ecological Indicators 10:112–117; doi:10.1016/j.ecolind.2009.04.013) emphasized that even statistically significant cross-taxon correlations can be too weak for reliable biodiversity prediction.
- Hunter et al. (2016; Ecological Indicators 63:121–125; doi:10.1016/j.ecolind.2015.11.049) formalized ecological surrogacy as using one process or element to represent another ecological property.
- Tälle, Ranius & Öckinger (2023; Biological Conservation 288:110384; doi:10.1016/j.biocon.2023.110384) synthesized evidence that surrogate species often have limited conservation utility.
- King et al. (2013) already showed that flower visitation is a poor proxy for pollinator effectiveness.

Therefore EGWEE should not claim to discover that “correlation is not prediction”, that ecological indicators can fail, or that visitation is an imperfect pollination proxy.

## What EGWEE adds

The narrower contribution has four linked parts.

### 1. Same reproductive life cycle, not cross-taxon surrogacy

The putative sentinel and target are mechanistically linked processes within the same plant reproductive life cycle. Pollination contributes to reproduction directly, but final reproductive performance also integrates mating quality, plant condition, post-pollination survival and, in some systems, later mutualisms such as seed dispersal.

This is a stronger intuitive surrogate relationship than using one taxonomic group to represent another. Failure is therefore biologically more informative than generic cross-taxon incongruence.

### 2. A shared disturbance creates real average coupling

Fragmentation is not merely a sampling backdrop.

- all 17 primary direct responses deteriorate on both g and lnRR;
- Aguilar et al. report positive pollination–female-fitness coupling;
- the corrected SF06 fragmentation-only model has beta_pollination=+0.190, p=0.0053.

Thus the indicator is genuinely disturbance-responsive and genuinely associated with the target.

### 3. Yet state translation remains many-to-many

Despite that coupling:

- frozen EGWEE matched programmes contain both false-reassurance and buffering geometries;
- corrected SF06 has 12/54 minimum deterministic sign mismatches;
- source-publication-disjoint SF06 retains 7/31 mismatches;
- mismatch persists after publication/species deletion, dead-zone filtering and marginal sign-confidence filtering.

The result is therefore not simply “weak correlation”.

### 4. Incremental sentinel value can be negligible

In corrected SF06:

- always predicting female-fitness decline makes 12/54 errors;
- the best pollination-sign lookup also makes 12/54 errors;
- the source-disjoint result is 7 versus 7;
- publication-LOO probability prediction is not improved by pollination sign under Laplace or Jeffreys smoothing;
- publication-LOO continuous severity prediction improves MSE only about 2–4% when pollination effect is added.

This directly separates four concepts:

1. disturbance response;
2. association;
3. state-diagnostic sufficiency;
4. transferable predictive value.

## Most defensible general statement

> **A biological process can be a real disturbance response and a statistically significant correlate of downstream function while still being an insufficient stand-alone sentinel of downstream state.**

The novelty is not the statistical truism itself. It is the empirical demonstration within a mechanistically linked reproductive cascade, across matched fragmentation programmes and an independent source-publication-disjoint external paired dataset.

## Why this is ecologically interesting

A simple cascade assumes that monitoring an upstream process summarizes downstream condition.

The combined evidence instead supports a branching pathway:

fragmentation → interaction quantity  
fragmentation → mating provenance / compatibility  
fragmentation → plant condition and post-transfer viability  
fragmentation → compensatory reproductive routes  
fragmentation → later dispersal / recruitment branches  
all → reproductive function.

Because several branches share the same disturbance driver, upstream and downstream effects can remain correlated even when the upstream state is insufficient for downstream diagnosis.

This gives a biological reason—not merely a statistical reason—for the association–sufficiency gap. Source-disjoint external examples show both directions with different mechanisms: *Samanea saman* buffers seed output despite reduced effective pollination but pays downstream progeny-quality costs, whereas *Tristerix corymbosus* retains or improves pollination near edges while overall reproductive success collapses because seed dispersal fails. The same statistical sentinel failure therefore emerges from different branches of the reproductive life cycle.

## Claim ceiling

Do not claim:

- a new general theorem that correlation does not imply prediction;
- universal failure of ecological indicators;
- zero causal importance of pollination;
- operational sensitivity/specificity for field monitoring from the literature sample.

Do claim, if the current robustness stack remains green:

- externally generalized fragmentation-specific interaction→function non-identifiability;
- significant average coupling coexisting with weak incremental sentinel/predictive value;
- recurrent matched-programme false reassurance as the strongest resolved failure mode;
- a branching missing-state mechanism as a prospective biological explanation.
