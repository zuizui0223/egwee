# ML008 / PS012 Tillandsia 2018 cluster audit result

## Terminal state

`signed_effect_and_covariance_not_reconstructable`

No primary I/F effect was admitted.

## What is source-supported

Sáyago et al. (2018) sampled each focal species at three continuous and three fragmented forest sites, with plants and years nested below site. The primary habitat tests therefore have an effect-unit-valid denominator for the landscape contrast:

- T. intermedia pollinator visitation: F(1,4)=3.7, P=0.13;
- T. makoyana pollinator visitation: F(1,4)=0.03, P=0.86;
- T. intermedia fruit set: F(1,4)=2.2, P=0.22;
- T. makoyana fruit set: F(1,4)=0.25, P=0.64.

The source text notes a trend toward higher visitation in fragmented forest, especially for T. intermedia, but does not provide a complete signed habitat coefficient/SE set for every species-layer pair.

The 2011 seed-set analysis is not substituted as primary F. Although T. makoyana seed set is lower in fragmented forest (continuous 86±2.4%, fragmented 77±4.1%; F(1,60)=4.3, P<0.05), that simple ANOVA uses individual-plant replication rather than the six-site fragmentation frame.

## Why F(1,4) is not enough for admission

With df1=1, the reported F statistics can be transformed into unsigned test-statistic magnitudes. That does not solve two required quantities:

1. a signed, source-scale habitat contrast with uncertainty for every I/F endpoint;
2. the within-study I/F dependence induced by shared sites, years and habitat assignment.

The publication provides neither paired site-level I/F summaries nor a model covariance that identifies this dependence. Setting covariance to zero would violate the multilayer contract.

Figure 3 contains back-transformed habitat/year predictions, but it is not digitized to manufacture site-level effects or covariance.

## Biological information retained without quantitative promotion

Both species show comparable pollinator visitation and fruit set between habitat conditions in the source tests. Pollinator composition changes strongly in T. intermedia, and T. makoyana shows lower 2011 seed set under fragmentation. This remains useful mechanistic evidence that interaction composition and downstream seed quality can change even when visitation rate and fruit set do not show the same habitat contrast.

## Reopen condition

Reopen ML008 if exact site-level summaries, raw data, or signed model contrast estimates with sufficient dependence information become available. Preserve the six-site effect unit and do not promote plant-level seed-set replication to the fragmentation level.
