# Protocol amendment — continuous fragmentation geometry

**Date:** 2026-09-11  
**Stage:** after primary-study screening began, before any pooled meta-analytic fit.

This amendment fixes the transform for positive, right-skewed geometric fragmentation variables before quantitative synthesis.

## Primary rule

For strictly positive habitat/population area variables used as an externally defined fragmentation exposure, use

`fragmentation_severity = -log(area)`.

For strictly positive separation/isolation distances where larger values mean greater fragmentation, use

`fragmentation_severity = log(distance)`.

Reported Pearson correlations with the transformed exposure are converted to Fisher `z(r)` for the continuous-gradient stream. If only population-level raw values are published, the correlation may be reconstructed from those published values using the same transform.

## Sensitivity rule

For transparency, retain the corresponding untransformed area/distance correlation as a sensitivity effect when it can be reconstructed from the same observations. The transformed and untransformed versions are alternative representations of the **same observation** and must never both enter the same pooled model.

## Eligibility boundary

- The geometric exposure must be defined independently of the biological outcome.
- Biological population size, abundance, floral display, visitation, reproduction or genetics cannot be relabelled as the fragmentation exposure merely because they covary with fragmentation.
- No transformation is selected separately by response layer or by which version gives the larger effect.

## Why this amendment exists

The first fully reconstructable gradient table (PS003, *Serapias lingua*) spans population areas from roughly 56 to 4585 m², making raw area strongly right-skewed. The transform rule is therefore fixed globally for all eligible area-gradient studies before any pooled model or layer comparison is fitted.
