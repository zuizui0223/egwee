# CFTQ0324 Erica discolor 20-patch I-F gate — 2026-09-27

## Programme

Programme identity: `P2_CF01_ERICA_ANGOH_2016`.

Primary public sources:

- Angoh (2016), MSc thesis, University of Cape Town;
- Angoh, Midgley & Brown (2021), *South African Journal of Botany*,
  doi:10.1016/j.sajb.2021.05.012.

## Effect unit is valid

The thesis defines **20 fynbos habitat patches**.

Appendix A tabulates for each patch:

- patch ID/name;
- patch area;
- distance to the nearest large patch;
- coordinates;
- surrounding fragmentation matrix.

Patch identity is therefore source-recoverable and independent of the biological response.

Within each patch, plants, flowers and fruits are nested observations.

## I and F are biologically aligned

For *Erica discolor* the thesis measures:

- I: proportion of flowers with evidence of pollinator visitation / disturbed anther rings;
- F: proportion of viable seeds in naturally pollinated ripe fruits.

The visitation GLMM includes patch ID as a random intercept to account for the ten sampled plants per
patch. Seed set is likewise collected across the same 20-patch programme.

## Public-data boundary

The source patch-response values are not tabulated.

- Figure 7 shows mean visited flowers per plant per patch against patch area, with SE bars.
- Figure 8 shows viable seed proportion against patch area for the 20 patches.
- Figure 9 summarizes the <100-ha versus >240-ha seed-set groups.

Thus Appendix A supplies the exposure vector, but the I and F vectors required for one common
20-patch Fisher-z recovery remain graphical.

The 2021 primary article confirms the same result pattern but does not expose a public raw
20-patch response table.

## Terminal status

`blocked_20patch_IF_response_vectors_only_graphically_reported_no_digitization`

Direct I-F programme increment: **0**.

This is an effect-recoverability boundary, not an ecological null. The system remains one of the
cleanest natural examples in the search of pollination and reproductive function persisting across
small fragmented habitat patches.

## Reopening condition

Reopen only if an authoritative source supplies the patch-level:

1. patch ID / area or isolation;
2. visitation proxy;
3. viable seed set.

Then retain habitat patch as n and reconstruct the common gradient/dependence without re-selecting the
exposure from effect strength.

## No rescue

Do not:

- digitize Figures 7 or 8;
- use ten plants per patch as fragmentation n;
- use flowers or seeds as independent patches;
- infer exact patch values from the published GLMM or Wilcoxon statistics;
- dichotomize the gradient differently after seeing results;
- interpret the null patch-size trend as equivalence;
- use the source to validate a finite EGWE/NEE operator.
