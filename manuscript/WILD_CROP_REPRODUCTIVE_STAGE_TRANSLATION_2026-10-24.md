# Wild and crop pollen-supplementation experiments: stage-response nonconcordance

**Empirical egwee, 2026-10-24.** External cross-domain macroanalysis. This is **not** the theoretical egwe programme or an independently admitted fragmentation meta-analysis. **Exploratory, source-locked, post hoc comparisons, not preregistered confirmation.**

## Question and source boundary

Can one observed pollen-supplementation intervention yield different directional conclusions depending on which portion of reproduction is measured, in **both wild plants and domesticated crops**? Which comparisons survive independent publication weighting and removal of concentrated taxa/sources?

- **Wild:** Bennett et al. (2018), GloPL, [doi:10.1038/sdata.2018.249](https://doi.org/10.1038/sdata.2018.249), [Dryad](https://doi.org/10.5061/dryad.dt437), **2,969 cases / 927 source publications / 1,265 species**. Source pair: **FS** (fruit set) and **SPFR** (*seeds per an existing fruit*).
- **Crop:** Siopa et al. (2023), PolLimCrop, [doi:10.1038/s41597-023-02797-6](https://doi.org/10.1038/s41597-023-02797-6), [Figshare original](https://doi.org/10.6084/m9.figshare.24625299.v1), CC0. The original physical v1 file contains **1,168 rows** (paper describes 1,169), IDs 1…1169 but **256 missing**, 293 distinct \`article_code\` values. Crop pair **FS** (fruit set) vs **SN** (seed number). **SN is not certified to be "seeds per existing fruit" for every primary crop study**, so the two datasets do not have identical estimands and their percentages must **never be pooled or tested for equivalence**.

Both original compilation papers already show positive mean responses to pollen addition and metric-dependent effect sizes; these are well-established ecology, **not egwee discoveries**. Source GloPL was decoded from a legacy-character Git blob into a numerical table in a UTF-8 mirror. The crop source was also retrieved as UTF-8 text; its checksum differs from the **original publisher bytes** (see [original-source receipt](../evidence/meta_extraction/pollimcrop_2023/SOURCE_PROVENANCE.md)). Numeric reproducibility is supported by row/source and original-header checks but *not certified raw-byte fidelity*.

Only same-case **observed raw mean differences** are compared. Zero contrasts stay in the data inventory but are excluded from a binary two-nonzero-sign table. Missing observations are not zero. Case/flower counts are **not** independent publication replications.

## Positive external generality result — stages can respond in opposite directions

| Same experimental case | Nonzero paired comparisons | Opposite point directions | Independent publication-code groups | Equal-publication discordance fraction and cluster-bootstrap 95% interval |
|---|---:|---:|---:|---|
| Wild FS vs seeds **per fruit** (GloPL) | **313** | **81 (25.9%)** | **84** | **23.8% [16.9%,31.4%]** |
| Crop FS vs reported **seed number** (PolLimCrop) | **300** | **75 (25.0%)** | **72** | **23.3% [15.2%,32.0%]** |
| Crop FS vs seed number, excluding the **three DOIs overlapping** the wild corpus | **299** | **75 (25.1%)** | **71** | **23.7% [15.4%,32.3%]** |
| Crop FS vs **fruit weight** | **292** | **117 (40.1%)** | **84** | **33.8% [25.5%,42.4%]** |

The three original publication DOI intersections: \`10.1093/aob/mcr293\`, \`10.1111/j.1744-7909.2008.00800.x\`, \`10.1590/s0006-87052009000100002\`. Thus the complete wild and crop datasets are **not** universally source-disjoint; the exclusion is mandatory for a source-independent crop sensitivity.

Crop FS-SN 2×2 among 300 cases (row = FS change, column = SN change):

| | SN higher | SN lower |
|---|---:|---:|
| FS higher | 188 | **36** |
| FS lower | **39** | 37 |

There are cases of both FS-up/SN-down and FS-down/SN-up. **This is an existence and point-direction topology, not the true prevalence of physiological conflict.** The source datasets are selected for studies that measure both endpoints, positive/negative means are noisy, and the SD/N data lack the necessary biological covariance to prove each discordance. The crop screen has **four cases from four distinct sources** with both marginal |z|≥2.2414 (naive SD/N independent-arm reference only), while wild FS-SPFR has **none** at this tighter screen. Those four must be verified in source units before being treated as independently established biological reversals.

### Taxonomic and source-selection sensitivity in crops

Rosaceae, especially *Malus domestica*, is heavily represented. Of the 300 crop cases, 180 are apple cases; 192 are Rosaceae cases. Results after transparent exclusions:

| Crop FS-SN frame | Mismatch / cases | Publications | Equal-publication mismatch fraction |
|---|---:|---:|---:|
| All | 75/300 (25.0%) | 72 | 23.3% |
| No *Malus domestica* | **25/120 (20.8%)** | 58 | 21.9% |
| No Rosaceae | **24/108 (22.2%)** | 53 | 23.0% |
| No single largest publication (74 eligible cases, 31 mismatches) | **44/226 (19.5%)** | 71 | 23.1% |

The broad stage-response mismatch cannot be attributed **exclusively** to apple, Rosaceae or the largest source. It does **not** imply common frequency among all plants or landscapes.

## A stronger same-crop-triple pattern, and its uncertainty ceiling

To avoid comparing separate source subsets for different outcomes, **178 experiments from 45 publications** recorded all three nonzero responses: **fruit set FS, seed number SN and fruit weight FW**.

Among the **same 178 records**:

- Fruit-set direction versus seed-number direction differs in **51** cases.
- Fruit-set direction versus fruit-weight direction differs in **81** cases.
- Directly paired comparison: **48** cases have FS–FW mismatch only, versus **18** with FS–SN mismatch only; **112** have equal binary mismatch status for both pairs.

The case-level excess of FS–FW discordance is **16.9 percentage points**. The **equally weighted 45-publication excess** is **17.2 percentage points** (a source-cluster bootstrap from the raw data gives approximately **5–29 percentage points**); 17 sources show a positive difference, 3 show a negative difference, 25 tie. A publication-sign-flip reference p is around **0.008**, but this test was chosen **after inspecting ten pairwise endpoint comparisons**; it is therefore **exploratory, not multiplicity-corrected confirmatory evidence**.

Sensitivity:

- Excluding apple: 64 triple cases, publication-equal excess ~16.7 percentage points; uncertainty broad.
- Excluding all Rosaceae: 59 triple cases, publication-equal excess ~11.8 percentage points, with source-bootstrap interval including zero.
- Excluding the largest publication: 122 triple cases, publication-equal excess ~17.3 percentage points.
- **Crucial precision falsification:** among the 99 triple cases with SD/N for all three responses, the source-balanced difference is smaller (~9.6 percentage points). In the **11 cases where all three nominal |z|≥1.96**, the FS–SN and FS–FW mismatch counts are **2 versus 2**. Fruit-weight and seed-count precision differ. Thus the descriptive excess could be due partly to endpoint measurement reliability, sampling design and source composition, not necessarily a distinct fruit-mass resource bottleneck.

## Ecological interpretation and novelty limits

A single treatment can appear successful by one reproductive endpoint and unsuccessful by another in both wild and agricultural contexts. **Interaction/treatment quantity does not uniquely translate into every component of realized function.** This is compatible with variation in mating compatibility, fruit abortion, resource allocation, fruit mass, flower display and sampling uncertainty; **no one mediator is identified**. Neither comparison tests an experiment's effect of fragmentation, nor does it establish a universal causal tradeoff or crop yield loss.

This extends the **existence domain of endpoint non-identification** but does not newly invent the response–effect distinction or pollen limitation as concepts. Prior source literature explicitly cautions that partial-flower supplementation and resource reallocation can bias pollen limitation estimates (Ashman et al., 2006, doi:10.3732/ajb.93.2.271), and that metrics carry different effects (GloPL 2018, PolLimCrop 2023). The added scientific contribution is a **same-experiment, multi-endpoint, publication-balanced and cross-source-overlap-audited empirical topology**, with a deliberately conservative precision ceiling.

The stronger **original empirical egwee fragmentation claim** remains separate: three independent matched landscape programmes with downstream I–F mismatch (Wandoo, Cardiopetalum and Acanthopale), not enlarged by these external pollen supplementation cases.

## Full reproducibility / publication boundary

- [Source files and byte/row caveats](../evidence/meta_extraction/pollimcrop_2023/SOURCE_PROVENANCE.md).
- [Pooled-source–safe paired analysis code](../scripts/audit_pollimcrop_glopl_cross_context_20261024.py) and [standalone workflow](../.github/workflows/pollimcrop-glopl-cross-context.yml).
- GitHub Actions output includes: publication-cluster bootstrap intervals, source-overlap, all ten crop endpoint pairs, full 2×2 response tables, triple-only paired difference with source sign-flip test, no-apple/no-Rosaceae/no-largest-source sensitivity and precision screens. A separate CSV preserves the 75 mismatched crop cases for auditing.
- **No** silent changes to registered five direct fragmentation clusters, eight quantitative matched I–F programmes, sixteen mixed-tier qualitative programmes, SF06 denominator, manuscript scale estimand, or \`submission_ready=false\`.
