# ML008 / PS012 Tillandsia 2018 cluster-audit contract

## Goal
Assess whether Sáyago et al. (2018), DOI `10.1093/aobpla/ply038`, can add a covariance-aware `I/F` fragmentation cluster without promoting plant-level replication to site-level evidence.

## Locked frame
- One study cluster containing two dependent species outcomes: *Tillandsia intermedia* and *T. makoyana*.
- Primary exposure: continuous versus fragmented forest.
- Independent fragmentation unit: site; each species has 3 continuous and 3 fragmented sites.
- Primary `I`: pollinator visitation rate across 2008–2010.
- Primary `F`: fruit set across 2009–2011, because its habitat test uses the same site-nested design and denominator df=4 as `I`.
- 2011 seed set is secondary only: the published simple ANOVA uses plant-level df=58/60 and cannot replace site-level F merely because *T. makoyana* is significant.

## Recoverability rule
For each species/layer, a quantitative primary effect requires a signed habitat contrast and uncertainty tied to the six-site frame. The reported `F(1,4)` statistic may be retained as a magnitude diagnostic, but nonsignificance is never coded as zero and an unreported sign is not guessed.

Cluster admission additionally requires within-study dependence for the I/F pair, preferably from paired site summaries/residuals or a source model covariance. Zero covariance is forbidden.

## No-rescue rules
Do not use plant counts as fragmentation n; do not promote the 2011 seed-set ANOVA to a six-site contrast; do not digitize Figure 3 to manufacture site means; do not infer signed effects from P-values; do not treat the two species as independent studies; do not set I/F covariance to zero.

## Terminal outcomes
- `ML008_admitted_I_F_site_covariance_aware`
- `signed_effect_not_reconstructable`
- `cross_layer_covariance_not_reconstructable`
- `source_access_blocked`
