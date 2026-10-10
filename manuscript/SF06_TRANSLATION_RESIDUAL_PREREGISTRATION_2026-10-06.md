# SF06 pollination→female-fitness translation-residual reanalysis — preregistration 2026-10-06

## Provenance correction after the first numerical execution

The **core compatibility-residual hypothesis and decision rule** in this document were genuinely frozen at commit `a49af606` (2026-10-06 14:13:10 UTC), before any project-computed SF06 row-level result existed.

GitHub Actions run `37477126333` was triggered from that commit and the runner was first provisioned at **14:36:24 UTC**. Its analysis emitted the first project-computed SF06 result at **14:36:47 UTC**. A later structural audit showed that the accessible public Table S1 DOCX itself contains **426 response-labelled physical rows** (267 female fitness, 88 male fitness, 71 pollination); its first Word table is header-only. The article reports **500 hierarchical meta-analysis input effects** (312/105/83), so the 74-value discrepancy is a **public-source coverage boundary**, not a recoverable skipped-table parser error. The first numerical output is therefore retained as a preliminary result for the available public-S1 subset, with later implementation/robustness changes tracked separately.

The timing classification used below is therefore:

- **initial preregistration:** the compatibility-residual question, exact paired unit, Hedges-d model, `gamma_SC > 0` prediction and decision rule present at `a49af606`;
- **pre-exposure topology specification:** the sign-topology target (`990a235`, 14:27:01 UTC) and constituent-sign consensus rule (`d5e02c2`, 14:32:51 UTC), both committed before the first runner was provisioned;
- **concurrent / not cleanly confirmatory:** the metadata pair-manifest change `a079f11` (14:36:36 UTC), committed after the first runner had started but 11 seconds before its logged numerical output;
- **post-exposure robustness or implementation correction:** all gates and sensitivities added after 14:36:47 UTC, including the minimum-coverage gate, publication normalization, source-overlap sensitivity, decision tree, species-level leave-one-out, frozen source/pair hard gate and the 500-row completeness repair.

Accordingly, the public-S1 reanalysis tests a **preregistered biological target in the complete accessible 426-row supplement, with post-exposure provenance and robustness corrections**. It must not be described as a clean untouched confirmatory replication. See `SF06_OUTCOME_EXPOSURE_TIMELINE_2026-10-06.md`.

## Post-exposure sign-parser correction — 2026-10-07

A raw Word-XML audit after outcome exposure showed that Hedges-d cells encode negative values with a space between sign and magnitude (for example, `- 1.733`). The original `first_float()` parser silently dropped these spaced minus signs. Commit `800ccfa` repaired the parser and added explicit invariants for ASCII and Unicode minus signs.

The corrected public-S1 result is therefore the authoritative implementation of the preregistered biological target, but the repair occurred after numerical exposure. The route remains classified as a preregistered biological question with a post-exposure implementation repair, not as an untouched confirmatory test.

Corrected headline results:

- external sign topology: 12/54 minimum mismatches, publication-LOO minimum 8, species-LOO minimum 11;
- source-publication-disjoint topology: 7/31 mismatches, publication-LOO minimum 5, species-LOO minimum 6;
- gamma_SC = +0.0639, 95% CI [-0.2627,+0.3905], p=0.701, directionally consistent but unresolved.

The earlier negative gamma and zero-mismatch topology remain archived only as invalidated parser outputs.

## Status

Prospectively specified **before opening or storing the row-level Hedges-d outcome cells** from Aguilar et al. (2024 online / 2025 volume), Supplementary Table S1 (doi:10.1093/aob/mcae076).

The source paper and its aggregate results are known: land-use effects on pollination and female fitness are positively correlated, and compatibility system moderates marginal average effects. EGWEE has already materialized the source publication/species/trait universe while deliberately excluding `Hedges' d` and `V(d)` cells.

This route asks a different question from the source paper and from the frozen EGWEE 16-programme translation map.

## Biological question

> **At the same observed pollination response to land-use change, does plant compatibility system predict the downstream female-fitness response?**

The hypothesis generated from the EGWEE translation analysis is that reproductive assurance can change the conversion from pollination damage to female fitness. A broad self-compatible (SC) label is an imperfect proxy for effective assurance, but the SF06 database provides enough coverage for a first independent external test.

## Source

Fixed public source:

- Aguilar et al., *Annals of Botany*, doi:10.1093/aob/mcae076;
- public Supplementary Table S1;
- source file hash must match or be recorded by the analysis workflow;
- no alternative dataset is substituted after outcomes are opened.

### Post-exposure source-coverage correction: public S1 versus paper-reported input counts

Aguilar et al. report hierarchical meta-analysis input counts of 312 female-fitness, 105 male-fitness and 83 pollination effects (500 total). The accessible Supplementary Table S1 DOCX contains only 267, 88 and 71 response-labelled physical rows (426 total). Structural audit of all seven Word tables shows a header-only first table followed by six data tables with 79/79/79/79/79/31 rows; the first data row is *Calystegia collina*. Thus scanning the first Word table cannot recover the 74-count shortfall.

