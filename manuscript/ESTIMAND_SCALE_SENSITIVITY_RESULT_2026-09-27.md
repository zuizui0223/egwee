# Estimand-scale sensitivity result — 2026-09-27

## Main finding

The manuscript's original layer-separation robustness classification is **not invariant to effect-size scale**.

### Historical Hedges-g primary

- full five-cluster Fisher p = **0.01212432**;
- omit ML001 *Serapias* p = **0.18194353**.

On g, the full rejection is therefore not leave-one-cluster-out robust and is materially dependent on ML001.

### Oriented lnRR sensitivity

Using the same positive group summaries and delta-method variances:

| dependence treatment | full Fisher p | omit-ML001 Fisher p |
|---|---:|---:|
| existing dimensionless rho proxy carried to lnRR | ~1.18e-10 | ~2.92e-05 |
| zero covariance | ~1.72e-09 | ~0.00434 |
| covariance-free Cauchy maximum-variance boundary | ~9.95e-05 | ~0.111 |

Thus reasonable working lnRR analyses can retain rejection after ML001 is removed, whereas a covariance-free worst-case does not certify that rejection.

The correct conclusion is therefore not that lnRR proves robust separation. It is that **the robustness classification itself depends on estimand scale and dependence assumptions**.

## Serapias rank reversal

Primary group summaries give:

| layer | Hedges g | oriented lnRR |
|---|---:|---:|
| F fruit set | -4.554 | -1.102 |
| C pollen immigration | -10.099 | -1.157 |
| G adult H_O | -26.072 | -0.650 |

Absolute-magnitude ordering changes from:

`g: G > C > F`

to:

`lnRR: C > F > G`.

The Serapias C–F contrast is not resolved on lnRR under the carried rho proxy (`p ≈ 0.605`). The apparent upstream C-versus-F bottleneck used in the recent ecology framing is therefore not scale-stable.

## Other primary systems on lnRR

Exploratory oriented lnRR values reproduce the biologically interpretable gradients noted in the audit:

- ML002 *Brosimum*: C ≈ -0.537; F ≈ -0.204;
- ML003 *Spondias*: adult H_O ≈ -0.154; juvenile H_O ≈ -0.536; seed H_O ≈ -0.397; C ≈ -0.151;
- ML014 *Eucalyptus socialis*: mating support ≈ -0.897; family growth ≈ -0.056.

These patterns suggest buffering/lag hypotheses, but they were recognized after inspecting the data and are exploratory.

## Scale-independent direction

All **17/17** primary direct effects are negative on both the oriented g and oriented lnRR representations.

Therefore the primary direct stream contains no qualitative sign discordance between biological layers. This is descriptive only; effects are dependent within clusters and are not entered into a sign test.

The clearest genuine sign discordance remains outside the primary direct stream in *Eucalyptus wandoo*'s gradient representation, where interaction/pollen quantity is positive while reproductive function is negative.

## Statistical limitations of lnRR sensitivity

- independent units are often only n=2–3 per habitat group;
- delta-method normal approximations can be poor at such small n;
- exact lnRR cross-endpoint sampling covariance is unavailable;
- bounded metrics such as fruit set and heterozygosity are not guaranteed to have equivalent biological meaning per unit lnRR;
- lnRR is therefore a sensitivity scale, not a replacement truth.

## Manuscript consequence

The paper may claim that fragmentation responses are directionally consistent in the primary direct stream while **relative response amplitude is scale-sensitive**.

It may not currently claim a scale-independent global layer-separation syndrome or a scale-independent variable bottleneck ordering.

## Machine check

`scripts/check_estimand_scale_sensitivity.py` must pass before any renewed submission-ready state.
