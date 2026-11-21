# Molecular conservation bridge — source gate decision, 2026-11-18

## Verified evidence at this gate
This note reconciles the new prospective molecular-conservation design with the pre-existing executed natural source receipt; it does not claim a fresh raw-data run.

- Source metadata and official Dryad file inventories: 2/2 verified for SMF001 and SMF002.
- SMF001 Argentina anserina: 10 original files, six named target XLSX present.
- SMF002 Leavenworthia alabamica: 12 original files, seven named target XLSX present.
- Download attempts for original workbooks raised HTTPError in both cases; precise status/auth cause was not established in the saved abbreviated console.
- Original XLSX worksheets actually read: 0.
- Verified same-mother/plant/year genotype × interaction × seed keys: 0.
- Newly estimated molecular-to-function effects: 0.
- CI runs 44035790388 and 44036022987; latest artifact 14307332132, SHA256 ddc728d5e613f6b232b62434c8378770436b6aac0ab2d785d71098d6612aba47.
- Existing receipt: research/compatibility_function/PRIMARY_PROGRAMMES_SOURCE_RECEIPT_20261117.md.

## Identifiability matrix
| programme | genetics | effective interaction | direct F | verified joint unit | current decision |
|---|---|---|---|---|---|
| SMF001 Argentina | inferred S/mate availability | controlled pollen tubes, no verified same-unit natural visitation | outcross seed count | no | SOURCE_ACCESS_STOP; only narrower controlled-cross question plausible after raw keys |
| SMF002 Leavenworthia | S-locus/self-compatibility | field pollinator visits | maternal fitness/seed | no | SOURCE_ACCESS_STOP; genotype×visit×maternal-year linkage unknown |
| SMF003 Rutidosis | diallel-estimated compatibility | pollen deposition | seed set | population-level published only | REUSABLE_NUMERIC_MATRIX_UNVERIFIED; observational prior art |
| SMF004 Spondias | adult/offspring genotype, paternity | source reports not matched to genetic-site/mother grain | fruit/seed source summaries | no | JOINT_GRAIN_NOT_IDENTIFIABLE |

## Decision and next action
Primary H3 cross-layer prediction cannot be fitted without fabricated joins: **NOT_IDENTIFIABLE_FROM_CURRENT_PUBLIC_RAW_ACCESS**. No claim of failed ecological effect.

The next legitimate action is authorized acquisition of one original source workbook or an author-provided equivalent, then **schema-only** inspection. Prefer SMF002 for a potential genotype × field visitation × seed outcome path; this is a source-structure priority, not evidence of joinability or effect direction. SMF001 remains the fallback for a narrower controlled-cross compatibility × seed test.

Before any outcome values are read, record:
1. original DOI/version, file member name, SHA256, and lawful acquisition route;
2. worksheet headers, field types, source-defined maternal/plant/population IDs, year, treatment, ploidy;
3. exact join keys and whether observational units represent the same mother/plant/cohort;
4. whether direct F occurs after predictors, with unobserved outcomes retained as missing;
5. independent holdout units and non-event denominator.

Gate PASS only if a non-invented genotype/compatibility × interaction × direct F join exists with source-consistent independent units and temporal ordering. Otherwise label NOT_IDENTIFIABLE and do not fit.

## Locked model proposal (only if gate PASS)
M0: D + habitat/environment + ancestry/neutral G + direct I.
M1: M0 + validated G_compatibility + effective pollen-donor state + predeclared I×G_compatibility; spatial alignment only if patchwise data actually exist.
Primary statistic: held-out mean NLL(M1)-NLL(M0), grouped by independent populations/programmes. Negative means improvement. Report block bootstrap uncertainty, calibration, and study-level sensitivity; do not use fruit/seed/locus as independent study.
Genetic intervention and ecological intervention effects are distinct; no causal genetic rescue without a valid controlled comparison and offspring/fitness endpoint.

## Claim ceiling
Existing field evidence supports compatibility limitation in some systems, not cross-system predictive transport or causal rescue. Neutral diversity, S-allele availability, effective mating, general fitness, and interaction-dependent seed/recruitment function are distinct. The numerical model AUC 0.927 is not a natural result. The five-cluster EGWEE synthesis and active EGWE Theoretical Ecology flagship remain untouched.

## Follow-up executed HTTP diagnosis — 2026-11-19
- Workflow: https://github.com/zuizui0223/egwee/actions/runs/44456077128 ; status completed/success.
- Job: 135331287864. Artifact: 14497324362, name molecular-source-access-only, SHA256 04e3998ec2f0a57c0ee7669dafc5fb88c47f568f4e3bdbbcf94d8d97bd720154.
- SMF001 official API advertises six XLSX, first two probed returned HTTP 401 each.
- SMF002 official API advertises nine XLSX (not all are the seven preselected target workbooks), first two probed returned HTTP 401 each.
- Thus 4/4 bounded probes were HTTP 401, no redirected success. The precise authentication requirement and availability via another legitimate publisher/author route are not established.
- Probe is Range bytes=0-0 and reads at most one response byte if reachable; no biological values are retained or displayed. Workflow success signifies successful diagnosis, **not successful source acquisition**.
- Decision remains SOURCE_ACCESS_STOP, no valid G×I×F matched rows and no new ecological result. Do not use unauthorized endpoints, scrape login sessions, or infer that all files are inaccessible from four probes.
- Next action: use documented source-owner or repository-authorized original file route; once acquired, inspect headers and provenance only, then freeze join grain before effect analysis.
