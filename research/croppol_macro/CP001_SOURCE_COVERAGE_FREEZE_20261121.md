# CP001 — CropPol macroecological source-coverage freeze

**21 November 2026. Empirical EGWEE; source structure and coverage only.**
This bounded next task implements the user's standing request to advance broad
public-data ecology. It is a separate visitor-to-production stream. It is not
a direct contact-to-sire replication, a genetic mechanism test, or a change to
the historical fragmentation meta-analysis.

## Question and approaches

The eventual question is whether measured visitor information adds prediction
for genuinely withheld source programmes or crops. The immediate gate establishes
what is jointly observed, at what grain, with what source grouping. Three routes
were considered: another isolated mating-network reanalysis; a literature-level
coefficient synthesis; and a versioned multi-study original-data coverage audit.
The third is selected as an implementation judgment consistent with the user's
public-database priority. This is not an outcome-selected search for a positive
sixth fragmentation cluster.

The original CropPol data paper ([10.1002/ecy.3614](https://doi.org/10.1002/ecy.3614))
and its [v1.1.1 archive](https://doi.org/10.5281/zenodo.5546600) report historical
coverage. [Reilly et al. 2024](https://doi.org/10.1111/geb.13843) already estimates
visitor–yield associations from a filtered 93-study sample. The published
202-study inventory, later 137-study grouping, and 93-study analysis must not
be treated as equivalent denominators. Published outcomes are already known;
no EGWEE raw-data relationship has been examined. Novelty of a future transfer
analysis remains to be assessed.

## Pinned controlling source

- Author repository: `ibartomeus/CropPol`, release `v2.1.0`.
- Release resolved on 21 November to commit
  `febec7dcc088ccf1bd721c41ce8dda87a2dcba1a`.
- Selected file: `Final_Data/CropPol_field_level_data.csv`.
- GitHub-published Git blob SHA1:
  `cd19a354741ac40428e6b94aa1ec2ee596ff0547`; size **2,195,393 bytes**.
- Fetch only the raw file at this exact commit. Verify its Git blob hash
  (`SHA1("blob " + byte_length + NUL + file_bytes)`) and byte length, then
  record a SHA256 of the original bytes. A Git blob SHA is not a plain file SHA1.
- Do not substitute a moving master, another release, mirror, or exported file.
  Source bytes remain transient and are not committed or uploaded as artifacts.
- Schema contract: the author's pinned compilation code lists 68 columns:
  [column order](https://github.com/ibartomeus/CropPol/blob/febec7dcc088ccf1bd721c41ce8dda87a2dcba1a/Final_Data/Supporting_R_scripts/add_dynamic_paper_variables_to_field_data_with_65_variables.R).
  Its exact output header is validated before row processing.

## Permitted stage-A inspection

Read only identifiers needed for within-file key counting, metadata categories,
and cell presence/numeric-syntax indicators. Do not compute means, ranges,
response distributions, correlations, coefficients, effect signs, model scores,
or numeric response-derived eligibility thresholds. No source row, identifier,
contact/email field, coordinates, or response/predictor value is printed or
retained in the derivative output.

Missing tokens are empty/whitespace, `NA`, `NaN`, `N/A`, and `null`
(case insensitive). Numeric zero is observed. Numeric syntax is checked without
using magnitude or sign. Unexpected nonmissing numeric strings are counted as
invalid, never repaired or shown.

Report:
1. File/schema fingerprints and row count.
2. Distinct `study_id`, `study_id2`, study-years, sites, crops and countries;
   missing key counts; duplicate `study_id × site_id × sampling_year` keys;
   whether each study_id maps consistently to study_id2.
3. Presence-only coverage for primary `yield`, secondary `yield2`,
   explicit fruit/seed components, visit fields, abundance fields and richness.
4. Separate joint counts for primary yield plus any recorded visit field, and
   primary yield plus any recorded abundance field, with documented yield units.
   Do not pool these measurement families or call either an admitted analysis.
5. Bounded categorical inventories for `yield_units`,
   `use_visits_or_abundance` and `taxa_recorded`, without row identifiers.
   These describe coding, not biological response relationships.

Counts of study_id2 are **provisional source groups**, not a verified number of
independent studies. The author code attaches this field from an additional
metadata workbook. Repeated years, shared sites/samples and reused synthesis
inputs need provenance reconciliation before source holdouts. Duplicate keys
are reported without dropping, averaging, or treating rows as independent.

## Interpretation ceiling and later gate

A successful stage-A run means original file identity, schema and descriptive
coverage were audited. It does not certify endpoint equivalence, independent
programmes, complete sampling, absence of confounding, causal pollination
benefit, or an analysis-ready pooled sample.

Before any prediction: classify direct reproductive versus agronomic outputs,
exclude visitation-derived pollen scores, distinguish actual visits from netted
abundance, verify source-family grouping, and freeze one baseline and one visitor
extension. Use whole-source holdouts, training-only transformations, and a score
that does not standardize with held-out response means or variances. If units
cannot be harmonized, evaluate a separately frozen within-test-source ranking
rather than mix numerical prediction errors. No model is fitted in this task.

## Source rights and ownership

Record conflicting labels rather than flatten them: the data paper describes
noncommercial CC BY-NC-SA use, older metadata says CC By, and the software
repository displays MIT. This audit redistributes only our code and aggregate
receipts, with original source credit. It makes no blanket MIT claim for raw data.

## Implementation and verification

Files in `research/croppol_macro/`: this contract, a source-only auditor,
synthetic regression tests, and a derivative result/receipt. A dedicated GitHub
workflow runs the tests and source gate, always retaining a receipt; access or
schema STOP is nonzero, never a biological null. Source manifest/hash, missing
versus zero, duplicate keys, provisional grouping, and blocked-access receipt
behavior require independent tests.

Implementation plan:
- [ ] Build an auditor with `inspect_csv(raw: bytes) -> dict`,
  `fetch_verified_source() -> bytes`, and `main() -> int`.
- [ ] Synthetic fixtures test zero versus missing, joint presence by measurement
  family, repeated source groups, duplicate keys, wrong headers/hashes and
  HTTP/timeout receipts. Observe failures before implementation.
- [ ] Run scoped tests, inspect source-safe output and obtain code review.
- [ ] Execute the fixed-source audit once; record exact counts and caveats.
- [ ] Keep a draft PR; no automatic source admission or model execution.

Scientific gate: **COVERAGE_ONLY_NOT_MODEL_ADMISSION** even if transport and
schema verification pass. Preserve `main`, the existing five-cluster evidence,
and theoretical `egwe`.

### Pre-run implementation review rulings

Before original row processing, independent code review identified unrestricted
category strings, incomplete transport-error receipts and discarded identity
evidence on a schema failure. These were reproduced with synthetic fixtures.
Categorical output now uses a bounded, independently specified vocabulary of
standard units and measurement labels; every other nonmissing label is counted
as `<unreviewed_label>` without printing its value. This inventory is deliberately
incomplete and does not decide endpoint eligibility. A populated unit field still
means field presence, not verified unit equivalence.

Request, byte identity and schema stages remain separate; verified byte hashes
are retained even if schema validation stops. The schema fingerprint is SHA256
of UTF-8 comma-joined ordered header names without a trailing newline, expected
`f2ee8b3f934bc412f649022c2349f77df18531842f4810983fa60bc721343866`.
Connection resets and truncated HTTP reads must produce an exit-2 receipt.
Redirect rejection is part of the exact-source contract and occurs before a
redirect is followed. No broader model or raw-data redistribution is authorized.

