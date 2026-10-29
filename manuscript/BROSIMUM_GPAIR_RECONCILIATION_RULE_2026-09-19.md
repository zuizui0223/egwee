# Brosimum adult-offspring genetic reconciliation rule — 2026-09-19

## Purpose

ML002 / *Brosimum alicastrum* already provides a valid 3-continuous versus 3-fragmented site design and public individual genotypes. It is **not** currently counted in the Phase-2 `G_adult-G_offspring` family because the first raw-genotype reconstruction of observed heterozygosity (`H_O`) failed to reproduce all four publication Table-2 habitat × cohort summaries.

This document fixes a reproducibility-only fallback before any site-level `H_E` effect is calculated.

## Frozen hierarchy

1. `H_O` remains the first attempted endpoint and remains failed for promotion.
2. A single fallback is allowed: source Table-2 expected heterozygosity `H_E`.
3. `H_E` can be promoted **only** if one transparent estimator, applied identically to all four habitat × cohort cells, reproduces the publication Table-2 `H_E` values at their reported two-decimal precision.
4. Candidate estimators are declared before site-level effect calculation:
   - locus-wise `H_E = 1 - Σp²` after pooling genotype rows within habitat × cohort, then equal-weight mean across the eight loci;
   - locus-wise unbiased `uH_E = (2N/(2N-1))H_E` under the same pooling;
   - equal-weight mean of site-level locus-wise `H_E`;
   - equal-weight mean of site-level locus-wise `uH_E`.
5. If none reproduces **all four** publication cells, Brosimum remains blocked and contributes no G-pair programme.
6. If more than one reproduces all four cells, use the simplest uncorrected `H_E` estimator among the matching estimators.
7. No estimator may be selected by the size, sign, significance, or pair-separation result of its site-level effect.

## Published targets fixed before fallback calculation

From Aguilar-Aguilar et al. (2023) Table 2:

- continuous adults `H_E = 0.65`;
- fragmented adults `H_E = 0.63`;
- continuous progeny `H_E = 0.59`;
- fragmented progeny `H_E = 0.60`.

These values are used only as reproducibility targets.

## Independent unit

The fragmentation independent unit remains site/population:

- continuous: CHA, CAR, CUI;
- fragmented: ASE, TEC, ZAP.

Adults, seedlings, loci, alleles and maternal families remain nested. Even if the fallback passes, Brosimum contributes one programme only.

## Anti-rescue rule

This reconciliation cannot alter the frozen Phase-1 ML002 effects or Fisher synthesis. Its only possible use is to determine whether the existing ML002 programme also contains a reproducible Phase-2 adult-offspring genetic pair. Failure leaves the current 4/5 G-pair coverage unchanged.
