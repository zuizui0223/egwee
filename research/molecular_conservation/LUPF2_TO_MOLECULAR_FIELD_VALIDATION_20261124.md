# From LUPF2 phenology→reproductive-index prediction to a molecularly testable conservation hypothesis

**Status 2026-11-24: synthesis/design, NOT a new causal or cross-system empirical conclusion.**

## What actually advanced
- **Observed, within-study exploratory T→W prediction:** *Lupinus angustifolius* 2026 field F3 source data, 2,008 complete-case records, 84 original experimental genotype-label groups, pooled held-out MSE M0=1.134807 (population+unknown line) versus M1=0.870675 (+flowering onset), gain +0.264132, 5/5 folds. See `LUPF2_EXPLORATORY_HOLDOUT_RESULT_20261124.md`. Original LUPF1 failed source integer validity and is preserved as a stop.
- **Unresolved selection:** only 66.4% source records carry both variables; FRO 69.6%, PIC 62.9%; unverified anonymous codes R and X only in FRO. See `LUPF2_POSTHOC_OBSERVATION_SUPPORT_20261124.md`. Missing phenotype data cannot be equated with biological reproductive failure.
- **Already published:** Sacristán-Bajo et al. 2025 (DOI 10.1111/eva.70087) and 2026 (DOI 10.1093/aob/mcag061) showed experimental advancement of flowering onset through assisted gene flow and F3 phenotypic persistence under field conditions. The original 2025 Methods describe seed production estimates and *L. angustifolius* mainly self-fertilizing before petal opening (natural outcrossing estimates below 2%). That 2025 mating-system description must **not** be misused to infer the 2026 offspring's realized paternity.

## Two mechanistic alternatives (separate, not interchangeable)

**A. Developmental/abiotic opportunity**: flowering-onset timing correlates with reproductive index because of season length, temperature, soil water, development, prior vigor or measurement/selection. This may operate in predominantly selfing taxa *without any necessary pollen-network rescue*. The present LUPF2 result cannot identify cause, sign of partial regression slope or whether the same trait predicts actual viable next-generation recruits.

**B. Interaction-gated molecular mating**: in self-incompatible taxa such as *Rutidosis leptorrhynchoides*, the genetically compatible pollen-donor pool, effective pollen transfer and S-compatibility can constrain seed production even where total pollen is delivered. Young & Pickup 2010 already published this qualitative dissociation in seven fragmented populations (DOI 10.1111/j.1365-2664.2010.01798.x). It is **prior art**, not the new LUPF2 discovery. Unmeasured patchwise cross-layer state cannot be reconstructed by joining 2008/2010/2012/2013 published population averages, some of which share identical population-pair identifiers.

## Molecular, physiological and ecological readouts in a future single-cohort study

| Process | Eligible measurement | What it must not be called |
|---|---|---|
| Neutral ancestry / population history | genome-wide SNPs from MIG-seq/ddRAD-seq, family-aware relatedness and F_ST; sample plants and offspring consistently | a validated S functional genotype or adaptive rescue by itself |
| Actual genetically compatible mating | source-validated S-locus haplotypes **only if locus and phasing verified**, or controlled diallel crossing to estimate compatibility probabilities | neutral heterozygosity or species richness |
| Effective plant–pollinator interaction | natural stigma pollen load AND compatible pollen-tube growth (e.g. staining), pollinator observation and, if genotype resolution allows, offspring paternity assignment | total visits or grains as proof of fertilization |
| Developmental T | maternal flowering onset and flowers open during local donor/pollinator activity windows | genetic cause of fecundity on its own |
| Biological function F and fitness W | maternal seed production, viable seeds, germination, cohort-tagged offspring survival/recruitment; keep W general and F interaction-dependent distinct | all sown records or nonmissing seed-index as established recruits |

## Locked alternative model classes for independent future systems

M0: F_future ~ density + climate/soil + census/genomic ancestry/neutral diversity + total pollen service + phenology.

M1: M0 + empirically determined compatible pollen-donor availability/effective mating and independent offspring paternity.

M2: M1 + **within-patch measured** covariance/alignment between maternal flowering, donor compatibility, effective interaction; avoid reconstructing this covariance from marginals.

Use holdout by entire **independent biological population/year**, not fruit, pollen grain, site nested in a shared crossing experiment or experimental genotype. Specify observation/missingness mechanism, block replication and practical smallest effect before data opening. Compare prediction and calibration; no transferable model AUC=0.927 or genomic-warning threshold. Distinguish intervention arms (pollination service restoration, ploidy/source-checked compatible pollen genetic supplementation, habitat/recruitment support) only when actual controls/randomization permit causality. Vet outbreeding depression and permits before any translocation.

## Decisive discriminating prediction
- If a trait-only time variable predicts W in the selfing comparator but adding compatible donor/pollen state materially improves heldout future F **specifically in independent SI systems**, partner-gated versus developmental bottlenecks would become distinguishable.
- If compatibility and measured interaction covariances add no independent predictive value beyond ancestry/density/phenology, the proposed generalized cross-layer transport is not supported in that design.
- Urban/island fragmentation comparisons would be **separate mechanism-stratified tests**, not presumed identical 'functional fragmentation' merely because both are spatially fragmented.

## Current gate
**Natural G×I×F cross-layer causal test: NOT IDENTIFIABLE.** LUPF2 supports only a carefully caveated empirical T–W within-experiment prediction; Rutidosis supports already-published compatibility limitation but lacks a verified common maternal×time molecular–interaction–recruitment source table. Next legitimate engineering/field step is to source or produce such co-measured data, not re-fit LUPF2 until a desired causal sign appears.
