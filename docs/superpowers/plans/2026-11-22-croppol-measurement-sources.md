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
- [ ] Write hand-derived fixtures covering the five Review Focus risks, zero/
  missing syntax, method/unit mismatch, source schema failure, safe output,
  source read failure receipts and separate primary/secondary endpoints.
- [ ] Run tests against unimplemented interfaces and observe failure.
- [ ] Implement the classifiers, source connected components, aggregate counts
  and predictor-only completeness/variation audit.
- [ ] Run all CP001 and CP002 tests; expect zero failures.
- [ ] Obtain fresh independent code review; fix important findings with a
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
