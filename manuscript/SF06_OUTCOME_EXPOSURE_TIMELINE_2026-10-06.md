# SF06 outcome-exposure timeline and inferential provenance — updated 2026-10-07

## Purpose

Record when SF06 numerical outcomes first existed, which decisions preceded exposure, which later changes were robustness additions, and how the spaced-minus parser defect changes interpretation.

The exposure boundary remains the first logged project-computed numerical result, even though that result is now known to be numerically invalid.

## Timeline

| UTC time | event | inferential status |
|---|---|---|
| 2026-10-06 14:13:10 | a49af606: compatibility residual preregistration | pre-outcome biological target |
| 14:13:15 | Actions run 37477126333 created | queued |
| 14:27:01 | 990a235: sign-level external topology target | pre-exposure specification |
| 14:32:51 | d5e02c2: constituent-sign consensus rule | pre-exposure specification |
| 14:36:24 | first SF06 runner provisioned | numerical execution begins |
| 14:36:47 | first numerical result emitted | outcome-exposure boundary |
| 14:39 onward | coverage, source-overlap, species-LOO and other promotion gates | post-exposure robustness |
| 23:24–23:34 | public DOCX structure audited | 426 physical response rows confirmed; 500 vs 426 reclassified as source-coverage boundary |
| 2026-10-07 11:52 | raw result-column audit | Hedges-d cells confirmed to contain spaced signs, e.g. "- 1.733" |
| 13:31 | 800ccfa: first_float parser fixed for spaced signs | post-exposure implementation repair |
| 13:32 | corrected gated rerun | authoritative public-S1 result generated and committed |

## The initial numerical exposure

The first run emitted:

- all paired units: 59;
- habitat-fragmentation pairs: 55;
- gamma_SC = -0.087740;
- 95% CI [-0.2899, +0.1144];
- p = 0.395;
- preliminary sign-topology mismatch count = 0.

Those values are retained in the audit trail but are **not biologically valid**.

### Why they were invalid

The source Word cells store negative Hedges d with a space between sign and magnitude:

- Cardiopetalum female fitness: "- 1.733";
- Cardiopetalum pollination: "- 0.048";
- Spondias pollination: "- 1.225";
- Spondias female fitness: "- 0.796".

The original parser used a regular expression that only retained a sign directly attached to the number. Thus "- 1.733" became +1.733.

The result-column mapping itself was correct:

- penultimate data cell = Hedges d;
- final data cell = V(d) followed by source citation.

The defect was specifically sign parsing.

## Corrected authoritative public-S1 result

After commit 800ccfa fixed spaced-sign parsing and added parser assertions, the same frozen public-S1 source produced:

### Sign topology

Habitat-fragmentation constituent-consensus pairs:

- n = 54;
- I lower, F lower = 35;
- I lower, F nonlower = 9;
- I nonlower, F lower = 7;
- I nonlower, F nonlower = 3;
- minimum deterministic mismatches = 12;
- publication-LOO minimum = 8;
- species-LOO minimum = 11;
- decision = external_sign_translation_nonidentifiability_supported.

Source-publication-disjoint sensitivity:

- n = 31;
- minimum mismatches = 7;
- publication-LOO minimum = 5;
- species-LOO minimum = 6;
- decision = external_sign_translation_nonidentifiability_supported.

### Compatibility residual

Primary model:

- gamma_SC = +0.063904;
- 95% CI [-0.262674, +0.390482];
- p = 0.701333;
- decision = directionally_consistent_unresolved.

The positive pollination coefficient is beta = +0.190421, p = 0.00531.

## Public-source coverage boundary

The downloadable Supplementary Table S1 contains:

- 267 female-fitness physical rows;
- 88 male-fitness physical rows;
- 71 pollination physical rows;
- total = 426 response-labelled rows.

The source article reports 500 hierarchical meta-analysis input effects. The missing 74 paper-reported inputs are not reconstructed. Every EGWEE SF06 row-level result is therefore a **public-S1 subset result**, not a complete 500-input reanalysis.

## Inferential classification

### Compatibility residual

The biological question, paired unit, primary model, directional prediction gamma_SC > 0 and decision rule were fixed before numerical exposure.

The corrected result must be described as:

> a preregistered biological hypothesis evaluated with a post-exposure implementation repair.

It is not an untouched confirmatory test. The result is directionally consistent but unresolved.

### Sign topology

The topology target and constituent-sign consensus rule were specified before first numerical exposure.

The corrected result supports external sign-level translation non-identifiability. However, publication/species coverage gates, source-overlap deletion and the parser repair were post-exposure additions or repairs. Therefore the allowed wording is:

> robust external generalization within the accessible public-S1 subset, with a pre-exposure-defined topology target and post-exposure implementation/robustness controls.

Do not call the entire route a preregistered confirmatory replication.

### Resolved-sign sensitivity

Only three pairs have both marginal endpoint signs resolved at 95%, and all three are lower/lower.

Therefore the external result is structural point-sign non-identifiability, not 12 individually resolved sign reversals.

## Hard rules

- preserve the invalid initial outputs for provenance;
- never cite the invalid negative gamma_SC or zero-mismatch topology as biology;
- do not call post-exposure gates preregistered;
- do not describe public S1 as the complete 500-input database;
- do not promote self-compatibility as a supported mechanism;
- do not convert mismatch counts into prevalence or out-of-sample prediction error;
- do not describe the 12 mismatches as 12 significant sign reversals.
