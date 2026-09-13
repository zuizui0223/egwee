# ML013 / *Swietenia humilis* 2011 effect-unit audit

## Decision

Terminal state: `single_continuous_reference_population_no_replication`.

The 2011 Biological Conservation study is strong same-study biological evidence for multilayer fragmentation consequences, but it is **not** admitted as a fourth covariance-aware EGWEE cluster under the existing effect-unit contract.

## Source geometry

Rosas et al. (2011), DOI `10.1016/j.biocon.2011.10.003`, compare contemporary pollen flow and genetic diversity between a large continuous-forest control and surrounding isolated/remnant populations of *Swietenia humilis*.

The source reports adult genotypes from six populations and identifies a single forest population (`S`) as the continuous-forest population, with the remaining sampled populations representing isolated/remnant conditions. Thus the binary fragmentation exposure has only one independent continuous reference population.

Maternal trees, progeny, pollen donors, microsatellite loci and pollen-pool observations are nested below population/habitat exposure and cannot be promoted to independent continuous-forest replicates.

## Multilayer signal retained as programme evidence

The published study reports strong, directionally concordant habitat summaries:

- progeny allelic richness: isolated = 6.1 vs continuous forest = 8.3 alleles per locus;
- pollen-pool structure: `Phi_Iso = 0.26` vs `Phi_For = 0.14`;
- effective pollen donors: `N_ep = 1.9` in isolated stands vs 3.6 in continuous forest;
- estimated sires per mother: 4.98 in isolated trees vs 9.8 in forest trees.

These support the biological interpretation that donor diversity and offspring genetic diversity are lower under fragmentation even though long-distance pollen movement persists.

These habitat summaries are not converted into primary Hedges-g effects because the fragmentation-level reference denominator is one population. Group-level maternal-tree or progeny sample sizes are not valid substitutes for independent habitat replication.

## Why this is not the same as a biological null

This closure concerns effect-unit identifiability/replication, not direction or strength of the biological result. The source itself provides multilayer concordance. EGWEE simply cannot assign a fragmentation-level sampling variance compatible with the current replicated-cluster contract from one continuous reference population.

## Reopen condition

Reopen quantitative cluster admission only if an effect-unit-valid representation supplies at least two independent continuous-reference populations under the same campaign/endpoint definitions, or if a prospectively justified hierarchical estimand is introduced that treats the original sampling structure without using nested maternal trees/progeny as habitat n.

Until then ML013 remains programme-level qualitative/descriptive evidence with zero admissible primary effects.
