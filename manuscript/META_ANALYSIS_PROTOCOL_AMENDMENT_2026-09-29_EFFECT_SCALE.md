# Meta-analysis protocol amendment — effect-scale interpretation

**Date:** 2026-09-29

## Status

This is a **post hoc protocol amendment** written after both the Hedges-g and lnRR sensitivity results were inspected.

It does not retroactively make lnRR preregistered. Its purpose is to prevent a scale-specific result from being presented as a scale-general ecological conclusion.

## Why the amendment is necessary

The primary direct analysis was defined on endpoint-specific Hedges-g scales. Hedges g standardizes each endpoint by its own within-group dispersion. In ML001 *Serapias*, adult H_O has exceptionally small between-population SD, producing a very large standardized effect.

A post hoc lnRR reconstruction using the same independent units changes both endpoint magnitude ordering and the leave-one-cluster-out conclusion:

- g omit-ML001 Fisher p = 0.1819435;
- lnRR omit-ML001 Fisher p < 0.005 under both raw-unit delta covariance and zero-covariance sensitivity.

Therefore equality/non-equality of layer effects is not invariant to effect-scale choice.

## Revised estimand hierarchy

### 1. Primary historical estimand

The original Hedges-g analysis remains the historical primary calculation and is reported transparently as such.

It answers:

> Are standardized fragmentation effects equal when each endpoint is expressed in units of its own pooled within-group SD?

This question is statistically legitimate but not scale invariant.

### 2. Mandatory scale sensitivity

For positive-valued endpoints, lnRR is reported as a mandatory sensitivity representation:

> What is the proportional fragmented/reference response after orientation to biological support?

lnRR is not promoted to a new preregistered primary endpoint.

### 3. Cross-scale claim rule

A paper-level biological claim about relative response magnitude, ordering, influential systems or robustness may be called **scale robust** only if its qualitative interpretation agrees between g and lnRR.

If g and lnRR disagree, the manuscript reports the disagreement and does not choose the scale that yields the preferred conclusion.

### 4. Sign-only qualitative evidence

Sign direction is treated separately from magnitude ordering. Because all 17 primary effects are negative on both g and lnRR, the scale-stable direct-stream conclusion is broad deterioration across admitted responses.

No sign test treats the 17 dependent endpoint effects as independent studies.

## Consequence for existing claims

Demoted:

- “state separation is Serapias-dependent and not robust” as a general ecological headline;
- Hedges-g magnitude rankings as biological severity rankings;
- ML001 C–F separation as scale-general.

Retained with explicit scale label:

- canonical g Fisher p = 0.0121243;
- g omit-ML001 p = 0.1819435;
- covariance and influence diagnostics on the g scale.

Added as sensitivity:

- lnRR full and omit-ML001 Fisher results;
- ML001 rank reversal;
- 17/17 cross-scale sign concordance.

## Relation to exploratory ecology

Any upstream→downstream attenuation / buffering pattern inferred from lnRR is exploratory because it was recognized after outcome inspection. It may motivate the fresh Q→E→F programme but must not be presented as a confirmed current-corpus law.
