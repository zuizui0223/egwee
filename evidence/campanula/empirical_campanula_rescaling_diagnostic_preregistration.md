# Predictor-only diagnostic — Campanula effective-interaction rescaling

## Purpose

PR #114 returned `no_interaction_representation_supported` and, critically, `M_phase` and `M_effective` were identical to machine precision under the preregistered StandardScaler + Ridge pipeline.

This diagnostic tests one narrow, outcome-independent explanation:

> Are the six source-defined effective pollen-transfer coordinates constant positive scalar multiples of their corresponding phase-matched visitation coordinates across the 23 populations, such that feature-wise standardization removes the efficiency multipliers exactly?

This diagnostic **cannot change the #114 decision**. It exists only to determine whether the observed M_phase/M_effective equivalence follows from the predictor representation itself.

## Source lock

Same immutable source as #114:

- Koski et al. (2018)
- Dryad doi:`10.5061/dryad.5nj81nf`
- Zenodo record `4969330`
- file `Koski et al. 2018_Data_ProcRoySoc.xlsx`
- MD5 `2d26307743e8a22384781854b8f2f33b`
- SHA-256 `b81b77248b75330049e1ddd8ae026db127f838e979620a0415a5addb9a7e8f27`
- sheet `PopVis Rates_ PL_Depletion`
- exactly 23 population rows

## Response firewall

The diagnostic must not read, parse, summarize, correlate with, model, or otherwise access numeric values from `Pollen Limitation 2016` or any other outcome column.

The workbook header may be read only to locate the predictor columns below. Numeric cell reads are restricted to the twelve declared predictor columns.

## Fixed predictor pairs

Deposition / female-phase pairs:

1. `Bumble Female Rate` -> `Bumble Grains Dep Per Hour`
2. `Megachile Female Rate` -> `Mega Grains Dep Per Hour`
3. `Small Female Rate` -> `Small Grains Dep Per Hour`

Removal / male-phase pairs:

4. `Bumble Male Rate` -> `Bumble Grains Rem Per Hour`
5. `Megachile Male Rate` -> `Mega Grains Rem Per Hour`
6. `Small Male Rate` -> `Small Grains Rem Per Hour`

No pair may be added, removed, swapped, or selected after seeing ratios.

## Fixed diagnostics

For each pair `(x, y)`:

1. For every row with `x != 0`, calculate `r_i = y_i / x_i`.
2. Let `r_med` be the median finite ratio.
3. Report the minimum and maximum ratio and maximum relative deviation `max(|r_i-r_med| / max(|r_med|, 1e-15))`.
4. For rows with `x == 0`, verify whether `y == 0`.
5. Independently z-standardize `x` and `y` over the same 23 population rows using population standard deviation (`ddof=0`) and report maximum absolute z-score difference.

No response-based statistic is permitted.

## Fixed decision rule

A pair is `constant_rescaling_confirmed` only if:

- at least two finite nonzero-source ratios exist;
- median ratio is positive;
- maximum relative ratio deviation <= `1e-10`;
- every zero source row has zero effective value; and
- maximum absolute difference after independent z-standardization <= `1e-10`.

Campaign decision:

- **`constant_rescaling_confirmed`**: all six pairs satisfy the rule;
- **`not_constant_rescaling`**: the locked source is readable but one or more pairs fail;
- **`not_identifiable`**: source hash, predictor columns, row count or finite numeric predictor requirements fail.

All outcomes are acceptable.

## Interpretation ceiling

If confirmed, the supported statement is only:

> Under the #114 source representation, each effective coordinate is a constant positive rescaling of its matched phase-visitation coordinate across populations, and independent feature-wise standardization makes those paired coordinates numerically equivalent.

This does not show that per-visit efficiency is biologically irrelevant. It shows that the specific #114 preprocessing representation could not preserve constant efficiency weights.

If not confirmed, the machine-precision model equivalence remains unexplained by this simple rescaling hypothesis and must not be repaired by reopening #114.

## Stop rule

Do not inspect `Pollen Limitation 2016`, rerun the #114 outcome model, construct summed fluxes, change scaling, or test alternative predictor subsets in this campaign.
