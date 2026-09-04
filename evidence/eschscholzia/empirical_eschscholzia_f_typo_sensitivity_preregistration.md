# Post-review secondary Eschscholzia F typo sensitivity

## Status and non-rescue boundary

This is a prospective **secondary sensitivity** declared after the locked primary result and before fitting any repaired F model. The primary result remains permanently `multi_endpoint_not_identifiable`. This sensitivity cannot replace, rescue, relabel or enter the original F+G primary decision.

## Single permitted correction

Only one exact literal correction is permitted:

- source role: `f_seed`;
- array key: `1||3`;
- field: `Habitat`;
- observed value required before correction: `Fallow graound`;
- replacement: `Fallow ground`;
- required matching pollinator-source value: `Fallow ground`.

The run must stop if the exact key/value precondition is not met, if more than one distinct metadata discrepancy is present, or if any mismatch remains after the one correction. No fuzzy matching, edit-distance rule, majority vote or correction of another field/key is allowed.

## Frozen analysis

After the single correction, rerun only the already declared F analysis:

- response: `log1p(Mean_number_of_seeds_from_field_exposed_flowers)`;
- held-out unit: Experimental array, LOAO;
- S0/S1/S2 definitions unchanged;
- `Ridge(alpha=1.0)` unchanged;
- equal-array scoring unchanged;
- 10,000 array-bootstrap samples with RNG seed `20260825` unchanged;
- the existing `D_capacity` S2-to-S3 secondary extension unchanged.

No other endpoint is rerun. No source row is dropped or added. No pollinator metric, endpoint, regularization, seed, confidence level or decision threshold changes.

## Reporting rule

Report the F sensitivity with the literal label `postreview_secondary_typo_sensitivity`. Show the unchanged primary decision beside it. Accept any result. The sensitivity may indicate what the F model would have produced under the declared key-specific correction, but it cannot establish primary multi-endpoint convergence or insufficiency.
