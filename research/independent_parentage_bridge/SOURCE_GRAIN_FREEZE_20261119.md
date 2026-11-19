# EGWEE: independent paternal opportunity source cohort and biological grain lock

**19 November 2026, empirical `egwee` only. Created BEFORE downloading or analyzing original individual-level paternity/outcome values in these candidate programmes.** This is a structural source audit followed, only if possible, by separately frozen empirical tests. The positive Barbot et al. 2026 contact–paternity conditional-marginal effect in draft PR #90 remains unchanged and is NOT treated as cross-study replicated here.

## Source LVP001 — Leventhal et al. (2026), Brassica rapa

Original article *Longitudinal and cross-sectional selection on flowering traits in a self-incompatible annual*, Evolution 80:1217–1229, DOI [10.1093/evolut/qpag047](https://doi.org/10.1093/evolut/qpag047); author Dryad repository [10.5061/dryad.tdz08kqdr](https://doi.org/10.5061/dryad.tdz08kqdr). Exact advertised original **`Leventhal_et_al_2026.zip`** (~1.67 MB) and `README.md` (~62KB), exclusively via official authenticated-free public Dryad API metadata URL and its advertised file download relations. The nested original files are identified by the author README (not invented); whitelist:

- Original `data-raw/` daily flower counts: `b30phenZerosJune7-2013.csv`, `compphenZerosJune7-2013.csv`, `fwphenZerosJune7-2013.csv`, `tkphenZerosJune7-2013.csv`;
- `data-raw/clump_coord.csv` and `data-raw/even_coord.csv` donor position and experimental geometry;
- `data/pedigree_assignment/pedigee_bZ_[pop].csv` 4 original population-specific full-season paternity assignments (note source README lists Comp/Fwest/Track but not B30 in one index; no fabricated fourth name);
- `data-raw/PollinatorVisitationDatafiles/PollinatorObservation_Comp&B30_editedForTimeSlices2.csv`, `PollinatorObservation_FarWest&Track_editedForTimeSlices2.csv` (observational sample likely aggregate by plot/date, **not confirmed plant→plant partner movement**);
- Author helper and genotype/phenotype files are *separate source-derived tiers*, not assumed original empirical raw individual pollen observations.

Original paper reports **854 original donor plants**, **180 maternal male-sterile gene-trap plants**, **1,970 genotyped offspring** in **4 experimental populations** from one broad study, with B30 (even), Comp (clumped), Track (even), Fwest (clumped), 2 observation seasons. Data originally collected in 2011, published 2026. Parentage from MasterBayes probabilistic assignment; some files are author-derived maximum posterior identities; do not promote `prob` below a selected threshold to true zero. Four experimental populations are not 4 independent studies.

### Stage A source-only receipt

Read official Dryad public `/api/v2/datasets/doi%3A10.5061%2Fdryad.tdz08kqdr`, version and file inventory from **advertised** `_links` only. Exact `identifier=doi:10.5061/dryad.tdz08kqdr`; check original SHA256 and advertised digest when possible. Read ZIP **metadata and first-row original CSV header only**, not individual father assignments, flowering values, genotype cells or field visit counts; for the nine to thirteen explicitly identified files, retain entry name, compressed/uncompressed size, SHA256 only if exact trusted source bytes, declared original filename, parsed header labels and physical CSV row counts, and whether a source-coded mother ID, father ID, flower-time and plant-level visitation key exist. ZIP entry path names may have a fixed author container root; strip that prefix only by matching exact suffix, never manufacture field names. Do not log any original per-plant ID or outcome values. If Dryad metadata success but file download 401/403/429, code stops **`PUBLIC_ORIGINAL_SOURCE_ACCESS_STOP`**; this is not a biological null, not a paper-availability judgement, and does not permit scraping alternative unverified mirrors.

### Stage B hypothetical biological opportunity test (not yet authorized)

Only after source file bytes and original key/header verification: freeze actual biological join for male donor ID, maternal gene trap batch/time and original paternity `P.1/P.2/P.3/prob`, source-specific positional coords and source original 2–3-day open-flower observations. Proposed independent *information-sufficiency* question: does measured source donor–recipient **flowering opportunity overlap**, beyond source pollination distance and source donor fecundity, improve predicting MasterBayes-assigned paternal success across heldout maternal gene-trap batches or populations? This is NOT the same as directly observed floral contact in PR #90. **Do not implement or claim this association until source-only join succeeds**, as the original paper already reported spatial/time mating patterns and selection on flowering time.

Eligibility requires ≥3 original populations with ≥50 source-assigned offspring each, source-transparent male/recipient/batch IDs, original phenology matched to donor ID for ≥80% of original assigned sire records, confirmed gene trap batch windows and ≥12 gene-trap batches that support original parentage. Whole-batch and whole-population prediction should be separate, no treating 1,970 offspring as independent field programmes. Missing paternity IDs not imputed.

## Source RHP001 — Rhodes et al. (2017), Oenothera harringtonii

Original article *Pollinator identity and spatial isolation influence multiple paternity in an annual plant*, Molecular Ecology, [10.1111/mec.14115](https://doi.org/10.1111/mec.14115); original Dryad [10.5061/dryad.p24q3](https://doi.org/10.5061/dryad.p24q3), **publisher source-mirrored Zenodo record [4942351](https://zenodo.org/records/4942351)**. Published record explicitly lists original 9 files with source size and MD5: `amPollinators.csv`, `genotypes.xlsx`, `multiplePaternity.csv`, `obs.csv`, `overallPollinators.csv`, `pmPollinators.csv`, `pollenDispersal.csv`, `pollinatorBouts.csv`, `Rhodes et al. 2017.R`. Only official Zenodo API-advertised links; preserve original file MD5, bytes, row counts and first-row labels. XLSX schema only: no original genotype values, parentage rows or individual outcome values accessed in this stage.

Biological key documented by authors: `multiplePaternity.csv` each maternal seed family/fruit with `plantID`, exclusion `treatment`, `isolation20`, `correlatedPaternity`; `pollenDispersal.csv` each seed with treatment and dispersal distance but **does not advertise mother/father IDs**; `pollinatorBouts.csv` each observed visit bout with `time`, `visitor`, `flowersVisited`, and no advertised maternal plant ID. Thus field treatment-level *pollinator-guild opportunity → genetic multiple paternity* can be studied, but **NOT exact donor-to-mother visitation and genetic sire pair contact**, even if all files retrieve. Published paper already reports nearly twice as many paternal donors with hawkmoths and isolation-dependent reductions in multiple paternity. Those are prior art.

### Stage A gate

Retrieve public Zenodo record ID 4942351 metadata and approved listed original nine source file streams, max 256 KB each, check source MD5/SHA256, inspect first-row CSV fields and structural row counts, XLSX file structure and worksheet first-row headers only, not genetic/offspring content; verify whether pollinator bout or visitation table actually contains **individual maternal/paternal site keys**. Full original file bytes are **never** committed or uploaded to EGWEE. Stop when original source checksum missing/mismatched, or 403/401/429, never treat access STOP as absence of biology.

### Joint admission gate, specified upfront

**No direct replication of PR #90** unless at least one fully new source has actual same-session **(motherID,fatherID) observational positive contact** measured or source-estimated with a verified original numerical variable and paternal assignments to matching plant IDs. Aggregated pollinator foraging bouts or co-occurrence based on flowering opportunity are **different estimands** and cannot be meta-averaged with the Barbot fixed-marginal contact-enrichment result.

If source LVP001 has 4 populations and source RHP001 has exclusion treatments, they may support separate new *opportunity/resource-filtering hypotheses* after their own source freeze. Do not count programme/populations as independent published studies. No retrospective cherry-picking of the original paper's known treatment effects, no fictional same-flower QPF stage, no relabeling paternity confidence as compatible stigmatic pollen, no raw rows/genotypes redistributed.

## Existing evidence preserved

The prior PR #90 Barbot source result: 741 outcrossed sampled offspring, observed **92.8475%** positive assumed-carryover-10 contact vs **80.2345%** mother/father-marginal null, +12.6130 pp conditional p=0.00049975; post-outcome deduplicated 303 genetic pairs shows +11.70 pp, and longer carryover assumptions saturate toward zero discrimination. All refer to one original manipulated research programme. The earlier 157-mother stigmatic pollen added no practical genetic mating prediction; the historical original 145 seed endpoint coverage STOP remains.

No edits/merges to main fragmentation synthesis, past PRs #52/#63/#85/#88/#89/#90, other ecology lines, or separate theoretical egwe.
