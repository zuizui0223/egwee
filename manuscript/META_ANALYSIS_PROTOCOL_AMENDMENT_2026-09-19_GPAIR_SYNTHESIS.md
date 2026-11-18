# Protocol amendment — five-programme G_adult−G_offspring synthesis

**Locked:** 2026-09-19 before the cross-programme pooled G-pair result is written to the evidence ledger.  
**Parent Phase-2 amendment:** `manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-18_SYSTEMATIC_COVERAGE_MODERATORS.md`

## 1. Trigger

The preregistered adult-versus-offspring cohort-lag gate opens when at least five independent same-exposure programme/study clusters contain both `G_adult` and `G_offspring`.

That gate is now met by exactly five independent programmes:

1. `ML003` — *Spondias purpurea*;
2. `P2_SF05_93` — *Parkia biglobosa*;
3. `P2_SF05_71` — *Heliconia acuminata*;
4. `P2_CF01_GPAIR_002` — Ethiopian *Prunus africana*;
5. `P2_CF01_GPAIR_003` — Kakamega *Prunus africana*.

This amendment opens only the prespecified `G_adult-G_offspring` pair synthesis. Moderator models remain closed until their independent-cluster gates are met.

## 2. Pair orientation

For every programme the primary contrast is:

`Delta_s = g(G_adult) - g(G_offspring)`.

Positive values mean the adult standing genetic response is more positive / less negative under fragmentation than the offspring response. Negative values mean the offspring response is more positive / less negative.

The synthesis tests a mean paired response difference. It does not test whether either cohort is itself harmed by fragmentation.

## 3. One independent contribution per programme

The primary denominator is the five independent programmes, not the number of developmental endpoints.

Four programmes have one co-primary offspring endpoint and contribute that covariance-aware pair contrast directly.

### 3.1 Spondias multi-cohort rule

`ML003` has two co-primary `G_offspring` endpoints declared before this synthesis:

- juvenile `H_O`;
- seed `H_O`.

Neither may be selected according to direction, magnitude, variance, or significance.

The primary ML003 programme contrast is the **equal-weight mean** of the two adult-minus-offspring contrasts:

`Delta_ML003 = 0.5 Delta_adult-juvenile + 0.5 Delta_adult-seed`.

Its sampling variance uses the full pairwise covariance already stored for adult, juvenile and seed endpoints:

`Cov(A-J, A-S) = Var(A) - Cov(A,J) - Cov(A,S) + Cov(J,S)`;

`Var(Delta_ML003) = 0.25[Var(A-J)+Var(A-S)+2Cov(A-J,A-S)]`.

Equal endpoint weights are used to preserve both co-primary developmental stages without precision-driven endpoint selection.

Juvenile-only and seed-only programme summaries are reported as sensitivity analyses, never as alternative primary specifications.

## 4. Five-programme random-effects model

After programme-level reduction there are exactly five independent contrast estimates `Delta_s` with sampling variances `v_s`.

Primary synthesis is an intercept-only random-effects meta-analysis:

`Delta_s = mu + u_s + e_s`;

`u_s ~ N(0,tau^2)`;

`e_s ~ N(0,v_s)`.

### 4.1 Heterogeneity estimator

`tau^2` is estimated by restricted maximum likelihood (REML), constrained to `tau^2 >= 0`. A boundary estimate of zero is valid and is not replaced by a positive value.

The REML objective is evaluated on the programme-level effects only.

### 4.2 Primary uncertainty

Because the gate opens at only `K=5` independent programmes, the primary confidence interval uses a modified Knapp–Hartung small-sample correction.

With REML weights `w_s = 1/(v_s + tau^2)`:

`mu_hat = sum(w_s Delta_s) / sum(w_s)`;

`q = sum[w_s(Delta_s-mu_hat)^2]/(K-1)`;

`q_star = max(1,q)`;

`SE_mKH = sqrt(q_star / sum(w_s))`.

The primary 95% interval uses Student `t` with `K-1 = 4` degrees of freedom.

The unmodified model-based normal interval is retained as a sensitivity result and cannot replace the mKH interval because it is narrower.

## 5. Descriptive heterogeneity

Report:
- REML `tau^2`;
- Cochran `Q` under the fitted programme weights / boundary fixed-effect equivalent when `tau^2=0`;
- descriptive `I^2 = max(0, (Q-(K-1))/Q)` when `Q>0`.

With only five programmes these heterogeneity quantities are descriptive and are not used to open moderators.

## 6. Influence and endpoint sensitivity

The following are required before a cohort-lag interpretation:

1. leave-one-programme-out pooled point estimates for all five programmes;
2. ML003 juvenile-only synthesis;
3. ML003 seed-only synthesis;
4. comparison of the primary mKH interval with the model-based normal interval.

No sensitivity result is allowed to replace the primary equal-weight ML003 specification.

## 7. Claim rule

A directional cross-programme cohort-lag claim requires the primary mKH 95% interval for `mu` to exclude zero.

If it includes zero, the correct result is:

> five independent programmes are sufficient to estimate the adult-versus-offspring response difference, but the current synthesis does not resolve a common directional cohort lag.

A nonsignificant or zero-crossing result is not evidence that adult and offspring responses are biologically exchangeable.

## 8. Relation to the frozen manuscript

Opening this pair-specific estimate does not change any Phase-1 effect, Fisher statistic, covariance sensitivity, or claim ceiling.

The expanded Phase-2 manuscript may supersede the frozen Journal of Ecology baseline only after the separate systematic search-completion gate is also satisfied. Reaching 5/5 in one pair family alone is insufficient for supersession.
