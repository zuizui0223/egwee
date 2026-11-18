# EGWEE: European site-level network -> wild-plant seed-setting transport feasibility
Protocol lock: 2026-11-18 (before opening any original seed/numerator/network predictor values)
Status: OUTCOME-BLIND DESIGN / DATABASE SOURCE GATE; draft research track
Branch: analysis/europe-seed-network-transport-20261118

## Biological question

Do metrics of a locally assembled *wild pollinator* visitation network predict *held-out-site* seed-fertilization success of wild plant species, beyond species-specific average fecundity? How far can interactions (I) be transported to reproductive function (F) when actual pollen compatibility (P) and same-species visits are not observed?

This is an independent empirical macroecology feasibility programme, not theoretical egwe, not the existing five-cluster Hedges-g meta, not the PoMS FIT/pan methodological pilot and not the Leavenworthia one-programme plant-level assay.

## Preregistered source target and provenance gates

- Data publication: "Direct and indirect effects of local habitat quality, landscape use intensity and honeybees on plant-pollinator network functioning and robustness across Europe", Zenodo **record 20284225** (version 2, 2026-05-19), DOI https://doi.org/10.5281/zenodo.20284225; CC BY 4.0 (attribute source authors in any derivative/report).
- Official API metadata: https://zenodo.org/api/records/20284225. For files, use ONLY API-supplied URLs and compare content to API-supplied file digest (MD5 if listed); additionally pin SHA256 of downloaded bytes in derivative provenance. No arbitrary endpoint synthesis, PDF table scraping or raw third-party data redistribution.
- Only \`seedset_data.csv\`, \`data_sem.csv\`, and \`Overview_data_sets.xlsx\` are on the initial source whitelist. The schema/row-count gate will only inspect inventory, filenames, hashes, headers, physical record counts, and maybe whitelisted study/site/species keys (in a later identity gate), **not** seed outcomes or predictor directions.
- Source description: \`seedset_data.csv\` has fertilized/unfertilized seed counts (outcome), \`mean_PSI.log\` (derived network pollination service index), \`fc_HL_z.sc\` (null-standardized wild pollinator functional complementarity), Study_id, Site_id, Species_long. \`data_sem.csv\` has study+site-level network metrics; linked sources are nested in **only two original studies**, even though seed values involve **eight plant species** (nine plus several 3–6-site species). The eight species are *not eight independent studies*.
- Sampling class: native same-site pooled community network + wild-plant seed set. **Not** direct genetically compatible pollen receipt; not a natural I→P→F path. Derived PSI is a constructed index; do not describe it as plant-specific raw visit frequency. The source authors already developed/tested network-function relationships, so reproducing their in-sample coefficients is not independent discovery.
- The corrected 2025 EuPPollNet database https://doi.org/10.1111/geb.70054 reports **623,476 records** (vs originally 1,162,109), 1,864 networks, 52 studies. It is a separate candidate network database and shares source studies with other compilations. Do not treat it as 52 independent seed-function programmes; avoid using the superseded uncorrected record total.

## Stage A: accessibility + structure (execute first, no outcomes)

Fetch official Zenodo version metadata, file manifests, source checksums, source headers and row counts on bounded downloads (max 64 MiB per file). Audit duplicate columns, empty/invalid headers, CSV format. Explicit error status \`ACCESS_STOP\` or \`SCHEMA_STOP\` instead of inventing data. Strict unit semantics and unique Study_id/Site_id keys then receive a separate stage B gate.

## Stage B: freeze source-identifiable prediction target BEFORE signed outcome values

Only proceed if both tabular files are available, all expected column names and exact study/site identity pairing pass, original seed count values are nonmissing nonnegative integers with positive denominators, and >=2 independent studies each have >=5 distinct source site IDs and >1 observed species/site. If these structural conditions fail, publish the coverage result and stop; do NOT lower thresholds to chase sign.

If identifiers and coverage pass, fix species and study nesting and the following **descriptive predictive target**:
- Response per individual flower/head/plant row: \`fertilized/(fertilized+unfertilized)\` with count denominator. If fertilized/unfertilized are already site-aggregated, use their native unit without pseudo-replication, and carry provenance explicitly.
- One grouped holdout fold per **whole site**, all species and replicate plants at a site held together. Exclude a fold from prediction when a species in its test fold has no occurrence in any training site, and report this proportion. Site is smallest credible geographic independence unit. No random row-level splitting.
- M0: within-study, within-species intercept-only training mean (regularized with a fixed Beta(0.5,0.5) pseudo-count) learned from other sites. M1: add standardized \`mean_PSI.log\` as a single shared logit-slope trained on the same training sites (species fixed effects, unpenalized or a fixed ridge penalty=1; choose and lock after headers, before outcome signs). Do not use seedset row duplicates of \`mean_PSI.log\` as independent network replication.
- M2 (secondary, only if complete): include \`fc_HL_z.sc\` beyond M1, with source-null-standardized network functional complementarity. Fit predictors with training-fold-only mean/std, not full-sample scaling. Report prediction log loss per held-out seed (descriptive and also equal-site average), and whether gains are coherent in each of the **two study** strata; do not call site/nested plants independent studies.
- Main comparison \`gain = heldout logloss(M0) - heldout logloss(M1)\`; positive is improved prediction. Conditional positive here would be evidence only of within-programme site transfer; *cross-study* generality cannot be established with two different species communities, and no genetic rescue/compatible pollen effect can be inferred. Require both studies to have positive gain to call directional consistency; no retrofitted effect significance. If prerequisite fails report \`NOT_IDENTIFIABLE\`.
- Hold source measurements to their original ecological sampling frame; if seed+network programme key pairing cannot be proven, stop before model estimation.
- Cross-validation of a predictor defined partly by seed set, or outcome leakage through pre-constructed variables, is prohibited. Verify PSI is assembled **only from visitation networks**, without any fertilized/unfertilized seed data used to compute it.

## Planned model/paper boundaries

Existing 2026 compilation already measures seed set and pollinator network indices at some of the same sites. The potentially new estimand is held-out-site predictive **transport**, with strict nesting/independence and comparison to a species-only baseline. Still a secondary pilot until more independent source programmes are found.

Require exact source version, attribution, scripts, CI, independent site bootstrap or site-level confidence description and explicit prediction denominator. No claims of causal functional transfer, generalized pollination services, gene-mediated partner compatibility or support for the egwe model without direct evidence.

This protocol was recorded before any signed seed outcomes or predictor values of this data publication were opened in this branch.
