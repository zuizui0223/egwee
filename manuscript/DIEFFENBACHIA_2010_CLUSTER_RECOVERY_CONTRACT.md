# ML012 / *Dieffenbachia seguine* 2010 cluster-recovery contract

**Locked:** 2026-09-13, before exact population-level Table 2/3 values are opened for quantitative synthesis.

## Goal

Test whether Cuartas-Hernández, Núñez-Farfán & Smouse (2010), DOI `10.1038/hdy.2009.179`, can contribute a fourth independent covariance-aware fragmentation cluster.

The source design contains two fragmented populations (`F1`, `F2`) and two continuous-forest populations (`C1`, `C2`) sampled under the same field campaign and analysed with the same nine allozyme loci.

## Independent-unit frame

Primary independent unit = population.

- fragmented n = 2 populations (`F1`, `F2`);
- continuous n = 2 populations (`C1`, `C2`);
- maternal families, mothers, seedlings, reproductive individuals and loci are nested below population and cannot become fragmentation replicates;
- the complete 2010 four-population experiment counts as one cross-system cluster.

The small `2 + 2` population frame is retained explicitly. It is not enlarged with family-, seedling-, locus- or plant-level pseudo-replication.

## Locked exposure

Primary exposure = source-defined forest condition:

- `fragmented`: F1, F2;
- `continuous`: C1, C2.

No post-outcome replacement with fragment size, reproductive density, pairwise geographic distance, pollinator abundance or another ecological covariate is allowed.

## Locked primary layers

### C — contemporary pollen immigration support

Primary C endpoint = **population-level pollen immigration fraction** from the source assignment analysis.

The source explicitly used adult/population assignment to estimate the fraction of male gametes assigned outside the maternal population. This directly measures contemporary cross-population pollen support and is therefore the primary movement/connectivity layer.

Orientation:

- higher immigration fraction = greater external pollen connectivity support;
- primary Hedges-g contrast is fragmented minus continuous;
- negative oriented g means fragmentation is associated with reduced external pollen support.

The source-reported group averages (31% fragments, 26% continuous) are not sufficient for admission. Exact F1/F2/C1/C2 values are required.

Do not replace C after value access with effective pollination area, geographic distance, local assignment, or another variable because it has a stronger contrast.

### G_mating — effective pollen-donor diversity

Primary G_mating endpoint = source `N_ep`, the effective number of pollen parents for the average maternal sibship, from the population-specific pollen-pool analysis.

Rationale fixed before opening exact values:

- `N_ep` is the source's direct effective-donor-number representation;
- higher `N_ep` = greater pollen-donor diversity/support;
- it is preferable to choosing inverse correlated paternity post hoc;
- `r_p`, adjusted pollen-pool structure and effective pollination area remain mechanistic/sensitivity context and are not separate primary layers.

Primary Hedges-g orientation is fragmented minus continuous, with negative oriented g meaning reduced donor diversity in fragments.

## Linked adult-genetic context

The 2006 programme paper reports adult genetic diversity for populations including C1/C2/F1/F2. These observations may be retained as linked programme context or a prespecified sensitivity only after population identity and sampling relationship are documented.

They do **not** create another independent study or cluster, and adult `H_O` is not required for initial ML012 admission. Do not combine 2006 observations into the primary C/G_mating covariance block unless a separate amendment establishes valid temporal/sample dependence before values are used.

## Effect representation

If exact four-population C and G_mating vectors are source-recoverable, calculate source-defined binary habitat effects using the existing standardized binary contract:

- Hedges g with `metafor::escalc(measure="SMD", vtype="LS")` semantics;
- independent sample sizes are `n_fragmented = 2`, `n_reference = 2`;
- no family/offspring/locus counts enter the fragmentation-level variance formula.

The small-n result is allowed to be imprecise. Do not inflate its precision with lower-level denominators.

## Within-cluster dependence

C and G_mating are measured on the same four populations and cannot be treated as independent effects.

After exact four-population values are recovered:

1. orient both population vectors as biological support before covariance calculation;
2. group-center within fragmented/continuous conditions;
3. compute the paired-population outcome-correlation proxy;
4. construct the 2×2 working covariance from that correlation and the locked marginal sampling variances;
5. require finite marginal variances and a positive-definite 2×2 covariance matrix.

Because four populations split across two exposure groups leave only `4 - 2 = 2` residual dimensions, the dependence estimate is fragile and must be labelled `proxy_reconstructed_small_n`.

If the 2×2 proxy is singular/non-finite, do not ridge it and do not set covariance to zero. Terminate `dependence_not_reconstructable` for covariance-aware admission; the signed source effects may remain descriptive/sensitivity evidence.

## Source-opening order

1. lock this contract;
2. inspect source table schemas/row labels only to verify that Tables 2/3 expose population-specific F1/F2/C1/C2 `N_ep` and pollen-assignment values;
3. freeze the exact Table 3 immigration calculation if assignment values require a row/column operation;
4. only then open exact population values once;
5. calculate C, G_mating and within-cluster dependence once;
6. accept concordant, discordant, null, imprecise or non-identifiable outcomes without rescue.

## No-rescue rules

Do not:

- count mothers, families, seedlings, reproductive individuals or loci as fragmentation n;
- choose `r_p`, `A_ep`, reproductive density or another mating parameter after observing which gives the desired result;
- use the source's 31% versus 26% group averages as though they were population-level replicates;
- infer exact Table 2/3 values by digitizing figures;
- import adult `H_O` from 2006 as an independent 2010 study;
- set C/G covariance to zero;
- add a numerical ridge solely to invert the covariance;
- change the fragmented/continuous classification after outcome access.

## Possible terminal states

- `ML012_admitted_C_Gmating_covariance_aware`;
- `population_specific_C_not_reconstructable`;
- `population_specific_Nep_not_reconstructable`;
- `dependence_not_reconstructable`;
- `source_access_blocked`.

All terminal outcomes are acceptable.