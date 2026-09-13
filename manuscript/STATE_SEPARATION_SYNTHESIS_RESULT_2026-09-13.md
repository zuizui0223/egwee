# EGWEE formal state-separation synthesis — result

**Date:** 2026-09-13

## Terminal result

`reject_general_layer_exchangeability`

The synthesis combines four independent covariance-aware multilayer fragmentation clusters without pooling their effect magnitudes across incompatible effect families.

### Cluster-level tests

| cluster | system | admitted layers | Bonferroni cluster p | interpretation |
|---|---|---|---:|---|
| ML001 | *Serapias lingua* | C / F / G_adult | 0.00354530 | clear within-system non-exchangeability |
| ML002 | *Brosimum alicastrum* | C / F | 0.19911670 | no individual-cluster rejection |
| ML003 | *Spondias purpurea* | C / G_adult / G_juvenile / G_seed | 0.17406774 | no individual-cluster rejection after six-pair correction |
| ML015 | *Eucalyptus wandoo* | I / F / G_adult | 0.00786120 | clear within-system non-exchangeability |

The strongest ML015 contrast is I pollen tubes versus F seeds per fruit: difference = 1.46930718 standardized-slope units, SE = 0.48829117, z = 3.00908, two-sided p = 0.00262040. The same fragmentation severity is associated with increased pollen-tube quantity but reduced seed production.

The strongest ML001 contrast is F fruit set versus G_adult H_O: difference = 21.51837567 Hedges-g units, SE = 6.63482966, z = 3.24324, two-sided p = 0.00118177.

### Cross-cluster synthesis

Fisher combination of the four independent cluster-level Bonferroni p-values gives:

- Fisher statistic: **27.70024526**
- df: **8**
- combined p: **0.0005347329**

Therefore the current natural-system corpus rejects the general layer-exchangeability null at the formal synthesis level.

## What this means

The supported statement is:

> biological responses measured under fragmentation cannot generally be treated as exchangeable manifestations of a single scalar deterioration state.

This result is stronger than noting that different studies report different effect sizes. Each cluster tests multiple layers on a shared fragmentation exposure while preserving within-system dependence, and the cross-system synthesis combines only cluster-level evidence.

## What this does not mean

- It does not establish one universal ordering of C, I, F or G.
- It does not imply that every cluster individually shows significant state separation.
- It does not numerically pool binary Hedges-g effects with standardized gradient slopes.
- It does not validate EGWE's finite-model operator ordering or strongest-refuge predictor in nature.
- It is not a prospective validation; the four-cluster corpus existed before this formal synthesis was defined.

## Audit trail

Method is fixed in `META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-13_STATE_SEPARATION_SYNTHESIS.md`.

Canonical executable is `scripts/synthesize_state_separation.py`.

GitHub Actions workflow `State separation synthesis` reproduced the complete calculation from repository evidence with no manual numerical inputs to the final test.
