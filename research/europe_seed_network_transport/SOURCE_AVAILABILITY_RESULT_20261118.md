# Zenodo v2 seed-network source availability — verified gate result (2026-11-18)

## Outcome: METADATA_ONLY_SOURCE_STOP — zero ecological effects

The source-locked plan \`PROTOCOL_SOURCE_FREEZE_20261118.md\` tested official Zenodo record \`20284225\`, DOI \`10.5281/zenodo.20284225\` (2026-05-19, version 2), before reading any seed counts or network values. An independent published-version metadata-only probe queried API records \`20284225\` (v2), \`18376300\` (v1) and concept \`18376299\` (redirects to latest v2).

On the official live Zenodo \`/api/records/{id}\` endpoint, **both v1 and v2 expose an empty \`files: []\` array (0 attached files)**. The concept record resolves to v2, also 0 files. The API reports DOI and concepts normally, so this is *not* a network/HTTP 401 failure or a guessed filename. Neither required original file \`data_sem.csv\` nor \`seedset_data.csv\` is present as an official downloadable attachment in the API manifests.

- Metadata probe run: https://github.com/zuizui0223/egwee/actions/runs/44221626457
- Source gate status: \`ACCESS_OR_SCHEMA_STOP\` with reason \`SOURCE_STOP: required original file absent: data_sem.csv; source keys=[]\`
- Original-source biological values accessed: **none**
- Native source study×site join established: **none**
- Seed effect or held-out predictive test estimated: **none**
- Raw third-party files redistributed: **none**

**Interpretation:** Public discovery records and mirrored abstracts describe a dataset with 2 seed-producing study programmes / 8 plant species and file names, but the official Zenodo version manifests in this environment have zero attached original files. Therefore the described seed records are **not verified usable original observations** through this record's API. Do NOT assume they exist, infer that all data are private, alter thresholds, or assign a biological null. Only reopen the downstream source-based prediction protocol if an author-authorized versioned file or primary repository path with matched data is recovered.

This does not alter source-verified empirical egwee fragmentation meta, PoMS, Leavenworthia source audits, or theory egwe. Because the gate stopped before data access, this branch is a reproducibility/discovery outcome, **not** a paper result.
