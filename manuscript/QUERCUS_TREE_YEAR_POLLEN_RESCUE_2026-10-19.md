# Quercus ilex: within-tree pollen supplementation versus early-to-late acorn attrition

**2026-10-19 | Empirical egwee exploratory cross-system check, one unfragmented oak programme.** Original experimental publication: Bogdziewicz et al. (2020), *Ecology Letters*, [doi:10.1111/ele.13609](https://doi.org/10.1111/ele.13609). Data: [Dryad doi:10.5061/dryad.sn02v6x2b](https://doi.org/10.5061/dryad.sn02v6x2b), with a [Zenodo mirror](https://zenodo.org/records/5306693). The original authors **already established** that flowering synchrony affects pollen limitation and hand pollination attenuates asynchronous-flowering seed losses. This is not a rediscovery of their phenology mechanism.

## New, narrower diagnostic

A realized pollen rescue recorded before the dry season need not persist unchanged to the final seed census. Re-evaluate exactly matched **same-tree control versus supplemented branches**, preserving two harvest stages (June early acorns; September after potential summer abortion) and both years. Ask whether the within-tree June treatment benefit persists by September, and whether the year contrast replicates among **the same trees**.

Haphazard branches were separated by vascular tissue but are **not** randomized independent trees; three shoots per branch are nested. The source table represents **960 shoot records** with **80 distinct tree IDs** observed in 2018 and 2019 (the paper describes 81 originally tagged trees). Of 160 potential tree-years, both branches have ≥1 jointly measured positive flower exposure and June/September acorn counts in **137 tree-years** (**67 in 2018, 70 in 2019**). Requiring all three source shoots complete in both branches leaves **109 tree-years** (47 in 2018, 62 in 2019). For the strict same-tree interannual change, **62 tree IDs** have both usable years.

Tree-year rate contrasts use treatment-specific source counted flowers in the exact same available shoot set at both censuses:

\[
\Delta_{June} =
\frac{\mathrm{June\ acorns}_{sup}}{\mathrm{flowers}_{sup}}
-
\frac{\mathrm{June\ acorns}_{control}}{\mathrm{flowers}_{control}},
\]
and \(\Delta_{Sept}\) replaces June by September acorns, with identically observed denominators. The attrition contrast is \(\Delta_{June}-\Delta_{Sept}\), **not** an estimated drought effect or a survival-probability contrast conditioned on initial acorn set.

## Source-data point estimates (rate difference, not count difference)

| Year | Independent trees | Mean added-minus-control rate in June | Mean in September | June minus September contrast |
|---|---:|---:|---:|---:|
| 2018 | 67 | **−0.0339** | **−0.0012** | −0.0327 |
| 2019 | 70 | **+0.0729** | **+0.0545** | +0.0184 |

All-three-shoot sensitivity: 2018 June **−0.0831**, September **−0.0568** (47 trees); 2019 June **+0.0611**, September **+0.0545** (62 trees). Thus the direction of the **descriptive annual response difference** does not depend only on including partial shoot arms.

In the **62 same trees** observed in both years, the year-to-year change in the treatment response (2019 minus 2018) is **+0.1016** for June and **+0.0620** for September; the original source has no synchrony or drought covariate in this shoot table to explain the changes. Paired tree-level uncertainty must be reported by the reproducible checker before interpreting significance. **The positive shift is not in itself a statistically demonstrated year × pollen-addition interaction.**

The source enforces acorns September ≤ acorns June ≤ original flowers when fully observed. Missing flowers, June counts or September counts are not zeros, and branches with no positive flower exposure are not assigned an effect of zero.

## Ecological reading and boundaries

Observed pollen supplementation can have different point effects by year and harvest stage, which is biologically consistent with changing pollen supply, flowering synchrony, resource conditions or fruit abortion. However the raw data do not identify these alternative processes. June and September acorns are repeated observations of shoots, not two independent experiments, and the 137 tree-years comprise only 80 distinct trees.

Relative to Sevenello's **different-plant, same-quadrat** OP versus OPSupp comparison, Quercus uses **paired branches within the same tree** and can better reduce between-plant floral-resource confounding, but resources may still move across branches and branch flower denominators differ. The two studies are genuinely separate publications/systems but cannot be pooled on a single reproductive benefit estimand without harmonizing designs.

This check complements the GloPL global FS/SPFR stage-response divergence and the fragmentation corpus; it does not establish a universal seasonal bottleneck, a response difference between insect/wind pollination, a direct drought effect or a new fragmentation result.

## Source integrity and status

The stored CSV at \`evidence/meta_extraction/quercus_ilex_pollen_2021/pollen_addition_results.csv\` came from a public Zenodo **text retrieval**. The publisher's original MD5 \`9bb924a2d0739e78e6823f1df6878e6a\` **does not match** the stored normalized text copy MD5 \`ec3ccf2901ab6f6de0bca9b90eafec86\`. Even though the size, rows, column types, logical nested sample design and numerical identities were verified, **source-byte identity is not certified**; this is a source-data recovery limitation, not hidden. Full details: \`evidence/meta_extraction/quercus_ilex_pollen_2021/SOURCE_PROVENANCE.md\`.

Code: \`scripts/audit_quercus_pollen_rescue_stages_20261019.py\`; CI \`.github/workflows/quercus-pollen-rescue-stages.yml\`. These checks must be green on the final branch before the automated reconstruction may be described as passed. No old ecological manuscript headline, corpus, publication freeze or \`submission_ready=false\` is changed.
