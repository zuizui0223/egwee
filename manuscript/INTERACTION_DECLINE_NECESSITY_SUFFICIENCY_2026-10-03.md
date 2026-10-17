# Interaction decline is neither necessary nor sufficient for reproductive decline — frozen evidence audit

## Question

Within the frozen matched fragmentation evidence universe, does an observed decline in interaction/pollen quantity uniquely diagnose an observed decline in reproductive function?

## Result

No. At the level of source-supported qualitative evidence states, interaction decline is **neither necessary nor sufficient** for reproductive decline.

### Not necessary

Reproductive decline occurs without an observed interaction decline in at least two independent programmes:

- *Eucalyptus wandoo* (quantitative): interaction/pollen-tube response is higher while seed production is lower;
- Hulting five-species fragmentation experiment (qualitative blocked): no detected pollination-rate edge/connectivity effect while seed production is lower near edges in four of five species.

Thus reproductive decline can occur even when the monitored interaction quantity does not decline.

### Not sufficient

Interaction decline occurs without an observed reproductive decline in at least three independent programmes:

- Toronto common milkweed (quantitative point state): pollinator abundance is lower while the reproductive-function point estimate is higher;
- *Haloxylon ammodendron* (qualitative blocked): insect visitation is lower while natural seed set is not detectably lower;
- *Caragana korshinskii* (qualitative blocked): pollinator activity is lower while the open-pollinated seed-set habitat effect is not detected.

Thus interaction decline does not uniquely imply reproductive decline.

## Leave-one-programme-out robustness

The two logical failures survive deletion of every single programme in the frozen 16-programme mixed-tier map: after any one deletion, at least one not-necessary counterexample and one not-sufficient counterexample remain.

This robustness applies to **existence in the mixed quantitative + source-explicit qualitative evidence universe**, not to a homogeneous quantitative meta-analysis.

Within the quantitative eight-programme tier alone, each logical direction has only one clean programme-level state counterexample (Wandoo for not-necessary; milkweed for not-sufficient), so quantitative-tier leave-one-out robustness is not claimed.

## Ecological interpretation

> **Observed interaction decline is neither a necessary nor a sufficient condition for observed reproductive decline under fragmentation in the frozen evidence universe.**

This explains why average positive pollination–reproduction coupling can coexist with misleading programme-level monitoring signals.

It also gives two management error modes:

- false reassurance: interaction appears intact while reproduction declines;
- apparent over-warning: interaction declines while reproduction is retained or not detectably lower.

## Claim ceiling

Allowed:

- mixed-tier existence of both logical counterexample classes;
- leave-one-programme-out robustness of their existence in the frozen 16-programme map;
- interaction quantity alone is insufficient as a stand-alone functional sentinel;
- multi-stage monitoring is needed when reproductive function is the target.

Not allowed:

- frequencies of the counterexample classes estimate ecological prevalence;
- qualitative blocked studies are quantitative replications;
- no-detected-loss is a true zero effect;
- pollinator monitoring has no conservation value;
- all interaction measures fail equally or all systems share one mechanism.

## Machine-readable implementation

- `evidence/meta_extraction/if_translation_map_v1.csv`
- `scripts/check_interaction_decline_necessity_sufficiency.py`
