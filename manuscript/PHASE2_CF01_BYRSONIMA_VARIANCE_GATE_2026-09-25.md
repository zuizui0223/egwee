# CFTQ0209 Byrsonima sericea direct I-F variance gate — 2026-09-25

## Candidate

Programme identity: `P2_CF01_BYRSONIMA_2009`.

Primary source: Dunley, Freitas & Galetto (2009), *Biotropica*,
doi:10.1111/j.1744-7429.2009.00524.x.

The habitat contrast is strong and simple:

- small fragments: SF1 = 0.22 ha, SF2 = 0.07 ha, SF3 = 0.28 ha;
- large fragments: LF1 = 36 ha, LF2 = 14 ha, LF3 = 99 ha.

The source equalizes pollinator-observation effort at 160 min per fragment and measures natural fruit
set in the same six-fragment system.

## Published response summaries

The source reports class summaries for:

- pollinator visit frequency: small 1.16 ± 0.16, large 0.54 ± 0.19;
- natural fruit set: small 34.7 ± 9.3%, large 26.7 ± 15.2%.

Those values make the biological contrast attractive, but they are not sufficient by themselves for
EGWEE admission.

## Effect-unit problem

The source's statistical methods explicitly state that:

- visit frequency and fruit set are measured at **individual-plant level**;
- sampled individuals are **nested within each fragment**;
- repeated observation periods, racemes, flowers and fruits are below individual/fragment.

The public article does not expose:

- six fragment-level visitation means;
- six fragment-level natural-fruit-set means;
- an unambiguous statement that the reported class SDs are **between-fragment** SDs rather than
  dispersion from the nested analysis;
- paired six-fragment I/F values from which within-cluster dependence can be reconstructed.

Therefore attaching `n=3+3` to the published class SDs is not certified.

## Decision

Status: **design-valid direct I-F candidate, quantitatively blocked by fragmentation-unit marginal
variance and dependence recoverability**.

No Hedges-g effect is admitted. Direct I-F coverage remains unchanged.

The frozen multilayer protocol does allow a cluster-robust fallback when dependence is known but the
covariance is unavailable. That fallback cannot rescue this case yet because the **marginal
fragment-level sampling variances themselves are not certified**.

## Reopening condition

Reopen if either:

1. the six fragment-level I and F summaries are obtained; or
2. an authoritative source explicitly confirms that the published class SDs are the SDs of the
   three fragment-level means per class.

If marginal effects become admissible but paired covariance remains unavailable, keep the two effects
in one cluster and use the pre-existing cluster-robust dependence fallback; never set covariance to
zero by convenience.

## No rescue

Do not:

- use focal plants as `n`;
- use 20-min observation intervals as `n`;
- use racemes, flowers or fruits as fragmentation replicates;
- assign `n=3` to the published SD without confirming its level;
- infer within-cluster covariance from class means;
- digitize class figures to invent fragment-specific values.

All terminal outcomes are retained.
