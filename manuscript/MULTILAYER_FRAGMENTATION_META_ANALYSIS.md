# Fragmentation does not act as a single biological state: a multilevel meta-analysis of plant interaction, movement, reproduction and genetic responses

**Status:** active protocol-first manuscript spine. Quantitative results are not yet claimed; study screening and effect-size extraction must follow the locked protocol in `META_ANALYSIS_PROTOCOL_2026-09-11.md`.

## Central empirical question

The companion NEE theory paper asks first whether fragmentation produces one biological deterioration state and, second, which cross-layer organization and life-cycle processes determine divergent futures. This paper asks the natural-data counterpart:

> **Across fragmented flowering-plant systems, do demographic/resource support, pollinator interaction, movement/gene flow, reproductive function and genetic state respond as one common deterioration axis, or do their effect sizes systematically diverge within the same study systems?**

A second question asks whether that divergence is structured by biological process rather than being unstructured noise:

> **Are cross-layer differences associated with mating system, pollination vector, movement/connectivity response, cohort identity and time since fragmentation?**

## Primary hypotheses

### H1 — biological layers do not share one fragmentation response

After orienting all effects so that negative values mean loss of functional support under greater fragmentation, the mean effect is allowed to differ among response layers:

- `D`: demographic/resource support;
- `I`: realised pollinator interaction / pollen receipt;
- `C`: process-specific movement, pollen flow or mating connectivity;
- `F`: reproductive function / fitness;
- `G_adult`: standing adult genetic state;
- `G_offspring`: progeny/juvenile genetic or mating state.

The primary test is an omnibus response-layer moderator in a multilevel meta-analysis with study/species clustering. Evidence for H1 requires more than a negative grand mean: layer-specific effects or within-study contrasts must differ beyond sampling uncertainty.

### H2 — contemporary processes can change before standing adult genetics

Where adult and offspring/current-process measurements coexist, contemporary interaction, movement and reproductive effects are predicted to be more negative than standing adult neutral-genetic effects after recent fragmentation. Offspring/juvenile genetic responses are predicted to track contemporary mating/function more closely than adult standing diversity.

This is the empirical cohort/history-lag prediction motivated by *Conospermum* and *Spondias*; it is not assumed a priori to hold in every taxon.

### H3 — process compensation modifies the function response

Among systems measuring both process and function, a less-negative or positive fragmentation effect on movement/connectivity is predicted to be associated with a less-negative effect on reproductive function. The analogous interaction-function association is also tested.

This is an associational meta-regression, not proof that movement causally rescued function. Miyake-jima *Camellia–Zosterops* is a mechanistic anchor for the compensation configuration; *Crepis sancta* is an anchor for uncompensated interaction limitation.

## Why this is not a repeat of existing meta-analyses

Existing syntheses have established average fragmentation or land-use effects separately for pollination/reproduction, plant genetic diversity, progeny quality, fine-scale genetic structure and pollinator abundance/richness. The present target is different: **link effects across biological layers within the same studies/species, then quantify concordance, lag and process-conditioned discordance.**

The paper therefore does not compete on a new grand mean of fragmentation. Its novelty is the multivariate question: whether published natural systems behave as a single deterioration axis once multiple biological layers are measured together.

## Study universe

Screening uses two complementary sources:

1. reference lists and deposited datasets from major prior meta-analyses of plant pollination/reproduction, plant genetics/progeny responses and pollinator responses to fragmentation or land-use change;
2. forward searches through 11 September 2026 plus the natural systems already audited in this repository.

The prior EGWEE systems are **seed systems, not the complete sample**. In particular, *Crepis*, Miyake *Camellia–Zosterops*, *Conospermum* and *Spondias* remain pre-specified mechanistic anchors, while Honshu–Izu, Zurich, Toronto, *Oenothera*, *Eschscholzia*, Mallorca carob and *Campanula americana* contribute only if their original studies satisfy the meta-analysis exposure and effect-size criteria.

## Effect-size strategy

The primary synthesis is restricted to direct fragmented-versus-reference contrasts that can be represented as Hedges' `g` (or reconstructed from means/SD/sample sizes or equivalent test statistics). Signs are harmonised so that negative values always indicate lower support/function under fragmentation. Variables whose raw increase indicates deterioration (for example inbreeding or genetic differentiation) are sign-reversed only after the raw effect and coding rule are preserved.

Continuous-gradient effects that cannot be mapped to the primary group contrast without strong assumptions are analysed in a separate Fisher-`z(r)` stream. They are not silently mixed with Hedges' `g`.

Multiple effects from one study/species are retained and modelled with study/species clustering and robust or explicitly modelled sampling dependence. They are not counted as independent studies.

## Primary model

For effect `j` in study/species cluster `i`,

`y_ij = mu_layer[j] + moderators_ij + u_study[i] + u_species[i] + e_ij`.

The primary inference is the joint test of `mu_layer`, followed by preregistered contrasts:

- interaction vs reproductive function;
- movement/connectivity vs reproductive function;
- adult genetics vs offspring genetics;
- adult genetics vs contemporary interaction/function.

A descriptive within-study discordance statistic may be shown, but the headline inference comes from the multilevel model and paired layer contrasts rather than an unweighted spread score.

## Process moderators

Predeclared moderators are limited to variables that can be coded without using the focal effect-size outcome itself:

- mating system / self-compatibility / autonomous reproductive assurance;
- pollination vector (vertebrate, invertebrate, abiotic where relevant);
- life form / longevity;
- measured cohort (adult vs seed/progeny/juvenile);
- time since fragmentation when reported;
- fragmentation contrast type (area, isolation/connectivity, composite landscape alteration);
- whether movement/connectivity was measured directly rather than inferred from neutral standing diversity.

The measured `C` effect may also enter a paired process–function meta-regression when both `C` and `F` are available in the same system. This is reported as association, not causal mediation.

## Mechanistic anchor systems

Four systems remain useful because they instantiate qualitatively different configurations already documented in the literature:

- *Crepis sancta*: interaction-limited, weakly compensated local fragmentation;
- Miyake-jima *Camellia japonica–Zosterops japonicus*: movement-mediated compensation;
- *Conospermum undulatum*: contemporary process decline with adult-genetic history lag;
- *Spondias purpurea*: near-synchronised interaction, pollen-flow, reproductive and offspring-genetic deterioration.

These examples illustrate the fitted multivariate patterns; they do not substitute for the meta-analytic sample.

## Expected paper-level conclusion if H1–H3 are supported

> **Habitat fragmentation has an overall detrimental effect on flowering-plant systems, but it does not act as one biological deterioration state. Interaction, movement, reproduction and genetic responses differ systematically in magnitude and timing, and part of that discordance is associated with compensatory movement/reproductive routes and cohort history.**

This would provide the empirical counterpart to the NEE state-separation theory without claiming that the finite-model operators are literally validated in nature.

## Claim ceiling

The meta-analysis can test cross-study regularities in response-layer effects and moderators. It cannot establish that the NEE simulator is the true mechanism, that one universal state vector exists, or that an observed movement–function association is causal rescue. Study selection, effect-size reconstruction, non-independence, phylogeny, publication bias and missing-layer patterns must all remain explicit.
