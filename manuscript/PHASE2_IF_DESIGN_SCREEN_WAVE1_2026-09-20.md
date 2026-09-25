# Phase-2 I-F design screen — wave 1 — 2026-09-20

## Current state

The outcome-blind metadata queue contains 32 unresolved publication identities for which the SF06 source table jointly flags pollination/interaction (I), reproductive fitness (F), and habitat fragmentation.

Wave 1 screens the first eight identities using title, abstract and methods/design information only. No Hedges d, source effect direction, p-value, significance label, or candidate-specific outcome magnitude is used for retention or closure.

Machine-readable decisions are stored in `evidence/meta_extraction/phase2_if_design_screen_v1.csv`.

## Wave-1 decisions

### Advance to quantitative full-text design recovery — 4

- **IFQ003 — Angoh et al. 2021, Erica discolor.** Source-defined patch-size/isolation fragmentation landscape; visitation and seed set share the patch system. Exact patch replication and dispersion remain to be recovered.
- **IFQ006 — Chen & Zuo 2019, Haloxylon ammodendron.** Methods specify six fragmented and six natural plots under one habitat experiment; visitation and reproductive success use the same 12-plot design.
- **IFQ007 — Chen et al. 2019, Caragana korshinskii.** Methods specify six fragmented and six natural 20×20 m plots; pollinator activity and seed-set/pollen-limitation responses share that design.
- **IFQ008 — Chiapero et al. 2021, Lithraea molleoides.** Study explicitly compares continuous versus fragmented Chaco Serrano forests and simultaneously evaluates reproductive ecology and progeny performance; exact site counts/common endpoint frame still need full-text recovery.

### Programme decomposition / duplicate audit — 1

- **IFQ002 — Aguilar 2005 PhD thesis.** SF06 contains many species and response rows from a thesis-level source. It cannot be treated as one programme or as 12 independent programmes without resolving chapters/species and overlap with later primary publications. It advances to decomposition/crosswalk only.

### Closed on design geometry — 3

- **IFQ001 — Abrahamczyk et al. 2021, Centaurea scabiosa.** Fourteen populations support a population-size analysis of visitation and achene production. Fragmentation is background context; the response model is not a source-defined fragmentation contrast.
- **IFQ004 — Barreto et al. 2018, Justicia aequilabris.** Edge versus interior is sampled inside one dry-forest fragment, so nested plants/flowers cannot become independent fragmentation replicates.
- **IFQ005 — Cascante et al. 2002, Samanea saman.** Isolated trees are contrasted with trees nested in one continuous population/reserve. The continuous reference landscape is not independently replicated.

## Counts

- primary I-F fragmentation metadata queue: **32**
- screened in wave 1: **8**
- advance to quantitative full-text screen: **4**
- advance to programme decomposition/crosswalk: **1**
- closed on design geometry/exposure: **3**
- pending primary I-F design screen: **24**
- newly admitted quantitative I-F programmes: **0**
- effect outcomes opened for screening decisions: **0**

## Immediate quantitative priority

The four advancing records are ordered by recoverable design geometry, not expected result:

1. **IFQ007 Caragana korshinskii** — explicit 6 fragmented + 6 natural plots.
2. **IFQ006 Haloxylon ammodendron** — explicit 6 fragmented + 6 natural plots.
3. **IFQ003 Erica discolor** — explicit patch-size/isolation fragmentation with same-system visitation + seed set; exact n pending.
4. **IFQ008 Lithraea molleoides** — explicit continuous/fragmented forests and multiple reproductive layers; exact n pending.

No I-F pair count changes until a candidate passes endpoint, independent-unit and dependence reconstruction checks.
