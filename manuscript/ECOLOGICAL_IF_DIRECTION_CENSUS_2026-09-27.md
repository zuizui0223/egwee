# Complete registered I–F direction census — 2026-09-27
## Status after the 2026-09-29 estimand-scale audit

This document is retained as **registered-scale exploratory provenance**. It is not a current scale-invariant manuscript claim.

The authoritative effect-scale interpretation is in `manuscript/ESTIMAND_SCALE_ROBUSTNESS_2026-09-29.md` and `manuscript/BOTTLENECK_SCALE_ROBUSTNESS_2026-09-29.md`. Hedges-g and lnRR give different system-specific magnitude/separation classifications. Any bottleneck, ordering or direction-census statement below must therefore be read as conditional on its declared effect representation.


## Question

Across every currently registered EGWEE programme that contains both an interaction/pollen-quantity response (I) and reproductive function (F), what direction is taken by a **resolved** within-programme I–F mismatch?

This is a descriptive census of the complete registered I–F programme set. It is **not** a new pooled meta-analysis, sign test, prevalence estimate or preregistered directional hypothesis.

## Programme denominator

Eight independent programmes currently carry eligible I and F information.

Seven permit a covariance-aware or otherwise registered within-programme I–F comparison:

1. Aizen–Feinsinger Chaco / ML020;
2. Sevenello edge–core annual forbs;
3. Bergsdorf Kakamega;
4. *Eucalyptus wandoo* / ML015;
5. *Cardiopetalum calophyllum*;
6. Zurich BetterBlooms;
7. Toronto common milkweed.

The eighth, Pritchard custard-apple orchard isolation, has valid marginal I and F gradients but no reconstructable paired covariance. It is retained as **not testable**, not assigned to either direction.

## Result

Among the **7 pair-testable programmes**:

- **3** contain a within-programme I–F mismatch that remains resolved under the programme's registered multiplicity rule;
- **4** do not resolve an I–F mismatch;
- **all 3 resolved programmes have F more negative than I**;
- **0** programmes resolve the opposite direction (I more negative than F).

The three resolved programmes are:

| programme | effect family | ecological geometry | programme-adjusted evidence |
|---|---|---|---:|
| *Eucalyptus wandoo* | Fisher-z gradient | pollen tubes increase while seed production declines | p = 0.00256953 |
| *Cardiopetalum calophyllum* | Fisher-z gradient | pollinator abundance changes weakly while fruit set declines strongly | p = 0.00315990 |
| Kakamega *Acanthopale pubescens* programme | direct Hedges g | visitation occurrence is maintained/slightly higher while fruit set is lower | p = 0.00653539 |

The four pair-testable unresolved programmes are Chaco, Sevenello, Zurich and common milkweed.

## Why this is ecologically interesting

The directional asymmetry is narrower than saying that fragmentation universally reduces pollinators.

In every registered programme where an I–F mismatch is actually resolved, the reproductive response is the more negative component. No registered programme currently resolves a case in which interaction/pollen quantity deteriorates more strongly than reproductive function.

This is compatible with a life-cycle bottleneck downstream of interaction quantity: pollen quality, compatible-mate availability, mating structure, heterospecific or self pollen, resource limitation, or other post-visitation processes can reduce realised reproduction even when visits or pollen quantity remain comparatively intact.

The present data do **not** identify which mechanism is responsible.

## Counterevidence retained

The direction census does not erase programmes without decoupling.

- Chaco shows both I and F declining without a resolved difference (p_ML020 = 1.0).
- Sevenello has three primary I–F panels with no resolved mismatch (programme p = 1.0).
- Zurich has four phytometer I–F panels and none resolves a difference after the programme-level multiplicity accounting.
- Common milkweed has opposite-direction marginal I and F gradients, but the covariance-aware interval crosses zero.
- Pritchard is not testable for an I–F difference because paired covariance cannot be reconstructed.

Thus the supported ecological statement is not that quantity–function decoupling is universal.

## Claim ceiling

> **Resolved interaction–function decoupling in the current complete registered programme census is directionally asymmetric: all resolved cases show reproductive function deteriorating more than measured interaction/pollen quantity.**

This is a descriptive property of the current audited corpus.

Do not convert 3/3 into a binomial/significance test, estimate its global prevalence, or claim a universal causal mechanism. The programmes differ in taxa, fragmentation exposure, effect family and retrospective/prospective status.

The machine-readable census is `evidence/meta_extraction/ecological_if_programme_census_v1.csv`; its source-backed validation is `scripts/check_ecological_if_programme_census.py`.
