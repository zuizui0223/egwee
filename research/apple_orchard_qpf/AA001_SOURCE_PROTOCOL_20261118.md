# AA001 — prospective original-source apple Q→germinated-P→fruit-F orchard grain audit

**Created 2026-11-18 before accessing source row-level values.** Empirical egwee, not theoretical egwe, and independent of the published CropPol and EuPPollNet source frames. This is an **original-source grain/coverage experiment**, not a confirmatory hypothesis about why bee visitation or crop yields differ across regions.

## Fixed original source and ecology

Riva et al. (2026), *Climate impacts apple pollination, yield and economic outcomes of farmers*, *Science of the Total Environment* 1029:181767, [10.1016/j.scitotenv.2026.181767](https://doi.org/10.1016/j.scitotenv.2026.181767). Published original dataset [Zenodo 10.5281/zenodo.19403906](https://doi.org/10.5281/zenodo.19403906), record ID **19403906**, CC/public original author license subject to record verification. Four original listed text files: `TransectIN.txt`, `GerminatedPollen.txt`, `initial_final_fruitset.txt`, `apple_weight.txt`. Use the official Zenodo API-advertised **file-content links**, never undocumented guessed file IDs, shadow mirrors, altered observations or substituted aggregate published plots.

The paper describes **33 apple orchards** spanning Europe and North Africa, standardized pollinator observations in 2022 and 2023, and treatments E = pollinator exclusion, O = natural open, OH = open plus hand-pollen supplementation. Pollen tubes/germinated pollen were assessed **in 2023 only**, with sampled floral styles removed for chemical/microscopy preparation. Apple fruit set and weight were recorded on other experimental plant material with source-defined orchard/tree/inflorescence nesting. Thus any admissible three-layer grouping is at best **same orchard×2023×treatment**, with P and F on distinct flowers. This is NOT a new third same-flower or same-mother complete Q–P–F programme like QPF001 or 2016 QPF004.

The existing six-source natural QPF atlas has **two** source-audited complete same-ramet/flower systems (Oenothera QPF001, Mertensia QPF004) and is **not expanded** by AA001. Source methods already analyzed how climate conditions flower visits, pollen germination and fruit formation. Repeating this established association is not a novel ecological result.

## Pre-outcome source execution

### Gate A: metadata and file schema only

- Read official public Zenodo `https://zenodo.org/api/records/19403906`, validate record numeric ID and `doi=10.5281/zenodo.19403906`, active published status.
- Follow **only** the exact four filenames above and each source-advertised HTTPS `content` link; verify original file size, md5 or sha256 digest when supplied, and record UTF-8/Latin1 lossless header, delimited row counts and SHA256. Total original file size expected approximately 135.5kB; enforce <512kB per source. Header and counts are structural, not biological outcomes.
- Never commit, upload or print original numeric site, fruit, pollen, visitors, field row, filenames with personal ID or place coordinates. Retain filenames, checksums, header labels/lengths, row counts and source API status only.
- If any source returns HTTP403/401/429 or any checksum mismatch, fail closed as `SOURCE_ACCESS_STOP`; do not assume private data or biological zero.

### Gate B: biological key and independent-unit audit, not signed results

After successful Gate A, before testing any effects:

- Derive normalized keys from actual source-defined fields. Explicitly differentiate `Region`, `Site`, `Plot`, `Inflo_ID`, `Treatment`, `Year`; no guessing that Site IDs are globally unique across regions or years.
- Match Q visitor transects only to the same original `Region×Site×year` orchard as P/F. P implicitly year 2023 ONLY if original source codebook confirms this; never fabricate one missing treatment/year or assume 2022 P=2023 P. Fruit F must have same treatment label (E/O/OH) and orchard/year; Q is site-level unmanipulated monitoring, not direct visitation to particular E/OH flowers.
- Preserve `Treatment` as experimental manipulation and separate from realized germinated P. P samples are destructive; NEVER join on `Inflo_ID` to a fruit from another cohort simply because numeric ID repeats.
- Count eligible original orchard-year sites, treatment cells and original regions with Q-P-F site-level observational support and source effort denominator; record overlap and any source loss. Plant/inflorescence rows remain nested, not independent landscapes.

### Gate C: only with viable coverage, later preregistered outcome test

If actual source support includes at least **12 unique orchard×2023** Q/P/F overlaps across at least **3 regions**, with known O/E/OH experimental assignment and comparable fruit denominator, freeze a **new treatment-stratified, whole-orchard heldout** predictive target, taking climate and experimental site/region into account BEFORE opening P–F effect signs. Retain separately any Q→P and P→F analyses to avoid inter-treatment spillover. If undercovered, `SOURCE_COHORT_COVERAGE_STOP` without refitting.

No pooled global Q→P→F individual mediation can be inferred from orchard averages; at most a **contextual orchid-level** source sensitivity. The original authors' claim that warm regions differ in pollination services and possible wind adaptation is already published; do not restate as novel. Any new interpretable result must be an independently held-out *conditional information increment* with uncertainty and correct source biological units.

## Reproduction and scientific firewall

Stage A script+workflow must be source-exact and outcome-blind. Subsequent stages may only use frozen post-A biological rules and be tracked as later commits. Original raw paper files live at Zenodo, never in egwee GitHub, GitHub artifacts or output logs. Save only machine-readable source manifests and aggregate gates. No edits to main fragmentation five-cluster effects, PR #52, #63, #72/#74, CropPol PR #78, the natural strict QPF two-source count, submission-ready flags, or theoretical egwe.
