# 2026 Lupinus field original-data source and design receipt — 2026-11-22

**Executed source-only receipt; no numerical phenotype/genotype effects, seed response signs, out-of-sample model scores or natural G×I×F validation.**

## Actual GitHub-run evidence

- Successful source-gate workflow: [Run 45032081434](https://github.com/zuizui0223/egwee/actions/runs/45032081434), [artifact 14758441208](https://github.com/zuizui0223/egwee/actions/runs/45032081434/artifacts/14758441208), ZIP SHA256 `a018c9c54cf6841e368290ff3d5f4c96642ae96e3209135fa89834853569e914`.
- **10/10 synthetic source/identifier safety tests passed**.
- 2026 field Figshare [10.6084/m9.figshare.29606180.v1](https://doi.org/10.6084/m9.figshare.29606180.v1): official metadata retrieved and one original `Lupinus_angustifolius_data_field.xlsx` fetched in runner. Raw XLSX remained in runner memory, was not committed or redistributed.
- Original source data worksheet: **3,025 physical rows including one header; 3,024 study-design records**. Columns verified by header: `id`, `genotype`, `population`, `line`, `flowering_onset`, `number_of_seeds`, `shoot_growth`. Presence of a column does **not** establish valid nonmissing seed observations or viable recruits.
- Observed categorical source-level denominators (no phenotype inspected): `population`: FRO **1,584**, PIC **1,440**; `line`: C **720**, J **648**, L **720**, R **144**, T **720**, X **72**. **84 distinct source genotype labels**, not necessarily 84 sequenced genotypes. Code labels have **not** been mapped to biological treatments by a verified source codebook; do not name a line AGF or control based on letter alone.
- 2025 common-garden 2025 publication original phenotype source `data_Lupinusangustifolius_geneflow.xlsx`: **1,776 records** (original Figshare [28304024](https://doi.org/10.6084/m9.figshare.28304024)).
- Direct cross-year structural audit: **0 exact interannual ID labels**, **0 exact population×line category overlaps** after case/whitespace normalization. This is a **source-label mismatch / unresolved pedigree crosswalk**, *not evidence that the original experimental lineages are biologically unrelated*. There is no valid individual-by-individual 2025–2026 join by raw label.
- 2025 source's marker genotype column is not demonstrated to be 2026 individuals' DNA calls. There is **no same-mother genotype×effective pollen×direct field viable recruit panel**, and **no extra independent original experimental programme**.

## Literature-level biological results (authors', not newly calculated)

- Sacristán-Bajo et al. 2025 *Evolutionary Applications* DOI **10.1111/eva.70087**: assisted gene flow from southern donor pollen to northern controls generated earlier flowering across derived lines; F1 heavier seed and reduced shoot growth; 36 candidate outlier SNPs associated with trait differentiation in sampled material. Original study analyses already exist.
- Sacristán-Bajo et al. 2026 *Annals of Botany* DOI **10.1093/aob/mcag061**: F3 offspring placed in an in-situ field environment retained earlier flowering and reduced shoot growth relative to controls; artificial selection contrasts did not reproduce the same clear earlier trait signal under the field condition. This is **published cross-generation trait transport** rather than an independent species-level replication.
- Source XLSX `number_of_seeds` is potentially an offspring production proxy, but **exact counting method, completeness, observation denominator, line code dictionary and original comparator are not yet frozen**. Do not call it measured ecologically mediated successful mating or established seedling recruitment.

## Fixed interpretation and stop rule

1. Dataset counts >3,000 are **not** 3,000 independent populations; two northern founder populations (FRO/PIC) and repeated line/genotype families form a deeply nested experimental programme.
2. Do not infer C/J/L/R/T/X treatments from letter names. Obtain original 2026 source codebook/figure/crossing design mapping and any year/family provenance first.
3. Do not match 2025 and 2026 by row order, approximate case, swapped codes, within-population rank or genotype numeric resemblance; same letter/ID also would not prove the same individual across F1 vs F3.
4. Before looking at `number_of_seeds`, freeze the source-defined reproduction measurement (observed/estimated, zero/missing), experimental blocks/years, control vs assisted origin and independent family/pedigree grouping; reserve the single 2026 field experiment for its proper inferential level.
5. Any future within-programme line contrast is **W_reproductive_proxy** (not genetic-compatibility **G_mate** or partner-mediated **F_direct**), and authors already reported the main phenology result. There is no support for a G×I×F natural validation or numerical conservation threshold here.

## Access diagnostic correction

[Official Dryad API accounts documentation](https://github.com/datadryad/dryad-app/blob/main/documentation/apis/api_accounts.md) confirms certain file download calls require an API bearer token. Prior HTTP 401 was an authentication gate rather than evidence no original exists. Repeated anonymous Dryad calls were removed from this PR's CI. The source-only Figshare read was a separate public provenance route.

**Decision:** `FIELD_SEED_COLUMN_PRESENT_BUT_LINE_SEMANTICS_AND_PEDIGREE_UNRESOLVED`. Treat as a high-quality **prospective phenotype–reproduction feasibility candidate**, not a new affirmative eco-genetic-function effect.

## Follow-up codebook audit — run 45032319827

- A new **text-only** audit examined the seven physical rows of the original `Lupinus_angustifolius_data_field.xlsx` first worksheet. It read no numeric outcome/genotype values.
- Result: `NO_VERIFIED_CODEBOOK_IN_SOURCE_SHEET1`; recognized C/J/L/R/T/X treatment-code definitions **0**. This is a stop on **verified one-letter code → biological treatment mapping**, *not proof that no mapping exists in the published supplementary methods or author's dictionary*.
- GitHub Actions [run 45032319827](https://github.com/zuizui0223/egwee/actions/runs/45032319827) succeeded and 10/10 synthetic source/ID tests passed. Codebook retrieval cannot convert the letter codes into source-defined CFL/GFL/EFL/OUT without external evidence.
- The 2026 OUP public abstract confirms the experiment had controls, artificial-selection lines (selfing and outcrossing), and assisted gene flow lines propagated to F3, **but does not identify which one-letter Excel source codes correspond to these arms**. See DOI 10.1093/aob/mcag061 (2026-03-26).
- **Decision: SOURCE_CODEBOOK_STOP_BEFORE_SEED_EFFECT.** No regression on `number_of_seeds`, no inferred family/pedigree links, no new causal reproductive rescue claims. Continue only if a primary codebook or correspondingly documented treatment crosswalk is recovered; then freeze source-defined controls, missing/zero outcome, cohort nesting and holdout before opening signed seed values.
