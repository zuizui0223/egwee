# ML014 / Eucalyptus globulus 2009 cluster-recovery contract

## Goal

Attempt a fourth independent covariance-aware multilayer cluster from Mimura et al. (2009), *Molecular Ecology* 18:4180–4192, DOI `10.1111/j.1365-294X.2009.04350.x`.

The source compares four native populations under replicated landscape fragmentation: two continuous and two fragmented populations, paired across Tasmania and Victoria.

## Locked design

- independent unit: population;
- exposure: source-defined `fragmented` versus `continuous` forest;
- primary C endpoint: MLTR correlated paternity `r_p` in the offspring cohort, oriented so higher correlated paternity = lower mating/paternal diversity = worse connectivity support;
- primary G_offspring endpoint: offspring expected heterozygosity `H_E` (or the source's exact offspring gene-diversity notation if explicitly synonymous), oriented so lower diversity = worse genetic state;
- common frame: all four populations only if both endpoints are reported/reconstructable for all four;
- offspring, maternal trees and loci remain nested and never become fragmentation replicates.

No switch to outcrossing rate, effective density, adult diversity, pollen-kernel parameters, allelic richness or another genetic endpoint after values are inspected.

## Dependence requirement

If C and G_offspring are recoverable on the same four populations, reconstruct within-cluster dependence from the paired population-level values or source uncertainty where possible. Do not set covariance to zero merely because only four populations are available. With two groups and four populations, any working covariance may be rank-limited; retain pairwise covariance and use the existing low-dimensional/cluster-robust contract rather than manufacturing full rank.

## Source opening order

1. source metadata / full-text availability / supplementary-file schema;
2. verify population labels and fragmented/continuous assignment;
3. verify that `r_p` and offspring `H_E` are exposed at population level for all four populations;
4. only then recover numeric values and calculate the paired C/G_offspring contrast and covariance.

## No-rescue rules

Do not:

- treat Tasmania and Victoria as the only two independent observations while simultaneously counting their nested populations again;
- use maternal-family or offspring counts as landscape n;
- substitute adult genetic diversity for offspring H_E;
- substitute outcrossing rate or pollen dispersal distance for r_p after seeing values;
- collapse the two fragmented populations because their mating patterns are heterogeneous;
- drop one fragmented population to strengthen direction;
- infer missing H_E values from the abstract phrase `little evidence of loss of genetic diversity`;
- use p-values or ranges without a signed population-level estimate.

## Terminal outcomes

- `ML014_admitted_C_Goffspring_covariance_aware`;
- `population_level_G_not_reconstructable`;
- `common_four_population_frame_not_reconstructable`;
- `covariance_not_reconstructable`;
- `source_access_blocked`.

All terminal outcomes are acceptable and retained.
