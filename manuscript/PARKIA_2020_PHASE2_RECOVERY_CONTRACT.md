# Parkia biglobosa 2020 Phase-2 recovery contract

## Source and audit status

Source: Lompo et al. (2020), *Fine-scale spatial genetic structure, mating, and gene dispersal patterns in Parkia biglobosa populations with different levels of habitat fragmentation*, American Journal of Botany 107:1041–1053, doi:10.1002/ajb2.1504.

This is a **retrospective external recovery**. The public article tables were visible during Phase-2 full-text screening before this recovery contract was committed. Therefore this recovery does **not** claim prospective outcome blinding. The safeguard is instead deterministic endpoint selection from the already-frozen EGWEE layer definitions and use of every source-defined population in the binary comparison.

No endpoint may be switched after the effect calculation because another metric gives a larger, smaller, or more significant result.

## Exposure and independent unit

The source explicitly defines:

- cotton populations (CP) = higher habitat fragmentation: **Walley, Vouza**;
- non-cotton populations (NCP) = limited habitat fragmentation: **Saki, Cassou**.

The primary direct contrast is therefore:

`CP - NCP`

with **population** as the independent fragmentation unit:

- `n_fragmented = 2`;
- `n_reference = 2`.

Embryos, maternal trees, individual adults, loci, paternity events, and bootstrap replicates are nested observations and never become fragmentation replicates.

## Locked primary endpoints

### C — contemporary movement/connectivity

Primary endpoint: **population-level pollen immigration rate `m_p` (%) estimated by NMπ**.

Reason:
- it is reported separately for all four source-defined populations;
- it directly represents pollen entering from nonsampled adults and therefore maps to `C_movement_connectivity`;
- parentage is an allowed direct-process measurement under the Phase-2 moderator schema.

Orientation multiplier: **+1** because higher pollen immigration represents greater movement/connectivity support.

Alternative movement summaries (`r_p`, `N_EP`, CERVUS dispersal distance, NMπ kernel distance, selfing) remain descriptive/sensitivity information and are not substituted into the primary C slot.

### G_adult — standing adult genetic state

Primary endpoint: **observed heterozygosity `H_O` of large trees**.

Reason:
- EGWEE already uses `H_O` as the canonical primary genetic-support representation where it is source-resolved;
- the source defines large trees as DBH >35 cm and describes full sexual maturity at approximately 30–50 years, making this the cleanest standing mature-adult cohort;
- using one source-defined mature cohort avoids post hoc pooling of small and large trees.

Orientation multiplier: **+1** because higher `H_O` represents greater genetic support.

`H_E`, allelic richness, effective allele number, and inbreeding coefficients remain sensitivity metrics. Small-tree `H_O` is not promoted as a second independent G_adult effect.

### G_offspring — contemporary offspring genetic state

Primary endpoint: **embryo observed heterozygosity `H_O`**.

Reason:
- embryos are available in all four populations;
- the source explicitly frames the adult-to-embryo comparison as the contemporary cohort test;
- seedlings are absent from both CP populations and therefore cannot define the common four-population comparison.

Orientation multiplier: **+1**.

## Effect-size contract

For each endpoint, use the existing EGWEE direct-stream formula:

- `d = (M_frag - M_ref) / s_p`;
- `df = n_frag + n_ref - 2`;
- `J = 1 - 3/(4df - 1)`;
- `g = J d`;
- `V(g) = (n_frag+n_ref)/(n_frag n_ref) + g^2/[2(n_frag+n_ref)]`.

Between-population SD inside CP and NCP is the standardizing dispersion. Individual sample sizes and source-reported SEs are retained as provenance only.

## Dependence and pairwise contrast

The three primary endpoints share the same four populations. Dependence is represented using the same paired-unit residual-correlation proxy used for the existing Spondias cluster:

1. orient each endpoint to biological support;
2. subtract the CP or NCP group mean from each population value;
3. calculate the Pearson correlation between within-group residual vectors;
4. set `Cov_ij = rho_ij sqrt(V_i V_j)`.

With four populations split across two exposure groups there are only `4 - 2 = 2` residual dimensions. The resulting three-endpoint covariance proxy is therefore expected to be rank-deficient and must not be inverted as a full 3 × 3 covariance matrix.

The predeclared Phase-2 cohort contrast is:

`G_adult - G_offspring`.

Its pairwise variance is calculated directly from the two marginal variances and their reconstructed covariance. C-to-genetic comparisons are descriptive unless separately opened by the Phase-2 estimand contract.

## Admission rule

Parkia may enter Phase 2 as one programme only if:

- all three endpoint rows reproduce the source tables exactly;
- CP/NCP membership is fixed as above;
- population remains the independent unit;
- no lower-level sample count is used as fragmentation n;
- the recovery script reproduces all effects and the pairwise covariance proxy deterministically.

Even if admitted, this single programme does not open a pair-specific meta-analysis by itself. The frozen gate remains at least five independent programmes for a repeated layer pair.
