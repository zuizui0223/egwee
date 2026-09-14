# ML016 / PS021 Swietenia macrophylla 2012 recovery result

## Terminal state

`family_level_mating_effect_and_dependence_not_reconstructable`

ML016 does **not** become a fifth primary multilayer cluster. It adds zero primary effects. The primary denominator remains **4 independent clusters / 11 primary effects**.

## What was recovered

The source provides strong directional evidence under its source-defined local landscape context:

- forest families: correlated paternity `r_p = 0.163`, growth `0.060`;
- isolated families: `r_p = 0.341`, growth `0.048`.

Higher `r_p` implies fewer effective pollen donors, so both source summaries point toward deterioration under isolation: lower pollen-donor diversity and lower five-year progeny growth.

The source also reports the same directional comparison separately within mesic and dry provenance. Those strata were prospectively retained as heterogeneity sensitivity and are not counted as additional systems.

## Why no primary Hedges-g effect is manufactured

The mating-system values in Table 1 are group-level MLTR estimates. The source methods state that, for provenance / isolation-context / population group estimates, maternal families were bootstrapped 1000 times to estimate mating-parameter variance. Therefore the reported parenthetical uncertainty for `r_p` is not a between-family sample SD that can be combined with `n_family = 47` forest and `24` isolated in the canonical Hedges-g formula.

Using those family counts with the bootstrap uncertainty would mix incompatible levels of representation and would violate the frozen effect-unit firewall.

The public supporting information does not repair this representation boundary:

- Appendix S3 explicitly describes family-level GLM slope bootstraps and population-level trend analyses;
- its tables expose regression summaries / population-level correlations rather than a keyed family table containing context, provenance, family `r_p`, and family growth;
- no public family-ID vector for `r_p` is exposed that can be joined to the family growth vector.

Accordingly, ML016 stores the source group summaries as `descriptive_only` and does not create a `g_admissible` row for either layer.

## Dependence gate

The prospective contract required paired family-level `r_p` and growth values so the G_mating/F covariance could be reconstructed after centering within the four context × provenance cells.

That paired representation is not publicly recoverable. The following rescue routes are forbidden and were not used:

- setting covariance to zero;
- back-solving covariance from Table 2 percent deviance explained / regression slopes;
- substituting Appendix S3 population-level correlations for family-level covariance;
- digitizing Figure 3;
- switching from `r_p` to another mating parameter after seeing results.

Therefore the covariance-aware admission gate fails by representation, not by biological direction.

## Interpretation

This study is biologically valuable supportive evidence: isolation is associated with higher correlated paternity and lower long-term progeny growth, with stronger disruption in mesic provenance. But the public representation does not permit the standardized family-level G_mating effect and paired cross-layer dependence required by the current primary meta-analysis contract.

This is a **representation boundary**, not a biological negative result.

## Reopening rule

Reopen ML016 only if a legitimate source family table becomes available with at least:

- maternal-family identifier;
- isolated/forest context;
- mesic/dry provenance;
- family-level `r_p`;
- family-level five-year growth.

If that table is obtained, use the already locked endpoints, all-family isolated-vs-forest Hedges-g contrast, provenance sensitivity, and paired context×provenance-centered covariance rule. Do not redesign the estimand after opening it.
