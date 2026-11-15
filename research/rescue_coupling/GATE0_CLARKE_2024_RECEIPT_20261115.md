# Public-source Gate 0/1 receipt — genomic improvement versus ecological-function recovery
## Clarke et al. 2024, audited 2026-11-15 without inspecting outcome direction

**Status: source-pinned, category-only evidence audit; no new estimate of rescue effect sizes.**

### Exact provenance

- Publication: Clarke JG, Smith AC, Cullingham CI (2024), *Molecular Ecology* 33:e17532, DOI https://doi.org/10.1111/mec.17532. The original article expressly considers **animal taxa**.
- Published dataset: https://doi.org/10.5683/SP3/9VKJI6.
- Original analysis source: https://github.com/AdamCSmithCWS/Genetic_rescue_meta pinned commit `61c59003a66580f5ba090de46dd8614008373cb7` and file `He_dGR.xlsx` pinned Git blob SHA-1 `546c93f67ffd67a8776f9a12cfe85af2dd42633d`.
- Exact original XLSX SHA-256: `cd95a8aa42beabd4f34650e1e782a03919621b0a2a53e6b4f027fd43d086d5ae`.
- Reproduction: GitHub Actions [run 43680981170](https://github.com/zuizui0223/egwee/actions/runs/43680981170) SUCCESS; category-only JSON artifact [14147134980](https://github.com/zuizui0223/egwee/actions/runs/43680981170/artifacts/14147134980). The author workbook itself was read in CI and **not redistributed or committed**.
- The frozen endpoint ontology is `CLARKE_ENDPOINT_CODEBOOK_20261115.json`; it was committed before looking at pre/post genetic/fitness values.

### Actual discovery denominator

| Source observation category | Source code | Paired source rows | Eligible as direct ecological-function recovery now? |
|---|---|---:|---|
| Population size | `PS` | **20** | No; demographic abundance `D` |
| Survival rate | `SR` | **4** | No; general fitness `W_survival` |
| Individual reproductive success | `IR` | **3** | **Not yet**; `W_reproductive_success`, must inspect original endpoint and source intervention |
| **Total complete** | | **27** | **0 verified directly ecological-function outcomes** from aggregate labels |

The **27 rows are nested in 19 independent source studies**, not 27 independent experimental systems. All 27 rows contain paired pre/post expected heterozygosity and fitness fields as required by the author's original analysis slice. However, only **19 rows** measure genetic and reported fitness post-states in the **same recorded generation**; **8 rows** measure them in **different generations**. Matching generation labels is necessary but not enough to establish synchronized ecological/trait/interaction measurement.

The three `IR` rows come from just **two original study labels**:

1. `Arrendal (2004)` (**two rows**), DOI https://doi.org/10.1023/B:COGE.0000014059.49606.dd: *Genetic evaluation of an otter translocation program*; microsatellite/mitochondrial evaluation of Swedish *Lutra lutra* reintroductions. The published abstract uses population growth/translocation success, not a reported pollinator/partner-mediated direct function. Whether the original data support the `IR` coding/functional response is **unverified** by the aggregate workbook.
2. `Gustafson (2017)` (**one row**), DOI https://doi.org/10.1098/rsos.170115: *A single migrant enhances the genetic diversity of an inbred puma population*. A genetic-management/offspring study in pumas; its `IR` field does not itself confirm an ecosystem-mediated ecological function.

The `Class` values in the workbook are numeric (`1`–`4`); they are not promoted to taxon labels without the source codebook. Source paper states animals and a mammal-heavy dataset. Thus **this aggregate published workbook is not a direct plant pollination-function dataset**.

### What can/cannot be said

**Confirmed:** a tractable, exact-source genomic diversity / general fitness dataset exists, with 19 studies, 27 source rows, and marked taxonomic/outcome/timing limitations.

**Not confirmed:** “ecological-function recovery fails despite genetic rescue”; no F endpoint has yet passed the source-measurement gate. An absence of a verified F column in this summary is **not** evidence of no ecological recovery in individual ecosystems.

**Not new:** Clarke et al. already reported mean pre/post genetic and general-fitness improvements and observed counterexamples where heterozygosity increased but fitness declined. Do not republish their association as a novel discovery.

**Decision:** stop a naïve 27-row pooled `ΔH_E → F_direct` analysis. Recover genuinely function-linked plant experiments and distinguish within-population, cross-population, habitat and demographic controls before extracting effects. Keep the author dataset as a **coverage/denominator audit** and possible background on general genetic rescue, not a surrogate direct ecosystem-function measure.

### Reproducibility and non-inference

This receipt uses recorded study names and endpoint labels only; no `Pre_He`, `Post_He`, `Pre_fit` or `Post_fit` values, derived log-response ratios, outcome signs, or effect-size estimates were used. The source code `research/rescue_coupling/audit_clarke_schema.py` enforces the pinned blob and `classify_clarke_endpoints.py` maps a predeclared endpoint ontology to each category. A new direct-function meta-analysis requires its own eligible denominator, independent source units and source-specific contrasts.
