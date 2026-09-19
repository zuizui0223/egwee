# ML002 Brosimum adult-offspring genetic reconciliation — 2026-09-19

## Decision

The existing ML002 *Brosimum alicastrum* programme remains **blocked from the Phase-2 `G_adult-G_offspring` family**.

The study design itself is adequate for a direct pair: three continuous-forest populations and three fragmented populations, with adult and progeny genotypes from the same six populations. The blocker is reproducibility of the published genetic-state endpoint from the public genotype workbook, not fragmentation-level replication.

No Phase-1 result changes, and the Phase-2 G-pair coverage remains **4/5**.

## First audit: observed heterozygosity H_O

The public Figshare workbook was reconstructed at the site and habitat × cohort levels.

Published Table-2 targets:
- continuous adults: 0.62;
- fragmented adults: 0.63;
- continuous progeny: 0.58;
- fragmented progeny: 0.59.

Neither a pooled-individual locus-mean reconstruction nor an equal-weight mean of site-level locus H_O reproduced all four cells at reported precision. The largest discrepancy is continuous adults: approximately 0.577–0.583 from the public workbook versus 0.62 in the publication.

Therefore H_O remains fail-closed and is not promoted.

## Reproducibility-only H_E fallback

Before calculating any H_E site-level effect, four transparent estimators were frozen as the only allowed fallback candidates.

Published Table-2 H_E targets:
- continuous adults: 0.65;
- fragmented adults: 0.63;
- continuous progeny: 0.59;
- fragmented progeny: 0.60.

Observed reconstructions:

| estimator | CON adult | FRA adult | CON progeny | FRA progeny | all four match? |
|---|---:|---:|---:|---:|---|
| pooled H_E | 0.618019 | 0.616368 | 0.603059 | 0.624830 | no |
| pooled unbiased H_E | 0.620173 | 0.625049 | 0.603857 | 0.626314 | no |
| mean site H_E | 0.605122 | 0.585364 | 0.583277 | 0.593925 | no |
| mean site unbiased H_E | 0.611960 | 0.620709 | 0.586184 | 0.598223 | no |

Thus **0/4 predeclared estimators reproduce all four publication cells**.

## Scientific interpretation

This is not evidence against an adult-offspring fragmentation contrast in *Brosimum*. It means the public genotype file and the publication's reported habitat-level genetic summaries cannot currently be reconciled under the declared transparent estimators.

The programme is therefore assigned:

`blocked_publication_raw_genotype_reconciliation`

Reopening requires one of:
- source/author-validated genotype data matching the publication analysis;
- the exact source code or estimator/provenance that reproduces the four Table-2 cells;
- an independently archived corrected genotype version with explicit version provenance.

It cannot be reopened by choosing a genetic estimator because it produces a convenient effect, or by treating individuals/loci as fragmentation replicates.

## Phase-2 consequence

- G_adult-G_offspring programme increment from Brosimum: **0**
- current G_adult-G_offspring coverage: **4/5**
- current systems remain: ML003, P2_SF05_93, P2_SF05_71, P2_CF01_GPAIR_002
- no pair-specific meta-analysis is opened from Brosimum
- frozen Phase-1 ML002 C/F effects and the five-cluster synthesis remain untouched

The dedicated reconciliation workflow should therefore pass by reproducing this **blocked** state, not fail as if a software error occurred.
