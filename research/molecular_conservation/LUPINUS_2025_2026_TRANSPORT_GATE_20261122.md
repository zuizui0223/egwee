# Lupinus 2025 genomic × 2026 in-situ phenotype conservation bridge — source-gated classification

**2026-11-22. Prospective cross-paper identification gate, NOT a new signed effect or an independent ecological replication.**

## Two real, source-grounded papers from ONE underlying assisted-gene-flow programme

| Component | Original paper | Public data / current status | Endpoint meaning |
|---|---|---|---|
| F1/F2 assisted gene flow and targeted genomic variation | Sacristán-Bajo et al. (2025), *Evolutionary Applications*, DOI **10.1111/eva.70087** | Figshare **10.6084/m9.figshare.28304024**; 2025 original phenotype Excel has `id,genotype,population,line,sister,year,flowering_onset,number_of_seeds,seed_weight,shoot_growth`. Separate raw SNP VCF and sample crosswalk exist. Previous source-only audits done; do NOT presume each phenotype individual has sequenced SNPs. | G_analyzed association with T (flower timing) and W/proxy-seed outcomes in managed common garden. Original publication already reports earlier flowering in AGF lines, 36 outlier SNPs, F1 heavier seeds and less shoot growth; number of seeds did not supply the same clear benefit. Authors' findings, not new independent observations. |
| F3 performance in natural in-situ garden | Sacristán-Bajo et al. (2026), *Annals of Botany* 137:2224–2234, DOI **10.1093/aob/mcag061** | Figshare **10.6084/m9.figshare.29606180.v1** identified from indexed dataset record. New script `audit_lupinus_2026_in_situ_source.py` retrieves official Figshare metadata, authorized published files up to 8 MiB, first-row XLSX headers and row counts only. | Published result: earlier flowering and reduced shoot growth in AGF offspring under in-situ conditions; 2026 study uses F3 progeny from previously generated lines. Artificial-selection phenotype contrast did not transport similarly. This is T transfer to field-like environment, **not demonstration of pollination, mating compatibility, seed/recruitment recovery**. |

Primary evidence:
- 2025 open paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC11885171/
- 2026 paper: https://doi.org/10.1093/aob/mcag061
- 2026 public source: https://doi.org/10.6084/m9.figshare.29606180.v1
- Prior source gate: `research/rescue_coupling/FIGSHARE_MOLECULAR_FUNCTION_GATE0_20261115.md`.

## Pre-outcome no-join and no-duplication rules
1. One biological source experiment programme across 2025 and 2026, not two independent species/population intervention replicates. Different years/environments/offspring generations provide a transport comparison, not additional independent founding populations.
2. The 2025 `genotype` spreadsheet column may label maternal genotype or experimental provenance rather than sequenced functional S alleles; SNP genotype must be verified through original sample-ID crosswalk and ancestry/pedigree.
3. F1/F2 common-garden individuals are **not the same individual observations as F3 in-situ offspring**. Join only by verified family/line/pedigree lineage with documented source-native keys; never join on merely a common population name.
4. First-round Figshare 2026 source audit is **metadata, sheet headings, physical row counts only**. Does not inspect phenotype values, regression signs, positive associations, individual IDs or SNP variants.
5. Report viable seed/recruitment only when directly measured and denominator available. No default imputation of absent seed/offspring data. A measured flowering-time shift is T, not F_direct.
6. Absent natural effective pollinator visit, genetically compatible pollen delivery and F_seed/recruitment in *same maternal cohort*, do **not** fit or claim the EGWE `G×I×F` relational model or an intervention-matching conservation threshold.
7. If 2026 source contains only flowering time and morphological growth endpoints, classify **T_TRANSPORT_PUBLISHED_F_DIRECT_NOT_IDENTIFIABLE**. This is a scientifically informative boundary, not evidence the intervention failed.

## Narrowest publishable implication
Two already published studies of the same assisted-gene-flow programme establish that induced early flowering can persist into a natural-environment F3 observation, while measurable growth consequences remain. They demonstrate **cross-generation trait transport**, not proven restoration of community-mediated ecological function, and may motivate testing temporal partner matching (phenology × pollinator overlap) in a separate prospectively designed field programme.

## Next gate
After an official verified 2026 Figshare source schema receipt, freeze its actual source-defined `line/family/generation/site/year` fields; compare to 2025 phenotype and sequencing sample metadata **without reading response signs**. Only then decide whether there is a legitimate new held-out ecological-function outcome; do not relabel authors' already published F3 trait result as an independent discovery.

## Access correction
Dryad official [API account documentation](https://github.com/datadryad/dryad-app/blob/main/documentation/apis/api_accounts.md) says some file downloads require a bearer token. The repeated official API 401 for *Rutidosis* is an authentication gate; the former anonymous Dryad probe steps have been **removed from the molecular-conservation CI**, and shall not be retried without an authorized token.