The authoritative public-source reanalysis therefore targets **all 426 rows actually present in the accessible S1 file** and records the paper-versus-public shortfall explicitly. It does not reconstruct the missing 74 paper-reported inputs. Any result is a public-S1 subset validation, not a reanalysis of the complete 500-input database.

## Post-exposure reproducibility gate for corrected reruns

Before any row-level Hedges-d or variance cell is used for inference:

1. the metadata-only exact pair manifest must already exist in EGWEE with `outcome_opened=no`;
2. the downloaded Supplementary Table S1 SHA256 must exactly equal the source hash recorded by the metadata-only SF06 materialization;
3. re-parsing source metadata must reproduce exactly the frozen `normalized publication × species × land-use` pair-key universe.

Failure of any gate stops the analysis before inferential results are generated.

## Pair construction

Rows are parsed exactly from Supplementary Table S1. Publication identity is normalized only for case and whitespace when constructing pair and cluster keys; the original citation string is retained for display.

Primary paired unit:

`normalized source publication identity × plant species × land-use factor`.

A unit is eligible only when it contains both:

- `Pollination`; and
- `Female fitness`.

Primary exposure restriction:

- `land_use_factor`, after case/whitespace normalization, must equal `habitat fragmentation`.

Male-fitness rows are excluded from this analysis.

If more than one row exists for one response inside the same paired unit, rows are combined **within response** by inverse-variance fixed-effect weighting before I–F pairing. For the Hedges-d residual model, **every constituent row** in both responses must have a finite Hedges d and positive variance; otherwise the whole paired unit is numeric-model-ineligible rather than dropping incomplete constituent rows. The sign-topology lane remains separate: it requires all constituent Hedges-d signs to be present and concordant within a response but does not require variance except for the resolved-95% sensitivity. No outcome-based endpoint selection is allowed.

Compatibility is taken only from the source metadata:

- `SI` = self-incompatible;
- `SC` = self-compatible;
- `NA` / undetermined is retained descriptively but excluded from the primary compatibility coefficient.

## Primary estimand

Let:

- `d_I` = source Hedges d for pollination;
- `d_F` = source Hedges d for female fitness.

The source orientation is retained: negative values mean lower pollination or fitness under anthropogenic land-use change.

Primary model:

`d_F = alpha + beta * d_I + gamma * SC + error`

with equal weight per paired unit and **publication-cluster-robust** standard errors.

Primary coefficient:

`gamma_SC`.

Directional prediction:

`gamma_SC > 0`.

Interpretation: for the same observed pollination response, self-compatible plants retain higher / less-negative female fitness than self-incompatible plants.

The reported primary inference is the two-sided cluster-robust p-value and 95% CI. The directional prediction is evaluated by coefficient sign; no one-sided p-value is used as the headline.

## Secondary estimands

1. Pair difference:
   `Delta = d_F - d_I`.
   Negative Delta means female fitness is more negatively affected than pollination on the source Hedges-d representation.

2. Cluster-robust model:
   `Delta = alpha + gamma_delta * SC + error`.

3. Interaction sensitivity:
   `d_F = alpha + beta*d_I + gamma*SC + theta*(d_I*SC) + error`.

4. Sign-topology census by compatibility:
   - false reassurance point geometry: `d_I >= 0, d_F < 0`;
   - apparent over-warning/buffering point geometry: `d_I < 0, d_F >= 0`;
   - concordant deterioration: `d_I < 0, d_F < 0`;
   - concordant non-deterioration: otherwise.

These topology counts are descriptive and not prevalence estimates.

## Sensitivities

- all eligible land-use factors, without the habitat-fragmentation-only restriction;
- inverse-variance weighted Delta regression using `V_F + V_I` as a zero-covariance working variance;
- publication-balanced regression in which each publication contributes equal total weight;
- **non-overlap external sensitivity:** delete every source publication already represented in the frozen EGWEE 16-programme I–F translation map, then rerun the consensus-sign topology and, when numerically estimable, the compatibility residual model.

The frozen overlapping SF06 publications are Aizen & Feinsinger (1994), Angoh et al. (2021), Chen & Zuo (2019), Chen et al. (2019), Chiapero et al. (2021), da Silva Elias et al. (2012), González-Varo et al. (2009), Kolb (2008), and Lopes & Buzato (2007). Whole publications are deleted even when SF06 contains additional focal species.


Unknown within-pair covariance is **not** estimated from outcomes and is not silently assumed known. The unweighted cluster-robust primary model avoids using a fabricated I–F sampling covariance.

## Decision rules

Support for the proposed compatibility translation modifier requires:

1. `gamma_SC > 0`; and
2. its 95% cluster-robust CI excludes zero in the primary habitat-fragmentation subset.

If the sign is positive but the interval includes zero, classify as `directionally_consistent_unresolved`.

If the sign is zero/negative, classify as `compatibility_translation_prediction_not_supported`.

No result can establish "effective reproductive assurance" because SF06 records compatibility, not experimentally measured viable assurance.

## Claim ceiling

Allowed if supported:

