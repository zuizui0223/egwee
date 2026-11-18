# LA004 — original internal insect-code glossary and control denominator audit

**2026-11-18.** Source-only provenance audit. **No new ecological effect, no inference on individual seed data, and no revision of the frozen LA001/LA002 site-holdout negatives.**

## Source and exact worksheet-backed discovery

The original user-provided Layman et al. 2017 Dryad archive [10.5061/dryad.2pj0j](https://doi.org/10.5061/dryad.2pj0j) (SHA256 `82bcaa1c3a504cc779bc9c2aa95199a657dd404b3fdf62f7059e4ff5028b39c1`) contains a previously unexamined **literal insect taxon glossary** at `Pollinator+Data+2014.xlsx` → `Landersville Field - Temporal` → **row 1**:

| Literal code | Source worksheet label | Source-grounded meaning |
|---|---|---|
| `F` | `F - Fly` | fly |
| **`Bf`** | **`Bf - Bee Fly`** | **bee-fly** |
| `B` | `B - Butterfly` | butterfly |
| `H` | `H - Honey Bee` | honey bee |
| `AH` | `AH - Adrenid / Halictid` | solitary bee groups (source spelling) |
| `U` | `U - Unknown` | unknown |

**Correction to LA003 wording:** It is no longer defensible to say the biological meaning of the **literal `Bf` string itself** is wholly unknown: the original archive explicitly labels it *Bee Fly*, not butterfly. This glossary is from an ancillary **temporal sheet**, not a formally linked machine-readable codebook covering every site/year. The spelling `BF` in main array sheets is not separately explained there; treating `Bf` and `BF` as the same bee-fly category remains a plausible case normalization but is not a complete reproduction of Table 2.

### Counts by case from the 121 completed source periods

| Source taxon code | Insect-event rows | Plant-position tokens |
|---|---:|---:|
| 2014 `Bf` | **44** | **205** |
| 2014 `BF` | **3** | **4** |
| 2014 `B` (butterfly) | **7** | **34** |
| 2015 `BF` | **85** | **780** |

Across both years the 121 source periods still contain **2,850 insect-event rows** and **6,702 plant-position tokens**, not the **3,748 visits** reported in original [Table 2](https://doi.org/10.1111/evo.13167). At the raw-token grain, collapsing `Bf` with `BF` produces AH **3,414 (50.94%)**, BF **989 (14.76%)**, other F **1,910 (28.50%)**, and Other **389 (5.80%)**, compared with the paper's 46.7%, 14.4%, 28.7%, 10.2% share respectively. These ratios are **not equivalent denominators**, and relative agreement for two taxa does not resolve 3,748.

### Why simply changing case normalization cannot reconcile 2014

The source-pinned LA003 formula is the per-completed-30min period mean `2 × recorded in-range plant-position visits in group / number of open flowers in same genotype group`. Compare two **diagnostic** encodings, neither promoted as a newly selected scientific model:

| 2014 / genotype | BF = `Bf` + `BF` | BF = literal `BF` only | Published BF | Other excluding `Bf` | Other including `Bf` | Published Other |
|---|---:|---:|---:|---:|---:|---:|
| SI | 0.18617 | 0.00278 | **0.060** | 0.10340 | 0.28679 | **0.236** |
| SC | 0.22515 | 0.00845 | **0.080** | 0.15157 | 0.36827 | **0.297** |

Neither of these two whole-category interpretations matches both published category rates, so treating `Bf` as butterfly (contrary to the explicit glossary) or silently uppercasing values is **not an adequate resolution**. A partial near-exact reproduction of **2014 SC total visitation rate** (source 2.24547, paper 2.245), and its AH/F subdivisions, remains valid as already documented by LA003. **3,748 remains an open source-processing question.**

## Rechecked the controls in both original sheets

The `Emasculation+experiment.xlsx` workbook has two tables, `Final pass` and `Fruit set first pass`. Both contain **21** literal `Control` entries; in both, every row has a recorded fruit outcome (**20 no fruit, one fruit with one seed**). In the Final pass sheet all **21** also have dates, divided into **7 observations on Excel date serial 42078 (2015-03-15)** and **14 on 42079 (2015-03-16)**. No four controls can be eliminated by a standard missing-date, missing-fruit or whole-day filter to reproduce the paper's **17** bagged control flowers.

This **does not prove** the article's 17 was wrong: differences in intended eligibility, treatment timing or unpublished exclusion rules may exist. With no source record defining which four should be excluded, **none are discarded or substituted**.

## Decision and next source gate

**What is resolved:** the literal 2014 `Bf` and `B` definitions, their raw counts, the inability of case folding alone to repair the category rates, and the fact that the extra controls are fully observed.

**Still unresolved:** the exact rule for article's total **3,748** visits; possible cross-sheet change in `BF` spelling; 2015's small rate differences; the source-based criteria that map **21** original controls to **17** article controls.

The archive's `main.cpp`, `Individual.h`, and `Locus.h` simulate mating/genetics, not the 2017 article's site-level observation preprocessing. No source file in this archive contains a literal 3,748 visit aggregate or a documented selection of 17 control records.

The strict next gate is an **author-confirmed Table 2 processing script or original observation codebook / exclusion log**. No result-conditioned visitor filtering, alternate site exclusion, case splitting, or fitted recalibration of field seed effects is permitted.

### Reproduce from the exact user-supplied archive

```bash
python research/compatibility_function/run_la004_glossary_control_audit.py \
  --source-zip /path/to/doi_10_5061_dryad_2pj0j__v20161228.zip \
  --output /tmp/LA004_source_only_receipt.json
```

The runner fails on wrong SHA, missing glossary, wrong source periods/category counts, control outcome incompleteness, or changed 6,702/2,850 source denominators. It writes only aggregated counts/rates/labels. The ZIP and individual rows are never redistributed via GitHub; CI is source-withheld and tests only synthetic controls plus source-generated aggregate receipts. Original LA001 and LA002 negative site-held-out predictions stay frozen.

## 2026-11-18 official Dryad dataset-page clarification

The primary Dryad **file descriptions for both 2014 and 2015 main-array files** use a different, broader official code dictionary from the ancillary temporal-sheet glossary quoted above: **`BF` = bee-fly, `B` = honeybee or carpenter bee, `L` = lepidoptera**, `F` = other Diptera, `AH` = Andrenidae/Halictidae, `K` = katydid and `U` = unknown. This **supersedes any implicit generalization of the ancillary temporal `B = Butterfly` label to every array worksheet**. Both source descriptions remain inspectable; do not retroactively erase the conflict. Exact citation and scientific limits: `LA005_OFFICIAL_DRYAD_MAIN_ARRAY_CODEBOOK_20261118.md`. Published visit total 3,748 remains unresolved.
