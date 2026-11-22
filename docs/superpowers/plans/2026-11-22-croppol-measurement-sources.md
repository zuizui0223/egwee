# CP002 Measurement and Source-Family Audit Implementation Plan
> For agentic workers: use superpowers:executing-plans. Root implements; fresh
> reviewer checks the whole change before original-source execution.

**Goal:** Produce an inspectable aggregate audit of measurement comparability,
source blocking and field-context baseline feasibility.
**Architecture:** Reuse CP001 exact source verification. A separate CP002 module
classifies metadata and constructs in-memory components; only aggregates leave
the process. A dedicated workflow runs scoped regressions and the live audit.
**Tech Stack:** Python 3.11 standard library; GitHub Actions.
**Spec:** research/croppol_macro/CP002_MEASUREMENT_AND_SOURCE_FREEZE_20261122.md

## Global Constraints
- Immutable CP001 source; no biological model or outcome distribution.
- No raw rows, IDs, coordinates, contact information or numeric values in output.
- Scientific status METADATA_AUDITED_NOT_MODEL_ADMISSION even on audit success.
- Draft PR94 only; no merge or main modification.

## Review Focus
- A generic unpublished label must never connect unrelated studies.
- DOI/year connections require transitive closure and must not split study_id2.
- Missing visitor taxa and missing measurements must not become zeros.
- Unknown or derived endpoint labels must not enter direct-output counts.
- A complete but constant field-context baseline must fail variation eligibility.

## Task 1: Measurement, grouping and baseline audit
Files: add CP002_METADATA_RULES.json, audit_cp002_measurement_sources.py and
test_cp002_measurement_sources.py in research/croppol_macro/.
Interfaces: inspect_csv(raw: bytes) -> aggregate dict; main() -> exit status;
reuse CP001 fetch_verified_source, verify_bytes, EXPECTED_COLUMNS.
- [x] Write hand-derived fixtures covering the five Review Focus risks, zero/
  missing syntax, method/unit mismatch, source schema failure, safe output,
  source read failure receipts and separate primary/secondary endpoints.
- [x] Run tests against unimplemented interfaces and observe failure.
- [x] Implement the classifiers, source connected components, aggregate counts
  and predictor-only completeness/variation audit.
- [x] Run all CP001 and CP002 tests; expect zero failures.
- [x] Obtain fresh independent code review; fix important findings with a
  reproduced failing test and record rulings.

## Task 2: Original execution and interpretation
Files: add .github/workflows/cp002-croppol-measurement-sources.yml and dated
aggregate receipt/result; update PR94 metadata.
Consumes: Task 1's inspect_csv/main and frozen rules.
- [ ] Commit code/rules/workflow before live execution.
- [ ] Execute original source audit; require verified identity/schema and
  aggregate-only artifact. A STOP is not a null ecological result.
- [ ] Inspect exact-head logs, verify artifact hash, and independently recount
  the decisive candidate and component counts.
- [ ] Persist result, remaining limitations and validation evidence; verify
  final-head execution and draft/unmerged state.

## Ledger
Pre-flight: Task 2 consumes Task 1 aggregate receipt, not raw data; no conflict.
Ruling: use a separate CP002 audit, preserving CP001 as the prior-stage record.
Cost if wrong: more files to maintain; avoids silently changing the old counts.
Ruling: no model in CP002; source meaning and baseline adequacy must be measured
before an incremental prediction test can be scientifically specified.
Cost: biological result waits for an admissible design rather than a trivial
constant-baseline comparison.

Task 1: initial 14 synthetic cases failed before implementation; after
implementation, DOI-regex failures were resolved and all 24 CP001/CP002 tests
passed. Two additional provenance-boundary fixtures then reproduced incorrect
embedded-year removal and valid DOI-parenthesis trimming; both fixed, 26/26 pass.
Ruling: original/coordinated DOI allowlist replaces unvetted parseable-DOI links;
source review identified synthesis containers and erroneous DOI suffixes.
Cost: unknown true source links may remain unmerged, so independence stays
unverified and modelling admission remains closed.
Ruling: preserve sampling protocol and report half-pair baseline variation in
addition to any variation, based on the independent pre-outcome design review.
Cost: narrower comparison blocks and possibly fewer feasible fields.

Final review: fresh independent review completed before live production execution.
Final: fixed baseline-denominator loss, impossible measurement domains and
unknown abundance scopes, duplicate-key dependence on metadata/covariates,
and missing-group namespace collision. Seven targeted fixtures reproduced the
issues (including missing-token inconsistency); final suite 33/33 passed.
Ruling: reviewer-set-aside provenance issues remain scientific limitations: no
physical field identity, independent programme identity, source endpoint
construction or preharvest covariate timing is certified. Cost: this audit cannot
admit a confirmatory transfer model even when its implementation succeeds.
Ruling: per-file source-hash documentation is supplied by the independently
collected evidence manifest, including the template blob verified by root.
No review finding is left as a deferred code defect.