- compatibility system explains residual pollination→female-fitness translation in this external source database;
- this provides external evidence that average pollination damage does not uniquely determine female-fitness damage;
- a corrected result may be described as **robust external generalization with a source-disjoint sensitivity** only when the non-overlap publication subset also passes the post-exposure coverage/influence gates. It must not be labelled a preregistered confirmatory replication. Otherwise the result is external-source confirmation with partial source overlap.

Not allowed:

- compatibility is the universal mechanism of EGWEE false reassurance;
- SC equals effective reproductive assurance;
- the source Hedges-d residual is effect-scale invariant;
- the reanalysis changes the frozen EGWEE 16-programme denominator;
- individual SF06 rows are independent when they share a publication.

## Independence from the source paper's published question

Aguilar et al. test compatibility as a moderator of the **marginal average effect** on pollination and on female fitness separately and report a positive overall pollination–female-fitness association.

This preregistration instead tests whether compatibility explains the **residual translation between the two responses within paired source units**.


## Pre-exposure topology definition and post-exposure robustness extensions

The **topology question** was committed at `990a235` (14:27:01 UTC) and the stricter **constituent-sign consensus rule** at `d5e02c2` (14:32:51 UTC), both before the first SF06 runner was provisioned at 14:36:24 UTC and before the first numerical result was emitted at 14:36:47 UTC. Those two elements were therefore specified before project-computed outcome exposure.

Later additions in this section are not preregistered confirmatory criteria. The minimum coverage gate, source-overlap sensitivity, publication-normalization repair, species-level leave-one-out, frozen-input gates and 500-row completeness repair were added after the first numerical exposure and are retained as conservative **post-exposure robustness / implementation controls**.

### Primary external-generality target

The main external generality question is now:

> **Among species/studies that measured pollination and female fitness under the same land-use contrast, does the sign of the pollination response deterministically identify the sign of the female-fitness response?**

For the **scale-stable primary topology**, response sign is defined from the constituent source rows *before* inverse-variance aggregation:

- `lower` only when **all** constituent effects for that response are negative;
- `nonlower` only when **all** constituent effects are zero or positive;
- `mixed` when constituent effects span both sides of zero.

A paired unit enters the scale-stable topology only when both I and F have consensus signs. This is deliberately stricter than using the sign of an inverse-variance weighted Hedges-d summary. Standardization by a positive SD cannot reverse each constituent mean-contrast sign, whereas changing effect representation can change relative weights and could in principle reverse the sign of an aggregated summary.

For the habitat-fragmentation subset, calculate the **best deterministic lookup** from consensus `I_sign` to consensus `F_sign`. For each observed I-sign state, choose the F-sign state that minimizes mismatches. Sum the remaining mismatches across I-sign states.

The sign of the inverse-variance weighted Hedges-d summaries is retained only as a **representation-specific sensitivity**, not as the scale-stable primary topology.

This is a structural compatibility diagnostic, not an out-of-sample error rate.

### Primary decision rule

Classify the external SF06 sign map as `external_sign_translation_nonidentifiability_supported` only when:

1. the habitat-fragmentation consensus-sign subset passes a **minimum coverage gate of at least 10 paired units, at least 10 unique plant species and at least 5 source publications**;
2. the full habitat-fragmentation **consensus-sign** paired set has at least one deterministic mismatch;
3. after deleting every whole source publication in turn, the best deterministic consensus I-sign→F-sign lookup still has at least one mismatch; and
4. after deleting every whole plant species in turn, the best deterministic consensus I-sign→F-sign lookup still has at least one mismatch.

The minimum coverage gate and whole-species influence rule were added **after the first preliminary numerical exposure**. They therefore cannot upgrade the SF06 route to confirmatory status. They are retained only as conservative promotion criteria for the corrected reanalysis, preventing repeated measurements of a few species from being presented as broad external generality. The source paper reports 82 species with simultaneous pollination and female-fitness effects before this stricter consensus filtering.

If the full map is non-identifying but at least one publication deletion removes all mismatches, classify as influence-sensitive.

### Conservative uncertainty sensitivity

For each endpoint separately, call a sign **resolved lower** only when the 95% marginal interval `d ± 1.96*sqrt(V)` lies below zero, and **resolved nonlower** only when the interval lies above zero. Pairs with either unresolved endpoint are excluded from this sensitivity.

The resolved-only topology is descriptive unless enough pairs remain; it is not required for the primary structural decision because marginal non-resolution does not make a point estimate equal to zero.

### Compatibility remains a secondary mechanism test

The preregistered model

`d_F = alpha + beta*d_I + gamma*SC + error`

remains unchanged as a **representation-specific mechanistic test**. A positive `gamma_SC` can support compatibility as one translation modifier on the source Hedges-d scale, but it is not used to establish the scale-stable external generality claim.

Thus the evidence hierarchy is:

1. **scale-stable external generality:** sign-level I→F non-identifiability;
2. **scale-dependent mechanism probe:** compatibility residual on source Hedges d.

Neither lane estimates the prevalence of false reassurance in nature.
