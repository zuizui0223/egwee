# Figshare public molecular-data Gate 0 — 2026-11-15
## Two independent genomic/conservation systems, no signed outcomes inspected

**Status: PUBLIC FILE METADATA + FIRST-ROW SCHEMA VERIFIED, NOT YET SAME-INDIVIDUAL G–F ESTIMAND.**

This source check was executed by GitHub Actions [run 43681713174](https://github.com/zuizui0223/egwee/actions/runs/43681713174), artifact [14148518142](https://github.com/zuizui0223/egwee/actions/runs/43681713174/artifacts/14148518142), in `audit_figshare_schema.py`; raw Figshare files were fetched into the CI runner but **neither redistributed nor committed**, and outcome values/signs and effect sizes were not examined.

### RC003 — Pseudoziziphus celata (genotypes and survival)

Public Figshare archive https://doi.org/10.6084/m9.figshare.30290722 (metadata source version `.v1`).

- `Zc_parentgenotypedata.xlsx` (17,803 B), source file ID `58525309`, verified SHA-256 `8e8e8a1d199ecd2e6fdf67464d7a66b7bfc9bf7aa2ca0a8c5d6771eece692ecd`; its first worksheet has **59 nonempty XML rows**, but it appears to have nonstandard/multilevel headers, so **do not** call 58 rows independent plants or resolve genotype-plant joins from this first row.
- `ziziphus.survival.txt` (54,927 B), source file ID `58525315`, verified SHA-256 `17395280f02a5fb88810555237ae637c993279a23da0bc6179f1233ca5f75b59`; **1,186 physical lines**, named columns `intro_yr`, `intro_type`, `genotype`, `Rgenotype`, `plant_id`, `survival`, `LastLiving`, `living`, `popcode`. A plausible individual/group key is present, but actual uniqueness, repeated observations, missingness and cross-table linkage are **not tested**.
- An external file `Copy of Genodive All Populations.2025` is listed, but is not a verified analyzable genomic table in this audit.

**Decision:** source contains genotype/management/survival data relevant to genetic restoration, but no confirmed directly measured pollination, compatible seed production or interaction-dependent function **in the verified sheet headers**. It **cannot yet** support the proposed `F_direct` or classify genetic rescue as opposed to demographic augmentation. RC002 Gavin-Smyth (2021) may share this Florida ziziphus conservation programme: retain a shared system-level cluster.

### RC004 — Lupinus angustifolius (genomic and reproductive phenotype potential)

Public Figshare archive https://doi.org/10.6084/m9.figshare.28304024 (source version `.v2`).

- `data_Lupinusangustifolius_geneflow.xlsx` (604,154 B), source file ID `52005152`, verified SHA-256 `c8033a1eee55663549e42c22264b830461db320f4f3209718df10b3f4a67df10`. Data worksheet `sheet2.xml` has **1,777 nonempty XML rows** including header (potentially up to 1,776 data rows, not confirmed unique individuals).
- Data headers: `id`, `genotype`, `population`, `line`, `sister`, `year`, `onset_date`, `sowing_date`, `flowering_onset`, `height`, `shoot_growth`, `ldmc`, `sla`, `number_of_seeds`, `seed_weight`, `biomass`.
- Other published files include `variants-gatk_haplotypecaller_SNP_raw.vcf` and `Metadata_VCF_SNPs_geneflow_Lupinus.xlsx`. The latter includes sample/analysis metadata worksheets; **no VCF SNP site calls or signed genetic associations were inspected**.
- Named `number_of_seeds` is a **potentially direct reproductive quantity**, but the source does not yet confirm whether it is complete, viable offspring output or whether the VCF individuals can be joined one-to-one to these `id` values. Cross-treatment contrasts, generation effects and any floral interaction/pollination component are **not yet estimated**.

**Decision:** priority source for separate analysis of genetic provenance vs reproductive phenotype, subject to joining molecular samples, classifying viable reproductive endpoints, retaining family/line/population nesting and explicitly reporting ancestry/environment confounding. RC004 and RC005 are follow-up reports from a shared assisted gene-flow programme, not independent biological replicates.

### Source-design implications and required locks before opening outcomes

1. Define the biological unit `line/population × family × individual × generation` and a versioned sample-ID crosswalk; gene-flow treatment and genotype are not equivalent to an observed realized genetic rescue.
2. Fix outcome categories: `F_reproduction` measured seeds or germination **if viable and source-defined**, `W_general` general survival/growth, `D` population counts, `G_neutral/functional` genome, `I` actual interactions; `number_of_seeds` alone does not establish pollinator service.
3. Freeze missingness rules and independent line-level holdout before testing genotype × treatment effects. No retrospective enrichment of only positive source rows.
4. Audit additional primary plant studies before claiming a meta-analytic common mean or moderator. In the current registry, source metadata **do not yield a confirmatory set of multiple independent complete G+F intervention studies**.
5. The Pyrus Dryad RC001 raw workbook remains `ACCESS_STOP` (HTTP 401 without authorized Dryad API bearer token); do not substitute external source data or infer treatment effects.

**Scientific boundary:** Observing molecular and phenotype column names is real source advancement, not proof that molecular diversity predicts functional recovery, and not a new numerical rescue result.
