# Ecological fragmentation-response regimes — 2026-09-27
## Status after the 2026-09-29 estimand-scale audit

This document is retained as **registered-scale exploratory provenance**. It is not a current scale-invariant manuscript claim.

The authoritative effect-scale interpretation is in `manuscript/ESTIMAND_SCALE_ROBUSTNESS_2026-09-29.md` and `manuscript/BOTTLENECK_SCALE_ROBUSTNESS_2026-09-29.md`. Hedges-g and lnRR give different system-specific magnitude/separation classifications. Any bottleneck, ordering or direction-census statement below must therefore be read as conditional on its declared effect representation.


## Purpose

This note translates the current EGWEE evidence into ecological response regimes without changing any
effect estimate, analysis family, admission decision or preregistered gate.

The organising question is ecological:

> When habitat fragmentation changes pollination, movement, reproduction and genetic responses,
> which processes remain coupled and which become decoupled?

This is not a new pooled meta-analysis. Direct Hedges-g contrasts and continuous Fisher-z gradients
remain in their registered effect families.

## Regime 1 — coupled interaction and reproductive decline

### Aizen–Feinsinger Chaco programme (ML020)

Across all three retained species, small fragments had lower pollen-tube support and lower fruit set:

| species | I effect | F effect | interpretation |
|---|---:|---:|---|
| *Atamisquea emarginata* | -0.713 | -1.005 | both decline |
| *Cercidium australe* | -0.637 | -1.139 | both decline |
| *Prosopis nigra* | -0.481 | -1.135 | both decline |

The three dependent species are reduced to one programme-level internal gate. The programme-level
Bonferroni p-value is **1.0**, so the data do not resolve an I–F magnitude difference.

Ecological reading: fragmentation can propagate through pollination and reproduction as a broadly
coupled deterioration pathway.

## Regime 2 — interaction quantity persists while reproductive function falls

Three independent natural programmes show the same qualitative motif on their own registered effect
scales.

### *Eucalyptus wandoo* fragmentation gradient

- interaction / pollen tubes: Fisher z = **+0.690**
- reproductive function / seeds per fruit: Fisher z = **-0.876**
- I − F difference = **+1.566**
- p = **0.0008565**

Pollen quantity increased along the composite fragmentation gradient while seed production declined.

### *Cardiopetalum calophyllum* fragment-area gradient

- pollinator abundance per flower: Fisher z = **-0.245**
- fruit set: Fisher z = **-1.684**
- I − F difference = **+1.439**
- 95% CI = **[+0.483, +2.394]**
- p = **0.00316**

Measured beetle-pollinator abundance changed weakly while reproductive function declined strongly
toward smaller fragments.

### Kakamega *Acanthopale pubescens*

- standardized pollinator occurrence: Hedges g = **+0.349**
- natural fruit set: Hedges g = **-2.848**
- I − F difference = **+3.197**
- 95% CI = **[+1.208, +5.186]**
- p = **0.00163**

Pollinator occurrence was maintained/slightly elevated at fragment sites while fruit set was sharply
lower.

These three programmes cannot be numerically pooled because they belong to different registered
effect families and were not selected prospectively as one confirmatory set. Their repeated
qualitative geometry is therefore a **descriptive ecological motif**, not a universal law.

The motif suggests that pollinator abundance, visitation occurrence or pollen quantity can be a poor
proxy for realised reproductive function after fragmentation. Candidate mechanisms include pollen
quality, compatible-mate limitation, self/heterospecific pollen, mating structure, resource
limitation and other post-visitation filters. The present analyses do not identify those mechanisms
causally.

## Regime 3 — weak or unresolved interaction–function separation

### Sevenello edge–core experiment

The three primary species panels show no resolved I–F separation:

- GORO: I − F = **+0.020**, p = **0.982**
- LARO: I − F = **-0.460**, p = **0.392**
- POAR: I − F = **-0.405**, p = **0.506**

Programme-level Bonferroni p = **1.0**.

This provides an important counterweight to the strong decoupling examples: edge exposure does not
automatically create a measurable mismatch between bee abundance and seed production.

## Within-region heterogeneity

The Kakamega programme shows that response geometry can vary even among species and campaigns in one
regional fragmentation setting.

*Acanthopale* shows strong interaction–function decoupling, whereas the two *Acanthus* campaigns and
*Heinsenia* show positive fragment-site responses in both I and F with wide I–F intervals crossing
zero.

Thus the ecological unit of explanation may need to include plant life history, mating biology,
pollinator identity and year/campaign context rather than treating “fragmentation” as a sufficient
mechanistic label.

## Genetic response timing

The present evidence does not support a general adult-versus-offspring lag.

In *Spondias purpurea*, adult H_O is lower in fragmented sites (g = **-0.941**), juvenile H_O is more
negative (g = **-3.181**) and seed H_O is **-1.118**, but the covariance-aware adult–offspring
contrasts are too imprecise for a system-level directional lag claim.

Across the preregistered five-programme G_adult–G_offspring family, the mean adult-minus-offspring
response contrast is approximately **+0.129** and does not resolve a common directional cohort lag.

The ecological implication is therefore a hypothesis, not a conclusion: standing adult genetic
diversity can potentially retain landscape history longer than contemporary interaction or
reproductive processes, but EGWEE does not yet establish a general lag across systems.

## Current ecological synthesis

The strongest ecology-first interpretation is:

1. habitat fragmentation can produce both **coupled** and **decoupled** biological responses;
2. a recurring natural motif is **interaction quantity without reproductive-function retention**;
3. that motif is not universal, and response geometry can differ among species in the same region;
4. no single pollination, reproduction or genetic metric should currently be assumed to proxy the
   whole fragmented-system response;
5. the next testable ecological problem is to identify which mating systems, pollination modes,
   life histories, fragmentation histories and demographic contexts predict each regime.

## Boundary

This note introduces no new significance test and does not alter Phase 1 or Phase 2 gates. It is an
ecological interpretation of already locked results.

It does not validate or falsify any finite EGWE/NEE operator.
