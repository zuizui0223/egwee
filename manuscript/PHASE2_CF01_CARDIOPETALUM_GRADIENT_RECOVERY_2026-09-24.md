# CFTQ0166 Cardiopetalum retrospective gradient recovery — 2026-09-24

## Admission

`P2_CF01_CARDIOPETALUM_2012` is admitted as **one retrospective gradient/generalisation I-F programme**.

The source Table 1 values and published directions were visible before the deterministic recovery rule was written. This is retrospective generalisation evidence, not prospective confirmation.

## Effect unit

- independent forest fragments: **10**
- independent unit: **forest fragment**
- marked plants / flowers / beetles / density plots / fruits / seeds: nested below fragment

## Locked variables

- fragmentation severity: **−log(fragment area ha)**; higher = smaller fragment
- I: pollinator abundance per flower (ABP)
- F: fruit set per flower (F)

## Primary effects

- I: r = **−0.240**, Fisher z = **−0.245**
- F: r = **−0.933**, Fisher z = **−1.684**
- marginal Fisher-z variance = **0.142857**

The interaction layer changes relatively weakly across fragment area, whereas realized reproductive function declines strongly toward smaller fragments.

## I-F response geometry

- residual rho(I,F) = **+0.169**
- working Cov(z_I,z_F) = **+0.024085**
- covariance determinant = **0.019828**
- I − F = **+1.439**
- SE = **0.487**
- 95% CI = **[+0.483, +2.394]**
- two-sided p = **0.00316**

The interval excludes zero. Under this retrospective fragment-area recovery, pollinator abundance and reproductive function are **non-exchangeable**: reproduction deteriorates much more strongly than the measured beetle-pollinator abundance.

## Sensitivities

On the source table:

- follicle set per flower: Fisher z = **−0.941** (n=10)
- seed set per flower: Fisher z = **−1.893** (n=9; F10 remains source-missing)
- isolation exposure, I: Fisher z = **−0.287**
- isolation exposure, F: Fisher z = **−1.279**

Both alternate reproductive endpoints retain substantially stronger negative fragment-area responses than I. The nearest-fragment-distance sensitivity also keeps F more negative than I. These are robustness descriptions, not substitutes for the locked primary endpoints.

## Ecological interpretation

This programme provides a direct natural example of **interaction persistence with reproductive collapse**. Beetle abundance in flowers is not sufficient to predict realized reproductive function across fragment sizes. Fragmentation can leave the observed pollinator-presence layer comparatively intact while local mating quality, pollen exchange, resource limitation, or other downstream reproductive constraints deteriorate.

This complements the Aextoxicon process anchor, where incoming seed movement can remain substantial despite low local fecundity.

## Scope

- gradient/generalisation programme increment: **+1**
- primary Fisher-z marginal effects: **+2**
- direct Hedges-g I-F increment: **0**
- Phase-1 five-cluster synthesis: unchanged
- EGWE/NEE finite-operator validation: none
