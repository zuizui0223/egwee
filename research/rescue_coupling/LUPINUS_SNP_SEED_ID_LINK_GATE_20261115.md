# Lupinus public molecular-versus-reproduction linkage gate — 2026-11-15

**Decision:** `ID_LINKAGE_REQUIRES_SOURCE_CROSSWALK`. This is a **negative identifier-matching result**, not a negative biological rescue effect. The phenotype and genomic files exist, but same-individual genotype and reproductive response **cannot yet be joined directly**.

Published source programme: `Lupinus angustifolius` assisted gene flow in Spain, Figshare https://doi.org/10.6084/m9.figshare.28304024; see source-backed candidate RC004 in `plant_primary_candidate_registry_v1.json`.

**Automated first-pass trial:** GitHub Actions [run 43681874852](https://github.com/zuizui0223/egwee/actions/runs/43681874852), artifact [14147854782](https://github.com/zuizui0223/egwee/actions/runs/43681874852/artifacts/14147854782), script `audit_lupinus_id_linkage.py`. Source files pinned by SHA-256:
- phenotype workbook `data_Lupinusangustifolius_geneflow.xlsx`: `c8033a1eee55663549e42c22264b830461db320f4f3209718df10b3f4a67df10`
- genomic sample-metadata `Metadata_VCF_SNPs_geneflow_Lupinus.xlsx`: `fed6babc38ed6ffcde49fcbc92489047fdd730d0fa277654d181c13f741380e8`

**Source identifier denominators (only identifiers/group labels read):**
- Phenotype rows excluding worksheet header: **1,776**, all with nonempty `id`
- Distinct phenotype `id` values: **1,598**; **178 repeated IDs**; these are not 1,776 independent plants. Repeats may be times/families/duplicated entries, not interpreted without source documentation
- Genomic sample metadata rows: **11**, with **11 unique `Sample(s)`** strings
- Exact case-folded/whitespace-normalized overlap between phenotype `id` and SNP sample `Sample(s)`: **0 / 11**
- The phenotype data also include `genotype`, `population`, `line`, `sister`, `year` group fields and outcome column headers `number_of_seeds`, `seed_weight`, `flowering_onset`, `shoot_growth`
- **No seed values, growth effect sizes, fitness signs, VCF variant calls or model outcome data read.**

**Next admissibility gate:** recover publication-author source sample correspondence between genomic `Sample(s)` entries and phenotype `line` / `genotype` / `id` / `year`. The direct 0/11 identifier result alone **does not** prove there is no biological link; marker samples may represent a subset/parent line and require an explicit genotype- or pedigree-level mapping. Never invent this link by fuzzy matching or claim a SNP→seed-output result until tested.

Only after a documented crosswalk may one predeclare independent family/line blocks, control group, generations, functional seed endpoint, and missingness; then generate signed effects under a reproducible model. Distinct `F1`/`F2` lineage labels can be repeated across individuals or generations and cannot be treated as new independent programmes.

**Scientific limit:** the public file set has verified molecular and seed-related data, but **joint individual-level empirical genotype–function analyses remain unverified**. This should not be hidden in a pooled genomic rescue result.
