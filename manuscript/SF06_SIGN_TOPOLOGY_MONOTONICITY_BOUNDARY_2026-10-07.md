# SF06 sign-topology monotonicity boundary — INVALIDATED BY SIGN-PARSER BUG (2026-10-07)

## Status

This note preserves an **invalidated inference** for auditability.

The original argument concluded that the stricter constituent-sign topology could not become non-identifying because an earlier IVW-Hedges-d sign map had zero mismatches. The subset/positive-weight monotonicity argument was mathematically correct **conditional on the earlier sign map being correct**.

That premise was false.

## Parser defect

The public SF06 Word file stores negative Hedges-d values with a space between sign and magnitude, for example:

- *Cardiopetalum calophyllum* female fitness: `- 1.733`;
- *Cardiopetalum calophyllum* pollination: `- 0.048`;
- *Spondias purpurea* pollination: `- 1.225`;
- *Spondias purpurea* female fitness: `- 0.796`.

The original `first_float()` regular expression only retained a minus sign when it directly touched the number. Thus `- 1.733` was parsed as `+1.733`.

Commit `800ccfa` corrected the parser and added explicit invariants for spaced minus signs.

## Corrected result

The corrected public-S1 habitat-fragmentation topology contains:

- 54 constituent-consensus pairs;
- 35 pollination-lower / fitness-lower;
- 9 pollination-lower / fitness-nonlower;
- 7 pollination-nonlower / fitness-lower;
- 3 pollination-nonlower / fitness-nonlower;
- minimum deterministic mismatches: **12/54**;
- publication leave-one-out minimum: **8**;
- species leave-one-out minimum: **11**.

After deleting every source publication overlapping the frozen EGWEE I–F map:

- 31 constituent-consensus pairs remain;
- minimum deterministic mismatches: **7/31**;
- publication leave-one-out minimum: **5**;
- species leave-one-out minimum: **6**.

Therefore the corrected result is:

> **external sign-translation non-identifiability supported within the accessible public-S1 subset.**

## Why the old monotonicity reasoning failed

Positive inverse-variance weights still cannot reverse a correctly parsed consensus sign. The error occurred **before** that reasoning: the earlier IVW sign map had already lost negative signs.

Once the source signs are parsed correctly, the premise “the full IVW map has zero mismatches” disappears. The corrected IVW-sign sensitivity itself has 12 mismatches, matching the constituent-consensus topology.

## Claim boundary

The invalidated zero-mismatch result remains in the repository for provenance and must not be cited as biology.

The corrected external result is still not a set of 12 individually resolved sign reversals: only three pairs have both endpoint signs marginally resolved at 95%, all concordant lower/lower. The supported claim is structural many-to-many point-sign translation with strong publication/species influence robustness, not 12 significant reversals.
