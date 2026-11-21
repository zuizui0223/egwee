# SD001 source audit: blocked retrieval, not a biological result

**21 November 2026. Empirical EGWEE; draft source audit only.** The two
original Silene data files have not passed an independent byte/checksum/header
verification. No pollen or paternity effect has been estimated by this audit.

## Executed evidence

| Observation | Source and exact revision | What was established |
|---|---|---|
| 19 November source run | [44547285623](https://github.com/zuizui0223/egwee/actions/runs/44547285623), head `3a892c9ed9a7ef3e820dcaf6a58a22c5a987d219` | Official metadata identified dataset 765421, RELEASED version 1.1, and two expected files. Both file reads stopped because the publisher redirected to a hostname the checker did not permit. |
| 21 November diagnostic push | [44913630072](https://github.com/zuizui0223/egwee/actions/runs/44913630072), head `5337486890f2278594ecc6be104ee57584f007fe` | Official dataset API returned HTTP 503 before file metadata could be revalidated. |
| 21 November diagnostic PR | [44913636276](https://github.com/zuizui0223/egwee/actions/runs/44913636276), same head | Independently executed request also returned HTTP 503. No new file bytes, headers or counts were verified. |

The first artifact was downloaded through the supported GitHub artifact API and
its ZIP SHA256 independently matched
`b6b1f866273825d37552b7042c4dffb442fac6c4a26b28b8c86e05552e186011`.
The diagnostic PR artifact is 14710912167, ZIP SHA256 reported by GitHub
`b849a24972417c656483b0ad27e498ca52ca60b537a0dd739ef96629af1c5b22`.
These are derivative audit receipts, not original biological datasets.

The earlier runs were green because recording a STOP returned exit code zero.
That certified execution of the receipt writer, **not source verification**.
The correction retains a receipt but returns exit code 2 for source STOP; the
workflow uploads the receipt even when this gate fails. No access restriction,
credential requirement or redirect allowlist has been weakened. HTTP 503 is an
observed response, not evidence that the data are private or permanently absent.

## Metadata previously verified, bytes still unverified

| Publisher file label | File ID | Reported ingested TAB bytes | Publisher MD5 field |
|---|---:|---:|---|
| paternity_assignment_results.tab | 765422 | 54,233 | a4ec102260e6e47c552077d615a09bc6 |
| pollen_counts_on_stigmas.tab | 765423 | 4,386 | 381c04ab183cedda09d0b0a3c8a93727 |

These hashes were read from publisher metadata; **neither was verified against
downloaded original data**. The official landing page identifies the saved
original format as CSV. Dataverse distinguishes saved originals from its
ingested TAB representation. The checker now compares an original download to
`originalFileSize` when original-file metadata are present, requires a valid
publisher MD5 before declaring success, and rejects non-RELEASED metadata.
Unknown original sizes and the allowed storage destination still require live
publisher verification after the source is accessible.

## Scientific scope and unresolved source accounting

The [official repository description](https://doi.org/10.57745/CF1VNW)
describes separate experiments: a natural-pollination parentage experiment on
21 mothers (10 display treatments, 11 controls), and a controlled sequential
pollen-deposition experiment whose stigmas were collected. Its advertised
1,150 parentage records and 186 pollen records are not independently recounted
here. Matching row positions or similar identifiers cannot join these assays.

The final [Joffard et al. article](https://doi.org/10.1002/ajb2.70276),
published online 13 October 2026, reports 1,320 seeds in its abstract. The
difference from the repository's advertised 1,150 records is **unreconciled**;
an assignment-failure or exclusion explanation has not been verified. Full
methods would also be needed for assignment thresholds, treatment allocation,
independent bee/bout counts and exclusions.

[Silene's author record](https://pubmed.ncbi.nlm.nih.gov/42866898/) and
[Brassica's author record](https://pubmed.ncbi.nlm.nih.gov/42945307/) share
Estelle Barbot and Mathilde Dufay/Dufaÿ. This is a different species and dataset
with overlapping investigators, not an independent-team replication. The
authors' published diversity and carryover findings remain prior work.

## Verification and disposition

Five offline regression tests were run against the old behavior first, showing
failures for source-STOP exit status, missing MD5, original/TAB size confusion,
and an unreleased version. Independent code review also identified a network
timeout that could escape without a receipt. Two additional regressions
reproduced this in metadata and file access, and bounded TimeoutError handling
was added. The corrected implementation passed all seven tests and the
existing source-safe self-test. These use synthetic fixtures and
**are not empirical source verification**. Current-head live results must be
read from the workflow receipt, not inferred from these tests.

Disposition: **SOURCE_ACCESS_STOP; NO_BIOLOGICAL_EFFECT_ESTIMATED**. Retain this
draft as a bounded source audit. Revisit when the publisher API and a verified
storage route are available; do not repeatedly retry the unchanged outage or
promote this source into the direct contact-to-sire replication denominator.
The next coverage effort should prioritize a public dataset containing several
original research programmes with matched measurement units.

No raw source rows, individual identifiers, genotype records or signed storage
URLs are redistributed. No empirical `main` or theoretical `egwe` changes.

Technical references: [Dataverse original-format access](https://guides.dataverse.org/en/latest/api/dataaccess.html#basic-file-access),
[Dataverse original versus tabular downloads](https://guides.dataverse.org/en/latest/user/find-use-data.html#tabular-data).
