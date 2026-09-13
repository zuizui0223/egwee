# ML015 / PS019 Eucalyptus wandoo 2018 recovery result

## Terminal state

`ML015_gradient_generalisation_I_F_Gadult_covariance_aware`

ML015 is retained as a three-layer **Fisher-z gradient generalisation cluster**. It is not a fourth primary Hedges-g cluster and does not increase the primary confirmatory denominator.

## Why the tier changed

The frozen meta-analysis protocol separates direct fragmented-versus-reference comparisons from continuous fragmentation gradients. The original ML015 recovery used standardized OLS slopes, which are not one of the frozen effect streams. In addition, the response-free PC1 is an EGWEE composite of three source fragmentation descriptors rather than a scalar contrast defined by the source.

The recovery was therefore returned to the pre-existing `fisher_z_gradient` stream rather than relaxing the protocol after seeing the result.

## Locked frame

- 19 source populations define the exposure geometry;
- 11 populations have all three response layers: `J,K,F,C,E,G,B,I,A,H,D`;
- independent unit = population;
- composite gradient = response-free PC1 of `-log10(size)`, `sqrt(isolation)`, `log10(shape)`;
- layers = pollen tubes (`I`), seeds/fruit y2 (`F`), adult `H_e` (`G_adult`).

The public source tables were visible during candidate discovery; this analysis is transparently source-discovery-exposed rather than called an outcome-blind preregistration.

## Fragmentation PC

Severity-oriented PC1 loadings are:

- smallness: `+0.5873571692`;
- isolation: `+0.4775526468`;
- edge dominance: `+0.6534179561`.

PC1 eigenvalue = `1.8276073487`. Larger score therefore represents smaller, more isolated, more edge-dominated populations.

## Canonical gradient effects

Using the frozen Fisher-z effect representation on the common 11-population frame (`V(z)=1/(11-3)=0.125`):

- `I_pollination`: `r=+0.59816906`, `z=+0.69029123`;
- `F_reproductive_function`: `r=-0.70437490`, `z=-0.87593080`;
- `G_adult`: `r=-0.38946811`, `z=-0.41117288`.

The qualitative geometry from the initial slope calculation is unchanged: pollen quantity increases along this composite fragmentation gradient while realised seed production declines; adult standing heterozygosity is weaker but points in the same deterioration direction as F.

The source independently reports the same biological tension: smaller populations received more pollen tubes while seed set was reduced, and the authors discuss pollen quality/self-pollen rather than pollen quantity as a plausible explanation.

## Dependence

The three effects share the same 11 populations. After fitting each raw endpoint on the fixed severity score, the residual-correlation proxy is:

```
[[ 1.0000000000,  0.1171782316, -0.3694768285],
 [ 0.1171782316,  1.0000000000, -0.1025244764],
 [-0.3694768285, -0.1025244764,  1.0000000000]]
```

Combining this with the three canonical Fisher-z marginal variances (`0.125`) gives the working covariance matrix:

```
[[ 0.1250000000,  0.0146472789, -0.0461846036],
 [ 0.0146472789,  0.1250000000, -0.0128155595],
 [-0.0461846036, -0.0128155595,  0.1250000000]]
```

Eigenvalues are `0.07877559, 0.11795799, 0.17826642`; the proxy matrix is positive definite.

## Synthesis boundary

ML015 adds **zero primary Hedges-g effects**. The primary confirmatory denominator remains ML001–ML003, totaling 3 independent clusters / 9 primary effects.

The three ML015 rows are `fisher_z_admissible` only in the separately analysed gradient/generalisation stream. Hedges g and Fisher z are not pooled on one effect scale.

Thus ML015 strengthens the external/generalisation evidence for cross-layer state separation, but it is not used to claim that the primary replicated binary/contrast synthesis has grown from three to four systems.