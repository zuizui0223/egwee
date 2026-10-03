# Estimand-scale robustness audit — 2026-09-29

## Decision

The original primary headline based on equality of Hedges-g effects is **not estimand-scale robust**.

The five-cluster g analysis remains numerically correct, but its leave-one-cluster-out interpretation changes when the same positive-valued primary endpoints are represented as log response ratios (lnRR). Therefore the manuscript must not present `g`-scale non-robustness as a scale-general ecological result.

## Canonical Hedges-g result

- full Fisher p = **0.0121243261**;
- omit ML001 *Serapias* p = **0.1819435271**;
- ML001 cluster p = **0.0035453009**.

This is the previously frozen result.

## Post hoc lnRR reconstruction

For every positive-valued primary endpoint, lnRR is defined as:

`lnRR = orientation × ln(mean_fragmented / mean_reference)`

with delta-method sampling variance from independent fragmentation units. Pairwise covariance is reconstructed directly from aligned raw independent-unit values by the multivariate delta method. ML014 reads the same public TERN family table used by the existing recovery script.

### lnRR with raw-unit delta covariance

- full Fisher p = **1.1917e-12**;
- omit ML001 p = **8.3144e-05**.

Cluster p-values:

- ML001 = **1.1301e-10**;
- ML002 = **0.0226112**;
- ML003 = **0.00392567**;
- ML014 = **0.00117784**;
- ML020 = **0.938056**.

### lnRR with zero within-cluster covariance

- full Fisher p = **1.7228e-09**;
- omit ML001 p = **0.00434418**.

Thus the contrast with the g result is not created by the reconstructed lnRR covariance.

## Serapias scale reversal

On Hedges g:

- C pollen immigration = **-10.0990**;
- F fruit set = **-4.5541**;
- G adult H_O = **-26.0725**;
- absolute-magnitude order = **G > C > F**;
- C–F pair p = **0.00720**.

On lnRR:

- C pollen immigration = **-1.15673**;
- F fruit set = **-1.10219**;
- G adult H_O = **-0.65009**;
- absolute-magnitude order = **C > F > G**;
- C–F pair p = **0.63640**.

The extreme g magnitude of adult H_O is therefore primarily a standardized-dispersion phenomenon rather than a scale-general statement that the genetic response is biologically much stronger.

## Scale-invariant sign information

All **17/17** primary direct effects are negative on both g and lnRR orientation.

- g negative = 17;
- lnRR negative = 17;
- sign discordance between scales = 0.

Therefore the primary direct stream contains no scale-independent evidence of opposite response directions among layers. Its robust qualitative information is broad concordant deterioration, not direction reversal.

## Ecological implication

The direct five-cluster corpus supports the statement that fragmentation is detrimental across all admitted primary responses. It does **not** support a scale-general claim that within-system biological layers separate in magnitude or that the g-based Serapias influence pattern is the uniquely correct robustness conclusion.

Exploratory ratio-scale patterns may still generate biological hypotheses—for example stronger mating/connectivity loss than downstream performance in ML002 and ML014, or stronger juvenile than adult genetic loss in ML003—but these patterns were noticed after inspecting the data and must be labelled exploratory.

## Claim ceiling

Allowed:

- the g-scale equality test rejects in the full five-cluster corpus but fails after omitting ML001;
- the corresponding lnRR sensitivity rejects both in the full corpus and after omitting ML001;
- the g-based robustness conclusion is estimand-scale dependent;
- all 17 primary direct effects are detrimental on both scales;
- ML001 C–F separation and endpoint magnitude ordering are not scale robust.

Not allowed:

- scale-general state separation in the primary direct stream;
- a scale-general claim that ML001 uniquely drives layer non-exchangeability;
- interpreting Hedges-g magnitude order as biological severity order;
- treating post hoc lnRR as a replacement preregistered primary estimand;
- claiming a confirmed upstream→downstream attenuation law from the current direct corpus.

## Machine-readable implementation

- `scripts/check_estimand_scale_robustness.py`
- `evidence/meta_extraction/estimand_scale_robustness_v1.csv`

Dedicated CI workflow: `.github/workflows/estimand-scale-robustness.yml`.
