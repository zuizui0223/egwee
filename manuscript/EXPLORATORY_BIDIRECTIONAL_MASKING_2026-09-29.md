# Bidirectional masking across fragmented plant reproductive systems — exploratory audit

## Status

**Post hoc / hypothesis-generating.**

This audit was defined after the 2026-09-29 estimand-scale analysis. It does not replace the scale-aware manuscript headline and is not a prevalence test.

## Core observation

The audited systems contain two opposite forms of false reassurance when only one reproductive layer is monitored.

### A. Interaction quantity can look intact while reproductive function deteriorates

All three registered programmes with a resolved I–F mismatch are function-dominant:

- *Eucalyptus wandoo*: pollen-tube response is positive while seed production is negative on the registered fragmentation gradient;
- Kakamega *Acanthopale pubescens*: visitation occurrence is positive while natural fruit set is negative; the downstream classification survives Hedges-g → lnRR re-expression;
- *Cardiopetalum calophyllum*: pollinator abundance changes weakly while fruit set declines much more strongly.

Two of these three programmes therefore show an actual opposite-sign `I+ / F-` response. No resolved I–F programme shows the reverse `I- / F+` polarity.

Point-estimate reverse polarity does occur in unresolved systems (Sevenello LARO/POAR, Zurich *Onobrychis*, common milkweed), so compensation remains plausible but is not resolved in the current registered comparisons.

### B. Reproductive function can look comparatively buffered while mating/connectivity deteriorates

Four independent movement/connectivity or mating-support → F programmes show a larger absolute process response than F on their registered representation:

- *Serapias lingua*;
- *Brosimum alicastrum*;
- *Eucalyptus socialis*;
- *Acer miyabei*.

For the three direct systems, the ordering `|process| > |F|` also survives Hedges-g → lnRR re-expression.

On lnRR, the downstream-to-upstream magnitude ratios are approximately:

- *Serapias*: |F/C| = 0.95;
- *Brosimum*: |F/C| = 0.38;
- *Eucalyptus socialis*: |F/mating| = 0.063.

These ratios are descriptive; they are not pooled and do not define a universal transmission coefficient.

## Ecological synthesis

The two motifs imply a stronger monitoring principle than a one-way attenuation model:

> **Fragmentation damage can be hidden on either side of reproductive function. Interaction abundance or pollen quantity can remain high while function falls, and short-term reproductive output can remain comparatively buffered while mating/connectivity erodes.**

Thus no single layer is a universally safe sentinel of reproductive-system condition.

## Why quantity is not quality

The resolved `I+ / F-` examples are biologically compatible with interaction-quality failure.

- In *Eucalyptus wandoo*, the source explicitly argues that small populations can receive high pollen-tube loads but lower-quality pollen through a higher proportional contribution of self-pollen, reducing seed set despite abundant pollen arrival.
- In Kakamega *Acanthopale*, visitation occurrence is maintained while fruit set falls; the recovered data do not identify compatible pollen or post-pollination mechanism, so the causal stage remains open.
- The eight-programme I–F corpus contains no programme that directly measures effective mating quality on the same fragmentation frame.

The reverse point-sign cases also show why lower abundance need not imply lower function. In common milkweed, the source study notes lower pollinator abundance toward the urban centre but suggests that higher pollinator richness and delivery of more outcrossed pollen could alleviate pollen limitation in this highly self-incompatible species.

## Relation to previous literature

Previous meta-analyses show average negative fragmentation/land-use effects on pollination and female fitness and a positive across-species correlation between their effect sizes. This audit addresses a different level: paired within-system geometry and the possibility that one layer gives a reassuring signal while another deteriorates.

Previous individual studies have also shown that visitation rate alone can fail to explain seed production, and that low functional connectivity can coexist with demographic persistence. Therefore neither 'visitation is not enough' nor 'genetic and demographic responses can decouple' is itself novel.

The potentially distinctive synthesis here is **bidirectional masking across paired reproductive stages under one fragmentation programme**, with explicit scale auditing.

## Claim ceiling

Allowed:

- the current audited programmes contain examples of both hidden functional loss and hidden mating/connectivity erosion;
- all three resolved I–F mismatches are function-dominant;
- two resolved I–F programmes have opposite-sign `I+ / F-` geometry;
- no resolved `I- / F+` I–F mismatch is present in the current corpus;
- all four audited movement/mating→F programmes have larger absolute process than F responses on their registered representations, with the three direct systems preserving that ordering on lnRR;
- these motifs motivate multi-layer monitoring and a fresh Q→E→F test.

Not allowed:

- a global prevalence estimate for either masking mode;
- a sign/binomial test treating dependent panels as independent studies;
- a universal claim that interaction quality is the causal missing mechanism;
- a universal claim that mating/connectivity always deteriorates before function;
- treating unresolved sign reversals as confirmed compensation.

## Machine checks

- `scripts/check_if_sign_topology.py`
- `scripts/check_bidirectional_masking.py`
- `scripts/check_bottleneck_scale_robustness.py`
