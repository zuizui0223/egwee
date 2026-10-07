# SF06 publication-LOO probabilistic sign-sentinel audit — 2026-10-07

## Status

Post-exposure exploratory diagnostic. This is not part of the preregistered SF06 inferential test and is not used to redefine the primary topology.

## Question

The corrected SF06 sign table shows zero improvement in deterministic 0/1 classification beyond the fragmentation-context baseline.

Because that result depends on a decision threshold, we also ask a probability-calibration question:

> When a whole source publication is held out, does pollination sign improve the predicted probability that female fitness is lower?

## Procedure

For each held-out source publication:

1. estimate the baseline probability of `F lower` from all remaining fragmentation pairs;
2. estimate separate probabilities `P(F lower | I lower)` and `P(F lower | I nonlower)` from the remaining pairs;
3. predict the held-out publication;
4. compare Brier score and log loss.

To avoid unstable zero/one probabilities in sparse sign states, the primary audit uses Laplace smoothing (+1 success and +1 failure). A Jeffreys-smoothed (+0.5/+0.5) sensitivity is also reported.

## Full habitat-fragmentation public-S1 subset

### Laplace smoothing

Row-weighted held-publication prediction:

- baseline Brier = **0.17421**;
- pollination-sign Brier = **0.17811**;
- relative Brier change = **+2.24%** (worse);
- baseline log loss = **0.53508**;
- pollination-sign log loss = **0.54348**;
- relative log-loss change = **+1.57%** (worse).

Publication-balanced averages show the same direction:

- Brier: 0.16432 → 0.17055;
- log loss: 0.51406 → 0.52775.

### Jeffreys smoothing

The result remains worse with pollination sign:

- row-weighted Brier: 0.17430 → 0.17866;
- row-weighted log loss: 0.53550 → 0.54554.

## Source-publication-disjoint subset

The source-disjoint external subset gives an even stronger lack of probabilistic gain.

### Laplace smoothing

- row-weighted Brier: **0.17875 → 0.18897** (+5.71%);
- row-weighted log loss: **0.54768 → 0.57476** (+4.95%);
- publication-balanced Brier: 0.18062 → 0.19224;
- publication-balanced log loss: 0.55337 → 0.58460.

### Jeffreys smoothing

- row-weighted Brier: 0.17874 → 0.19002;
- row-weighted log loss: 0.54829 → 0.58555.

## Interpretation

The external result is therefore stronger than a threshold artefact.

Pollination sign:

- does not reduce deterministic sign-classification errors;
- does not improve held-publication probabilistic prediction under either smoothing rule;
- nevertheless coexists with a statistically positive continuous association between pollination and female-fitness Hedges d.

The empirical distinction is:

> **association is not the same thing as incremental sentinel information.**

A process can be a genuine population-level correlate of function without improving diagnosis of function in a new study once the high baseline risk associated with fragmentation is already known.

## Claim ceiling

Allowed:

- pollination sign fails to improve held-publication probability prediction in this public-S1 subset under two prespecified smoothing conventions reported together;
- the probability audit supports the association-versus-sentinel distinction.

Not allowed:

- this post hoc audit is confirmatory;
- the scores estimate operational field-monitoring performance in an external target population;
- pollination has zero causal importance;
- the result justifies discarding pollination measurements.
