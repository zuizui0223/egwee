# LUPF1 original-run stop, source-only diagnosis, and strictly bounded repair (2026-11-24)

Status: **source schema stop, NOT a biological null**. The initial outcome-read attempt [GitHub Actions run 45311778662](https://github.com/zuizui0223/egwee/actions/runs/45311778662) produced `SOURCE_OR_FROZEN_ANALYSIS_STOP`, reason `SOURCE_FIELD_HEADERS_CHANGED`, **zero outcome-model scores**, although the CI job itself was marked success because valid source stops are allowed.

## Independent source-only diagnosis

[Run 45328163059](https://github.com/zuizui0223/egwee/actions/runs/45328163059) printed **ONLY verified original XLSX worksheet-header spellings**, no seed-count values. The 2026 source sheet2 has raw header `number of seeds` (spaces), whereas the preregistered script requested normalized `number_of_seeds`. Other required raw headers `id`, `genotype`, `population`, `line`, `flowering_onset` match literally. Previous metadata logs showed normalized headings, inadvertently hiding the spelling difference.

## Exact correction boundary

- Input decoder now selects source-native `number of seeds` and renames **only this key** to the preregistered internal field `number_of_seeds`. No alternate outcome column and no data-selected exclusion.
- New synthetic XLSX test verifies the mapping before reaching real numerical outcomes.
- **Unchanged**: source article and sheet, 3,024 source rows, anonymized six-category line baseline, outcome y=log1p(seed_count), flowering-onset predictor, genotype-group five-fold split, ridge lambda=1, two-part success rule, 1,000 group-bootstrap uncertainty, missingness rules, no causal genetic or G×I×F claim.
- Preregistration remains commit `28938fe193d01d7eca5bd2fe776f37ecb1f58e27`, an ancestor of all repair commits. The workflow must verify this ancestry.
- In case of further source semantic/denominator mismatch, STOP explicitly and diagnose; do not change model/holdouts after outcome inspection.

**No new result is implied by a fixed parser**. Distinguish CI success from empirical analysis success. Next action: read CI rerun's JSON outcome artifact, validate source count/fold blocks and record the signed result unchanged; if it stops again, document the exact stop without selecting a new model.
