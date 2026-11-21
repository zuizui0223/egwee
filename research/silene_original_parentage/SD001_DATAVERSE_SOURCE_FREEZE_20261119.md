# SD001 — Silene dioica new original father assignments and measured pollen carryover, source-gate ONLY

**19 November 2026, empirical EGWEE. Frozen before downloading or examining any row-level father, seed, stigmatic-pollen, visitation or genotype values from the new source.** One independent experimental *Silene dioica* programme, not an exact replication of the Barbot *Brassica rapa* contact→assigned-father PR #90.

## Official public original data and provenance

Original experimental data Joffard, Lecat, Ollier, Jolivel, Schmitt, Godé, Barbot, Dufay and De Cauwer (2026), *Experimental manipulation of floral display size does not affect the distribution of paternal diversity in Silene dioica*, public French national repository Recherche Data Gouv, [Dataverse persistent identifier 10.57745/CF1VNW](https://doi.org/10.57745/CF1VNW). Related manuscript preprint DOI [10.1101/2025.07.19.665651](https://doi.org/10.1101/2025.07.19.665651). Original repository states public `paternity_assignment_results.tab` (5 variables and **1,150** genetic seed assignments, with 21 maternal plants) and `pollen_counts_on_stigmas.tab` (4 variables, **186** stigma pollen measures under sequential visits by pollen-carrying bumblebees).

**Both experimental assays are not the same individual flowers.** The pollen-contact assay lets a pollen-laden bumblebee visit 10 sequential female flowers, counting deposited grains, but **stigmas are subsequently collected** and therefore do not generate seed offspring. The paternity assay samples offspring after natural open visitation of distinct 21 experimental maternal plants, some assigned increased floral display. Thus original source cannot establish physical individual-flower Q→P→F or direct original father/recipient contact from its own pollen-count file. The published paper already reports source paternity/mate-diversity outcomes and the measured bumblebee carryover curve as prior art; EGWEE cannot claim their experiments as new discovery.

## Stage-A exact original Dataverse source gate (no biological outcomes)

1. Query only the published original repository API `https://entrepot.recherche.data.gouv.fr/api/datasets/:persistentId/?persistentId=doi:10.57745/CF1VNW`, verify returned persistent ID and latest published dataset version. Retain original publisher metadata, no user authentication. Enumerate the source file records from `data.latestVersion.files[*].dataFile` and source `directoryLabel`, `label`, `dataFile.id` (metadata only).
2. Select only **exact original filenames** `paternity_assignment_results.tab` and `pollen_counts_on_stigmas.tab`, never infer a guessed file ID or use a scraped mirror. Fetch through the official `/api/access/datafile/{file_id}?format=original` endpoint derived from the publisher's file metadata. The source API may return a converted original format; validate returned header, physical row count, source advertised checksum only where that digest unambiguously refers to the retrieved content, source SHA256, MIME, size and response URL; distinguish lossless original format from transformed export. If original API returns a file that is not source-authenticated, STOP rather than treating a mismatched digest as equivalent original data.
3. Inspect **only first-row source column headers** and physical nonempty row count, no biological row cell contents or genetic allele/genotype, maternal or assigned paternal ID, stigma pollen quantity, offspring counts, source per-visit pollen deposition values, sex/pollinator behavior. Expected original source records **1,150** and **186** respectively. No row-level data redistributed or uploaded; GitHub Actions emits only source fingerprint and source-safe schema labels.
4. Exact source biological grain: check whether any publisher original field labels contain `mother`, `father`, `sire`, `offspring`, `plant`, `bout`, `flower`, `sequence`, `order`, `visit`, `pollen` and output boolean presence of potential join key categories. **Do not certify same-flower join from similar names**, or treat 10 consecutive visited stigmas as candidate mothers of genotyped offspring. An explicit source plant ID, plot ID or replicate is not automatically a shared maternal identity across assays.
5. Fail closed on HTTP401/403/429, missing published file, incompatible schema, file size/MD5/SHA256 drift or missing source access; report **source access/identity STOP**, not biological null.

## Conditional next step (requires new freeze after source gate)

If the sequential-pollen source has an independently identifiable **bumblebee bout ID**, an exact **sequential flower position 1–10** and deposited pollen grains, a new independent **pollen carryover function** across bouts can be measured as an original source *different-stage* test (pollen load decay with visitation sequence). The response outcome is measured grains per stigma, not genotype-assigned fathers; use only measured source bouts as independent units, not 186 stigmas as 186 independent insect populations. The original authors likely report that curve already, so any new contribution must use a **frozen transferable calibration / transport test** against a separate dataset and establish independent novelty (or else report simple replication of author work).

If the parentage data separately supply exact maternal plant IDs, assigned source sire IDs and source treatment, a different independent genetic mating-network analysis may be possible, but it must not be joined to the separately excised stigmas. This is **one new original research programme**, not a cross-study direct contact→sire replication. The 1,150 original seed rows are not 1,150 ecological experimental replicates; 21 mothers are the experimental units.

## Strict biological conclusion ceiling

The prior Barbot PR #90 source finding (+12.61 pp under fixed mother/father offspring-marginal null, robust to roster missingness in draft PR #92) remains **one original research programme** for actual same-study directed contact vs assigned sire. Independent Rhodes 2017 wild *Oenothera* source has grouped pollinator exclusion and maternal correlated paternity but no matched individual partner contact, so its mean model +7.49% was statistically uncertain. **Silene 2026 is another separate source for process stages, not an automatic second contact→sire replication.**

Preserve original source intellectual credit, raw data at original repository, no original genotype/visit/individual phenotype rows redistributed, no GitHub `main` or theoretical `egwe` mutations.

## 21 November source-gate correction (after access STOP, before outcome inspection)

The original freeze is retained above. The executed [source audit result](SD001_SOURCE_AUDIT_RESULT_20261121.md)
records the 19 November redirect rejection and the 21 November HTTP 503.
The advertised row counts remain unverified; the published abstract's 1,320
seeds versus 1,150 deposited records also remains unreconciled. Separate
experimental material must not be described as independent-team replication:
Barbot and Dufay/Dufaÿ are authors of both the Silene and Brassica papers.

This amendment changes technical evidence reporting, not a biological model:
source STOP now exits 2 while retaining the derivative receipt; only RELEASED
metadata and a valid publisher MD5 can pass, and saved-original bytes use the
publisher's original-file size rather than an ingested TAB size. No redirect
domain or authentication policy is relaxed. Synthetic regression tests do not
establish availability, biological key identity or source row counts.

