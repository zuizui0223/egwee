# Complete paired process–function bottleneck census — 2026-09-27

## Scope

This document is the canonical descriptive census behind the manuscript-level conclusion that habitat fragmentation does not impose one fixed life-cycle bottleneck.

It unifies two non-overlapping registered programme sets:

- **8 interaction/pollen-quantity–F programmes**;
- **4 movement/connectivity or mating-support–F programmes**.

The programme IDs are disjoint, giving **12 independent programmes** in the complete process–function denominator.

Effect families remain separate. Hedges-g and Fisher-z values are never pooled numerically.

## Complete denominator

Across 12 programmes:

- pair-testable: **11**;
- resolved process–F mismatch: **4**;
- unresolved: **7**;
- not testable: **1**.

Among the four resolved mismatches:

- **3 are downstream function-dominant**: F is more negative than interaction quantity;
- **1 is upstream process-dominant**: movement/connectivity is more negative than F.

The resolved downstream programmes are:

- *Eucalyptus wandoo*;
- *Cardiopetalum calophyllum*;
- Kakamega *Acanthopale pubescens* programme.

The resolved upstream programme is:

- *Serapias lingua* — pollen immigration more negative than fruit set.

## Interaction–function subset

The 8-programme I–F subset contains:

- pair-testable: 7;
- resolved: 3;
- unresolved: 4;
- not testable: 1;
- resolved F-more-negative-than-I: 3;
- resolved I-more-negative-than-F: 0.

This subset also exposes the measurement gap:

- quantity-level interaction/pollen endpoints: **8/8**;
- direct effective-mating-quality endpoints on the same I–F frame: **0/8**.

## Movement/mating–function subset

The 4-programme movement/connectivity or mating-support–F subset contains:

- resolved: 1;
- unresolved: 3;
- resolved process-more-negative-than-F: 1;
- resolved F-more-negative-than-process: 0.

Point estimates place the process endpoint more negative than F in 3/4 programmes, but only *Serapias* resolves the difference. No pooled directional law is inferred.

## Ecological interpretation

The complete denominator contains both directions of resolved mismatch.

This rules out two simplistic descriptions of the current corpus:

1. reproductive function is always the first or strongest component to deteriorate;
2. movement/mating support is always the first or strongest component to deteriorate.

The supported description is instead:

> **The position of the strongest fragmentation response varies among natural plant systems.**

Some systems show downstream function-dominant mismatch, some show upstream process-dominant mismatch, and many remain unresolved or approximately coupled at current precision.

## Statistical boundary

The **3 downstream : 1 upstream** resolved split is descriptive.

Do not:

- convert it into a binomial or sign test;
- estimate global regime prevalence from 12 programmes;
- pool Hedges-g and Fisher-z differences;
- classify unresolved programmes as coupled;
- infer one common causal mechanism.

## Fresh-validation consequence

The next prospective question is bottleneck localization within the same new programme:

`Q = interaction quantity`

`E = effective mating / compatible pollen / realized mating quality`

`F = reproductive function`

with primary fresh H2-v2 contrast:

`Delta_QE = Q - E`.

The current 12 programmes are discovery evidence. Existing I–F programmes and the four auxiliary movement/mating–F programmes cannot be reused as fresh H2-v2 confirmation.

## Machine-readable source

- `evidence/meta_extraction/ecological_process_function_programme_census_v1.csv`
- `scripts/check_ecological_process_function_programme_census.py`

## Main-paper representation

- Table 2 contains all 12 programmes.
- Figure 4 summarizes the major response geometries and the measurement gap.
