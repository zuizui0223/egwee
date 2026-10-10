# Interaction–function sign geometry audit — 2026-09-29

## Why this audit

The effect-scale audit showed that relative response magnitude is not invariant to the choice between Hedges g and lnRR. A more scale-stable ecological question is therefore:

> **Do interaction quantity and reproductive function move in the same or opposite directions under the same registered fragmentation exposure?**

For positive-valued direct endpoints, the sign of the fragmented/reference contrast is unchanged by switching from Hedges g to lnRR. Continuous-gradient programmes retain their registered Fisher-z sign. This makes sign geometry a more defensible cross-representation qualitative property than relative effect magnitude.

## Complete panel census

The registered I–F evidence contains **18 primary panels from 8 independent programmes**.

Panel-level sign geometry:

- concordant deterioration (`I−, F−`): **8 panels**;
- concordant improvement (`I+, F+`): **4 panels**;
- interaction loss with function retained/improved (`I−, F+`): **4 panels**;
- interaction retained/improved with function loss (`I+, F−`): **2 panels**.

Thus **6/18 primary panels have opposite I/F signs**.

These six sign-discordant panels occur in **5 independent programmes**:

- Sevenello edge–core annuals;
- Kakamega multi-species fragmentation programme;
- *Eucalyptus wandoo*;
- Zurich BetterBlooms phytometers;
- Toronto common milkweed.

This count is descriptive. Programmes have unequal numbers of dependent species/panels, so `5/8` is not treated as a prevalence estimate or binomial test.

## Both directions of qualitative decoupling occur

### Interaction retained/increased while reproductive function declines

Two independent programmes contain the strongest form of hidden reproductive failure:

- *Eucalyptus wandoo*: pollen-tube quantity increases with fragmentation severity while seed production declines;
- Kakamega *Acanthopale pubescens*: standardized visitation occurrence is higher in fragments while natural fruit set is lower.

These are qualitative sign reversals, not merely differences in standardized magnitude.

### Interaction declines while reproductive function is retained/increased

Three independent programmes contain the opposite geometry:

- Sevenello: LARO and POAR have lower bee abundance at edges but positive point responses in viable-seed production;
- Zurich: *Onobrychis viciifolia* has lower all-pollinator capture rate with urbanization but positive fruit-set response;
- Toronto milkweed: pollinator abundance declines toward the urban centre while mean follicles per inflorescence shows a positive point response.

These patterns are consistent with reproductive buffering, alternative pollination routes, resource reallocation or other compensatory processes, but the present data do not identify a common mechanism.

## The more surprising result: the same landscape can produce different sign geometries among species

Four programmes contain multiple primary species/panels under one registered landscape/exposure frame:

1. Chaco (three species);
2. Sevenello edge–core (three primary species);
3. Kakamega fragmentation programme (four primary panels);
4. Zurich urban gardens (four phytometers).

Three of those four programmes show **within-programme qualitative heterogeneity**:

- Sevenello: GORO is `I+, F+`, whereas LARO and POAR are `I−, F+`;
- Kakamega: *Acanthopale* is `I+, F−`, whereas the *Acanthus* and *Heinsenia* panels are `I+, F+`;
- Zurich: *Onobrychis* is `I−, F+`, whereas the other three phytometers are `I−, F−`.

Only Chaco is qualitatively uniform, with all three species `I−, F−`.

This means that landscape exposure alone is not sufficient to determine the interaction→function trajectory. **Plant identity and its mating/pollination/resource biology can change the sign of the functional response even within the same landscape experiment or programme.**

## General ecological statement

The strongest scale-stable ecological result from the broader I–F evidence is:

> **Interaction quantity is not a monotonic proxy for reproductive function under fragmentation and land-use change. The same landscape exposure can produce hidden reproductive failure, apparent functional buffering, concordant deterioration or concordant improvement depending on the focal plant.**

This is stronger than saying merely that fragmentation effects are context dependent, because qualitative response geometry can differ among focal species sharing the same exposure frame.

## Relation to previous synthesis

Global meta-analyses show negative mean land-use effects on both pollination and female fitness and a positive cross-species association between their effect sizes. That establishes average coupling at broad scale.

The present matched-programme sign audit asks a different question: whether pollination/interaction quantity and reproductive function necessarily move in the same direction **within the same landscape exposure**. They do not.

Methods literature has also warned that visitation is a poor proxy for pollination effectiveness. The present result extends that concern one step further: even measured interaction/pollen quantity can fail to predict the sign of reproductive-function response under landscape change.

## External qualitative support

Hulting et al. (2025) provides an independent replicated five-species fragmentation experiment that could not enter the quantitative effect-size synthesis because model coefficients/SE or hierarchy-preserving raw effects were not reconstructable. Published results report no detected edge/connectivity effect on pollination rate, while seed production increased with distance from edge for four of five species.

This source is retained as qualitative external support only; non-significance is not coded as zero and it does not increase the quantitative programme denominator.

## Claim ceiling

Allowed:

- opposite-sign I/F responses occur in both directions across independent programmes;
- five independent programmes contain at least one primary sign-discordant I/F panel;
- three independent multi-panel programmes show different sign geometries among focal species under the same registered exposure frame;
- interaction quantity is not a universally monotonic proxy for reproductive function;
- these sign properties are more effect-scale robust than g-versus-lnRR magnitude ordering.

Not allowed:

- 5/8 is a global prevalence estimate;
- sign-discordant panels are statistically independent observations;
- one compensatory mechanism explains all `I−,F+` cases;
- one pollen-quality mechanism explains all `I+,F−` cases;
- unresolved magnitude contrasts prove biological equality;
- the Hulting non-significant pollination result equals a true zero effect.

## Machine-readable implementation

- `evidence/meta_extraction/if_sign_geometry_census_v1.csv`
- `scripts/check_if_sign_geometry.py`
