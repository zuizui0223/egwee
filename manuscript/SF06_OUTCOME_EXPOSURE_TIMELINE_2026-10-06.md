# SF06 outcome-exposure timeline and inferential provenance — 2026-10-06

## Purpose

This file records when SF06 numerical outcomes first existed, which analysis decisions genuinely preceded that exposure, and which later changes are implementation repairs or post-exposure robustness checks.

The boundary is the **first logged project-computed numerical result**, not whether a generated result file successfully reached the Git branch.

## Timeline

| UTC time | event | inferential status |
|---|---|---|
| 14:13:10 | commit `a49af606`: compatibility translation-residual preregistration | **pre-outcome** |
| 14:13:15 | Actions run `37477126333` created from `a49af606` | queued; no runner yet |
| 14:15:35–14:20:45 | parser hardening commits `dc885d6`, `b39de7f7`, `21fc409f` | pre-exposure implementation work |
| 14:27:01 | `990a235`: sign-level external topology target added | **pre-exposure specification** |
| 14:32:51 | `d5e02c2`: topology changed to constituent-row sign consensus | **pre-exposure specification** |
| 14:36:24 | first runner provisioned for run `37477126333` | numerical execution begins |
| 14:36:36 | `a079f11`: metadata-only exact pair manifest change committed | concurrent with first run; not treated as clean confirmatory gate |
| 14:36:47 | run `37477126333` emits first SF06 numerical output | **outcome-exposure boundary** |
| 14:36:47 | generated files committed inside runner, but push rejected as non-fast-forward | result existed even though branch files did not |
| 14:39:17 onward | coverage, publication normalization, non-overlap, decision-tree, species-LOO and frozen-input gates added | **post-exposure robustness / repair** |
| 14:48:42 | run `37478175906` on parser-hardened `21fc409f` reproduces the same preliminary compatibility estimate | still based on incomplete 426-row table scan |
| 15:00:02 | `b4216301`: parser corrected to require the published 500-row totals | **post-exposure implementation correction** |

## First exposed numerical result

Run `37477126333`, job `112315344981`, emitted:

- all paired units: **59**;
- habitat-fragmentation pairs: **55**;
- `gamma_SC = -0.0877403395`;
- 95% CI: **[-0.2899153944, 0.1144347155]**;
- two-sided p = **0.3949976263**;
- preregistered decision label: `compatibility_translation_prediction_not_supported`.

Run `37478175906`, job `112319033704`, later reproduced the same estimate to numerical precision after the leading-variance parser fixes.

These numbers are **non-authoritative preliminary outputs** because both successful runs still used the 426-row scan that skipped the first Word table.

## Why the preliminary result is not the final SF06 result

Aguilar et al. report:

- female-fitness effects: **312**;
- male-fitness effects: **105**;
- pollination effects: **83**;
- total effects: **500**.

The original implementation iterated over `tables[1:]` and parsed only **426** rows. The corrected implementation now scans all Word tables and refuses to proceed unless the exact published 312/105/83 totals are recovered.

Therefore the preliminary `gamma_SC` is retained for provenance and outcome-exposure timing only. It is not used as the paper's SF06 estimate.

## Inferential classification going forward

### 1. Compatibility residual

The biological question, paired unit, primary model, directional prediction `gamma_SC > 0` and decision rule were fixed at `a49af606` before numerical exposure.

However, the implementation required a post-exposure completeness repair. The corrected 500-row run must therefore be described as:

> **a preregistered biological hypothesis evaluated with a post-exposure corrected implementation**

not as an untouched confirmatory test.

The preliminary incomplete run did **not** support the predicted positive compatibility modifier. That fact is retained and no alternative moderator may be substituted because it looks better after this exposure.

### 2. Sign topology

The topology question (`990a235`) and constituent-sign consensus rule (`d5e02c2`) were committed before the first runner was provisioned and before the first numerical output.

Later coverage, source-overlap and species-influence requirements were added after exposure. Thus the corrected topology analysis has a **pre-exposure-defined target with post-exposure robustness gates**.

Any positive corrected result may support generality, but the paper must state this mixed provenance and must not call the entire robustness stack preregistered.

### 3. Effective reproductive assurance

The failed preliminary compatibility prediction does not justify switching the SF06 moderator from compatibility to another trait.

The biologically richer concept of **effective reproductive assurance** remains a prospective hypothesis generated from the independent EGWEE mechanistic synthesis. It is not tested by SF06 compatibility labels.

## Hard rules

- Do not delete or hide the preliminary negative compatibility output.
- Do not call the 426-row result final.
- Do not call post-14:36:47 gates pre-outcome.
- Do not change the compatibility prediction after seeing the preliminary result.
- Do not promote a new SF06 moderator because compatibility was negative/unresolved.
- The corrected 500-row route must pass the frozen source hash and exact pair-universe gates before interpretation.

## Preliminary topology output from the incomplete source scan

A later queued workflow from commit `990a235` completed at 15:02:12 UTC. It still used the incomplete **426-row** scan and the older IVW-Hedges-d sign definition, but it executed the sign-topology target that had been specified before the first numerical exposure.

Its logged output was:

- exact paired units: **59**;
- habitat-fragmentation pairs: **55**;
- minimum deterministic mismatches: **0**;
- whole-publication LOO minimum mismatches: **0**;
- topology decision: `external_sign_translation_nonidentifiability_not_supported`.

This is **not the corrected external-topology result**. It is retained because it is directionally inconvenient evidence and therefore must not disappear from the audit trail. The final topology requires the corrected 500-row source scan and the stricter constituent-row consensus-sign rule.

If the corrected analysis also remains identifying, EGWEE must not claim broad sign-level external generalization. The biologically interesting conclusion would instead become a scale contrast: matched fragmentation programmes can show translation failures that are obscured when heterogeneous literature is pooled at a coarser response-summary level.
