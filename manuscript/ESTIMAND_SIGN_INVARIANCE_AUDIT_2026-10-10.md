# Algebraic sign invariance is not a second robustness replication — 2026-10-10

## Audit question
What does “17/17 primary effects negative on oriented Hedges g and oriented lnRR” add beyond the signs of the underlying observed group-mean differences?

## Mathematical answer
For each strictly positive pair of group means, the oriented uncorrected estimators are
`g = o J (mean_fragmented - mean_reference) / pooled_SD` and
`lnRR = o log(mean_fragmented / mean_reference)`.
Here `o` is the predeclared biological direction (+1 or -1), `J>0` is the small-sample correction, and `pooled_SD>0`.
Because `log` is strictly increasing and both denominators are positive,
`sign(g) = sign(lnRR) = sign[o (mean_fragmented - mean_reference)]`.
This is an algebraic identity, not an empirical robustness test between independent effect-size estimates.

## Source-level check
`evidence/meta_extraction/estimand_scale_sensitivity_v1.csv` contains 17 source-summary effects in five independent programmes (ML001, ML002, ML003, ML014, ML020). All 34 group means are strictly positive (minimum 0.065), all group-unit counts exceed one, and all 17 observed g and oriented-lnRR values agree with the common oriented raw group-mean difference. Negative effects: g 17/17, lnRR 17/17; violations of the identity: 0/17.

The 17 negative **observed point estimates** are a substantive descriptive property of the admitted fragment/reference corpus. But the `17/17 across scales` count is not two independent replications, does not supply a cross-scale robustness p-value, and cannot measure ecological prevalence because effects are nested within only five programmes and studies were selected through a conditional admission protocol.

## What remains a genuine scale sensitivity
Effect magnitude, ordering, standardized difference tests, within-programme covariance-sensitive contrasts and leave-one-cluster inference **can** change between g and lnRR. In ML001 *Serapias*, G > C > F on |g| but C > F > G on |lnRR|; the C–F contrast is resolved on g and unresolved on lnRR. This is the nontrivial scale result.

## Guardrails
- In all prose, replace “independently robust signs across two scales” with “uniform oriented group-mean direction; sign concordance is guaranteed by the transformations for these positive means.”
- Keep endpoint uncertainty, study-level dependence, selective corpus admission and publication/source overlap explicit.
- The proof applies to uncorrected lnRR computed from the **same positive arithmetic group means** and a positive Hedges correction. It does not automatically apply to bias-corrected lnRR estimators, zero/negative means, transformations of individual observations before averaging, or separately estimated contrasts.
- Keep `submission_ready=false` and the frozen denominator intact; this note changes interpretation only, not source effects or Fisher statistics.

Source: `scripts/check_effect_scale_sign_logic.py`, cross-checking the existing 17-row estimand-scale sensitivity file. For lnRR estimation limitations see Lajeunesse (2015), *Ecology* 96:2056–2063, doi:10.1890/14-2402.1.
