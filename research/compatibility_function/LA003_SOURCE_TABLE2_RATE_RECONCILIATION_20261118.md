# LA003 — published visitation rate reconstructed in part from original Dryad observation sheets

**Source-only audit, 2026-11-18.** This is not a seed-fitness analysis, hypothesis test, or alteration of the frozen LA001/LA002 negative results.

## Exact evidence and scope

Original Layman, Fernando, Herlihy & Busch (2017), *Evolution* 71:884–897, [DOI 10.1111/evo.13167](https://doi.org/10.1111/evo.13167), Table 2. Exact user-supplied original Dryad ZIP [10.5061/dryad.2pj0j](https://doi.org/10.5061/dryad.2pj0j), SHA256 `82bcaa1c3a504cc779bc9c2aa95199a657dd404b3fdf62f7059e4ff5028b39c1`; outer and inner XLSX CRC checks passed. Third-party original data are **not republished**. Source-analysis script: `run_la003_published_visit_rate_audit.py`.

All 121 completed half-hour source observation periods match the Methods (45 in 2014, 76 in 2015). Each source `TOTAL` equals the number of numeric plant-position tokens logged between `Open Flowers` and `TOTAL`. Across these 121 sessions:

| Original-source counting unit | Total | 2014 | 2015 |
|---|---:|---:|---:|
| Insect-event rows | **2,850** | 532 | 2,318 |
| Numeric plant-position tokens (including invalid 34) | **6,702** | 1,657 | 5,045 |
| Sum of unique plant positions *within each insect-event row* | **5,064** | 1,370 | 3,694 |
| Admissible 1–32 tokens after excluding zero-open-flower positions | **6,663** | 1,620 | 5,043 |
| Article Table 2 total visits | **3,748** | not explicitly disaggregated | not explicitly disaggregated |

Thus the published **3,748** is not a direct read of the insect-row count, the all-position count, or event-wise distinct plant positions. There are **38** original in-range tokens to zero-open-flower positions (37 in 2014, one in 2015), and one out-of-range `34` (2015).

## A useful partial numerical reproduction: visits per flower per hour

For each completed 30-minute source observation period, within a genotype group (SC vs SI), compute `2 × (numeric positions visited in group) / (number of open flowers in group)` and then average across sessions with nonzero open flowers in that genotype. Do *not* substitute the pooled total across all periods, which weights flower-rich sessions differently. The source-only reconstruction gives:

| Year | Genotype | Mean source position-token rate (visits / flower / hour) | **Published Table 2 total rate** | Source − paper |
|---|---|---:|---:|---:|
| 2014 | SI | 1.98577 | 2.008 | −0.02223 |
| 2014 | SC | **2.24547** | **2.245** | **+0.00047** |
| 2015 | SI | 1.03913 | 1.068 | −0.02887 |
| 2015 | SC | 1.14730 | 1.167 | −0.01970 |

In particular, the **2014 SC** source per-period mean matches the paper to rounding. Its source solitary-bee rate `1.67818` versus paper `1.678` and source other-Diptera rate `0.19057` versus paper `0.191` are also near exact. This indicates the source's position-token numerator and open-flower denominator can reproduce **part** of the published rate method, and the prior issue should no longer say the whole visitation calculation is opaque.

## Unresolved taxon classification

A separate source-only audit of the *case-sensitive* taxon codes found:

| 2014 code | Insect-event rows | Position tokens |
|---|---:|---:|
| `Bf` | **44** | **205** |
| `BF` | **3** | **4** |

The 2015 source uses `BF` (85 insect-event rows, 780 tokens) and no `Bf`. The existing LA001/LA002 source parser converts both 2014 codes to uppercase `BF`, but it is **not established from a source legend** whether these were interchangeable insect categories. Under that case-insensitive assumption, 2014 SC's source BF rate was **0.22515**, whereas paper Table 2's bee-fly rate was **0.080**; source category *Other* was **0.15157**, whereas paper *Other* was **0.297**. The opposite shifts nearly offset in the combined visitation rate. This is a **taxonomy/codebook ambiguity**, not grounds to declare the source wrong or retroactively reclassify insects to fit the paper.

## 2015 status

Source per-period SC/SI rates are close to Table 2 but differ by ~0.02–0.03 visits/flower/hour. The 2015 field workbook has **80** `Open Flowers` rows and **76** completed `TOTAL` periods. These four unfinished source periods were excluded under the pre-outcome LA001 protocol; they must not be added merely to force a published total. The exact published filtering/averaging protocol and taxon grouping remain unverified.

## Single-visit assay control mismatch remains

The paper reports **17** bagged controls. In the supplied `Emasculation+experiment.xlsx / Final pass`, there are **21** control rows, including one fruit with one seed. Which four controls were omitted in the paper, and why, is not identified; no source-based row selection was performed. The independent assay's solitary-bee, bee-fly, and other-Diptera n/fruit/seed counts agree with the paper and remain fixed in LA002.

## Reproducibility / scientific decision

This audit reads **only** original pollinator worksheets. The archive's `main.cpp`, `Individual.h`, and `Locus.h` simulate mating compatibility, selection, and mutation; they **do not provide the missing observation-table cleaning/aggregation script**. No individual plant/seed/genotype values, raw original event sequence, or source XLSX were committed. The audit script must be supplied the original ZIP locally; GitHub CI only checks source-withheld logic and aggregate receipts.

**Issue #67 remains open** with a narrowed blocker: recover the *exact* paper counting unit for 3,748, the 2014 `Bf` versus `BF` dictionary, small 2015 rate corrections, and which four control rows were excluded. Until then, LA001/LA002 are legitimate analyses under their declared source-token operationalization but **not** complete replications of the original article's Table 2. Their primary negative conclusions are unchanged and no post-hoc predictive retuning is authorized.

## 2026-11-18 supplementary correction: original code label found

A subsequent **source-only** check found the literal 2014 code glossary in `Pollinator+Data+2014.xlsx`, `Landersville Field - Temporal`, row 1. It states **`Bf - Bee Fly`** and **`B - Butterfly`**, together with `F - Fly`, `H - Honey Bee`, `AH - Adrenid / Halictid` and `U - Unknown`. Thus **the literal `Bf` meaning is not entirely unknown**. The uppercase `BF` seen in the main array data has no separate explicit definition in this ancillary temporal-sheet glossary. The casefold-based BF/Other rates are still not the published Table 2 category rates; arbitrary reassignment of `Bf` to butterflies would contradict the source codebook.

Both original sheets of `Emasculation+experiment.xlsx` contain 21 control entries with complete fruit outcomes; the `Final pass` 21 controls all have dates (7 on 2015-03-15, 14 on 2015-03-16), so **the article's 17 controls cannot be reconciled by missing dates/outcomes or by an entire-date exclusion**. This does not identify which controls the article counted.

Full audit, rates under both case rules, source counts and scientific limits:
`LA004_SOURCE_CODEBOOK_CONTROL_AUDIT_20261118.md`. The 3,748 published visit-unit mapping remains unresolved, and LA001/LA002 negative predictive conclusions are not modified.
