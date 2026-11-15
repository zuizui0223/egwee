# Primary-source check of Clarke's reproductive-success rows — 2026-11-15

**Stage:** outcome-blind, source-definition screening after endpoint ontology lock; no fit effect directions, confidence intervals, rescue success classifications or new pooled effect sizes opened. Source schema receipt: GitHub Actions [run 43680981170](https://github.com/zuizui0223/egwee/actions/runs/43680981170), artifact `14147134980`, source workbook SHA-256 `cd95a8aa42beabd4f34650e1e782a03919621b0a2a53e6b4f027fd43d086d5ae`.

## Correct independent denominators

- Original published Clarke et al. (2024), *Molecular Ecology*, DOI [10.1111/mec.17532](https://doi.org/10.1111/mec.17532): **19** independent publications / **27** usable paired genetic+fitness cases, primarily mammals.
- Author's frozen `He_dGR.xlsx` original analysis slice has **27 complete rows** and **19 unique Study IDs**. Endpoint labels: `PS` 20 comparisons, `SR` 4, `IR` 3. Figure/Table in Clarke label the corresponding endpoint classes **population growth/size, survival rate and reproductive success**; the `IR` code's biological interpretation remains **reproductive contribution**, *not* automatically partner-mediated or plant reproductive function.
- Only **2 unique papers** supply the 3 `IR` comparisons: **Arrendal (2004)** two cases and **Gustafson (2017)** one. **19/27** rows use the same numeric post-intervention generation for genetic and fitness measurements; **8/27** use different generations. Matching numeric generation tags do not prove synchronized within-cohort sampling.
- 27 rows must not be analyzed as 27 independent rescue systems.

## Source screen 1 — otter translocation

**Arrendal J, Walker CW, Sundqvist A-K, Hellborg L, Vilà C (2004)**, *Genetic evaluation of an otter translocation program*, *Conservation Genetics* 5:79–88. DOI [10.1023/B:COGE.0000014059.49606.dd](https://doi.org/10.1023/B:COGE.0000014059.49606.dd). Publisher abstract and source: https://link.springer.com/article/10.1023/B:COGE.0000014059.49606.dd

Design: documented translocation/reintroduction of Norwegian Eurasian otters into two Swedish localities; native and translocated genetic identities tracked with mtDNA and nuclear markers. Release areas involved **47** individuals near one locality and **7** at another. Authors caution that post-release population growth should **not** be assigned to introduced animals automatically: no detectable genetic contribution at the first evaluated locality, detectable altered composition near the second. Observed change in population abundance reflects demography as well as the intervention and cannot by itself identify genetic rescue; mating/offspring contribution is source-specific and geographically restricted.

**Endpoint decision:** the Clarke `IR` summaries require source-specific ascertainment; even if interpreted as offspring contribution, *ecological-function recovery* (plant pollination, compatible seeds, effective dispersal service or another direct interaction-dependent process) **was not measured** by the cited translocation-genetic evaluation. **Not admitted to `F_direct`.** Not a negative result about functional rescue in this system; that endpoint is missing.

## Source screen 2 — puma natural migrant

**Gustafson KD, Vickers TW, Boyce WM, Ernest HB (2017)**, *A single migrant enhances the genetic diversity of an inbred puma population*, *Royal Society Open Science* 4:170115. DOI [10.1098/rsos.170115](https://doi.org/10.1098/rsos.170115). Open full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC5451821/

Design: observational **natural migration**, not a planned translocation intervention. A male puma (M86) crossed an interstate barrier and was identified as the sire of **11 offspring**. Heterozygosity and allelic richness increased in the small population, but the authors explicitly distinguish *genetic restoration* from causally established *genetic rescue*. Field variation in survival, territory, resources and other mortality means that relief of inbreeding depression was **not confirmed**.

**Endpoint decision:** a pedigree-supported reproductive event, but no controlled `gene flow × habitat/interaction` comparison and no measured partner-mediated ecosystem function. It can motivate a `G` genetic contribution / `W` offspring observation, **not an estimate of ecological-function rescue or causal genetic rescue**. **Not admitted to `F_direct`.**

## Gate 1 verdict

| Quantity | Result | Meaning |
|---|---:|---|
| Source publications | 19 | independent paper denominator, not 27 |
| Original usable paired rows | 27 | 20 population growth/size + 4 survival + 3 reproductive |
| `IR` rows | 3 | only two unique original papers |
| `F_direct` confirmed via original `IR` papers | **0** | no ecology-function endpoint established within this source screen |
| Matched post-measurement generation | 19 / 27 | timing only; not sampling-unit alignment |
| Source papers surviving strict direct-function criterion | **0 / 2** | this is a **measurement/admissibility result**, not evidence of absent recovery |

**Decision: STOP before computing a new Clarke `ΔHe→F_direct` meta-analysis.** The existing original dataset was designed for genetic state and population-level fitness, and re-estimating its already-published positive regression would not answer the new question or be novel. This STOP applies **to the original Clarke aggregate dataset**, not to independent functional plant studies with their own molecular data.

## Next data stream — direct gene-flow/mate function in flowering plants

Conduct a distinct **plant controlled-pollination/functional-genetic source screen**, not a retroactive recoding of Clarke rows. A strong initial candidate is Castilla et al. (2019), *Pyrus bourgaeana*, 6 crossing treatments, genetic kinship from microsatellites, fruit/seed/germination endpoints, public source workbook at Dryad [10.5061/dryad.6t72p3j](https://doi.org/10.5061/dryad.6t72p3j). Confirm independent tree/population/cohort units, original treatment codes, and endpoint denominators before fitting any effects.

The 2021 clonal self-incompatible-plant genetic rescue cross experiment, 2025/2026 related *Pseudoziziphus celata* parentage translocation programme, and 2025/2026 `Lupinus angustifolius` assisted gene-flow lineage must be **linked as potentially dependent studies within each shared system**, not counted as independent source programmes without verification.
