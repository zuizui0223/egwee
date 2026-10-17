# CF01_GPAIR_003 / Prunus africana Kakamega 2008 Phase-2 recovery contract

**Locked:** 2026-09-19 before EGWEE effect rows are written for this programme.

## Source and audit status

Source: Farwig, Braun & Böhning-Gaese (2008), *Human disturbance reduces genetic diversity of an endangered tropical tree, Prunus africana (Rosaceae)*, Conservation Genetics 9:317–326, doi:10.1007/s10592-007-9343-x.

This is a **retrospective external recovery**. The publicly indexed full-text Table 2 was visible during candidate discovery. No prospective outcome-blind claim is made. The safeguard is a fixed source-defined exposure, one matched endpoint in both cohorts, retention of all eight sites, and deterministic calculation independent of effect direction or significance.

This Kenyan Kakamega programme is geographically and observationally independent of CF01_GPAIR_002, the Ethiopian Yineger et al. 2014 *P. africana* programme.

## Target pair

Primary Phase-2 family: `G_adult-G_offspring`.

The source explicitly sampled adults (80–100 years old) and seedlings (1–5 years old) in the same eight sites so that the two generations are spatially matched within site.

## Exposure and independent unit

Primary exposure = source-defined forest context:

- fragmented = fragment sites: **Malava, Kisere, Ikuywa, Kaimosi**;
- reference = main-forest sites: **Mukangu, Buyangu, Isecheno B, Isecheno A**.

Independent fragmentation unit = **site/population**.

Thus:

- `n_fragmented = 4`;
- `n_reference = 4`.

Adult trees, seedlings, microsatellite loci, alleles and the within-site adult–seedling pairing are nested observations and never increase fragmentation-level n.

The paper also discusses local selective logging/disturbance. Those attributes are retained as contextual/moderator information and do not replace the predeclared binary main-forest versus fragment exposure after outcome inspection.

## Locked genetic endpoint

Primary endpoint in both cohorts = Table-2 Nei mean expected heterozygosity `H_E`.

Rationale:
- identical population-level metric is available for every site in both cohorts;
- expected heterozygosity is an established G-state endpoint in the EGWEE Phase-2 recovery family;
- using the same metric in both generations avoids cross-metric conversion.

Orientation multiplier = `+1`: larger `H_E` means greater genetic support.

Observed heterozygosity `H_O`, allelic richness, allele number, inbreeding coefficient and population-specific differentiation remain sensitivity/descriptive quantities and cannot replace `H_E` because they yield a more convenient pair result.

## Direct effect calculation

For each cohort use the canonical direct EGWEE Hedges-g estimator:

- `d = (M_frag - M_ref) / s_p`;
- `df = n_frag + n_ref - 2`;
- `J = 1 - 3/(4df - 1)`;
- `g = Jd`;
- `V(g) = 1/n_frag + 1/n_ref + g^2/[2(n_frag+n_ref)]`.

Dispersion is between independent site-level `H_E` values within forest context. Individual sample counts do not enter fragmentation-level n.

## Paired dependence

Adult and seedling `H_E` values share the same eight sites.

Dependence is reconstructed with the declared paired-unit proxy:
1. subtract the fragment/main-forest group mean from each site value within each cohort;
2. calculate the Pearson correlation between adult and seedling residuals;
3. set `Cov = rho sqrt(V_adult V_seedling)`;
4. calculate the primary pair difference `G_adult - G_offspring` and its variance directly.

## Admission

This programme contributes exactly one independent programme to the Phase-2 G-pair family if:
- all eight Table-2 rows are reproduced exactly;
- all four source fragment and four main-forest sites are retained;
- population/site remains the independent unit;
- both Hedges-g effects and the paired covariance are deterministic;
- the 2×2 covariance block is positive definite.

It does not enter or modify the frozen Phase-1 five-cluster Fisher synthesis.
