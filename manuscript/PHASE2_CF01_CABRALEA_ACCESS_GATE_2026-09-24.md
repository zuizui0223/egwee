# CFTQ0124 Cabralea four-site I-F recovery gate — 2026-09-24

## Frozen target

Programme: `P2_CF01_CABRALEA_2015`.

The source sampled reproductive output in three fragmented and three continuous forest sites, but
direct pollinator visitation only in:

- fragmented: F1, F2;
- continuous: C1, C2.

The frozen paired I-F contract therefore limits the common independent-unit frame to these **four
forest sites**.

Primary I = pollinator visits per 30 min, aggregated to site.
Primary F = developed fruit number per sampled tree, aggregated to the same sites.

## Public-source audit

The open article provides:

- site identities and site characteristics;
- the F1/F2/C1/C2 pollinator sampling design;
- lower-level tree and 30-min observation replication;
- fragmentation-group means/dispersion and fitted GLMM test results.

It does **not** publish the site-level visitation and fruit-number summaries needed to form four
paired observations and reconstruct the registered I-F sampling covariance.

The group-level means cannot be combined with `n=2` sites per condition, because their reported
dispersion comes from lower-level biological/observation units rather than the fragmentation unit.

No numerical EGWEE Hedges-g effect was calculated.

## Decision

Status: **design-valid, quantitatively blocked by four-site effect-unit recoverability**.

This is not a null I-F result. The published study itself reports fragmentation-associated changes,
but those published lower-level/group summaries cannot be promoted into the registered independent
site-level meta-analytic effect.

## No rescue

Do not:

- use 25 trees/site as habitat n;
- use repeated 30-min observations as habitat n;
- attach group-level SD to `n=2` sites;
- combine the six-site F denominator with the four-site I denominator;
- digitize figures or reverse-engineer GLMM coefficients;
- switch to seed number/fruit, fruit weight, abortion or predation because they are more recoverable.

Reopen only if an authoritative source supplies F1/F2/C1/C2 site-level I and F values.
