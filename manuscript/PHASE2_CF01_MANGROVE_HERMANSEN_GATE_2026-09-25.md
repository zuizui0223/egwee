# CFTQ0312 urban mangrove direct I-F gate — 2026-09-25

## Programme

`P2_CF01_MANGROVE_HERMANSEN_2017`.

Primary source: Hermansen, Minchinton & Ayre (2017), *Oecologia* 185:221–231,
doi:10.1007/s00442-017-3941-1.

The source compares replicated *Avicennia marina* stands of three size classes within each of two
estuaries:

- large: >1500 trees;
- medium: 300–500 trees;
- small: <50 trees.

The abstract describes sets of three stands per size class within each estuary, implying a maximum
stand frame of 18 independent stands. The exact site table must be verified before calculation.

## Independent unit

Independent unit = **mangrove stand**.

Estuary is a source blocking factor. Trees, flowers, honeybee observations, fruits, propagules and
seedlings are nested below stand.

## Locked layers

Primary I candidate = stand-level abundance/activity of pollinators, especially the direct
honeybee-visitation measure used by the source.

Primary F candidate = direct fruit production / fruit output at stand level.

Fruit size/quality are secondary. Seedling recruitment/survival belong to D/resource-demography and
cannot replace F.

## Public-source recovery audit

The article confirms the full 18-stand geometry and makes the independent unit explicit through its
figure captions.

- Figure 2 reports honeybee and other-insect abundance for large, medium and small stands in both
  estuaries, and **each bar represents one stand**.
- Each pollinator stand mean is based on six 30-min video recordings on individual trees.
- Figure 3 reports fruit per floral shoot, fruit per tree and fruit weight for the same stand-size
  design, again with **each stand represented by one bar**.
- Fruit output is based on replicate trees within each stand (20 where available, with lower counts
  in some small stands).

Thus trees, videos, flowers and fruits are clearly nested below stand; the 18 stands are the
fragmentation-level units.

The remaining problem is numerical recoverability. The public text/tables do not expose one
machine-readable 18-stand vector for the primary pollinator response and one matching 18-stand
vector for fruit production. Those values are encoded graphically in Figures 2 and 3.

## Decision

Status:
`blocked_18stand_common_IF_vectors_not_publicly_recoverable_without_figure_digitization`.

No direct I-F Hedges-g programme is admitted.

The source ANOVA results confirm strong stand-size effects, but the frozen EGWEE direct family does
not back-transform omnibus/model tests into Hedges g without a prespecified compatible
standardization, and it does not digitize response figures to create stand values.

Direct I-F programme increment: **0**.

## Reopening condition

Reopen only if an authoritative public/source/author dataset supplies stand-level honeybee or broad
pollinator abundance and stand-level fruit production for the same stand frame, or supplies a
stand-level model contrast already on a compatible standardized scale.

## Admission

No direct Hedges-g effect is calculated until authoritative source material provides either:

1. stand-level I/F summaries on the same 18-stand or source-valid subset frame; or
2. source model contrasts with stand-level replication/uncertainty that can be mapped to the frozen
   large/medium/small design without treating trees or fruits as n.

A binary direct contrast must be source-defined before outcome selection. If the source is best
represented as an ordered stand-size gradient, retain it in Fisher-z/generalisation rather than
inventing a binary threshold.

## No rescue

Do not:

- count two estuaries as only two fragmentation replicates if stands are source-independent;
- count trees/flowers/fruits as stand n;
- collapse medium stands into small or large after inspecting effect strength;
- replace F with recruitment because recruitment is stronger;
- interpret a weak size class as evidence of equivalence.

All outcomes are retained.
