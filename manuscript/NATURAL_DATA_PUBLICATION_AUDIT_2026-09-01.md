# Natural-data four-gate publication audit — 2026-09-01

## Decision

Treat the four locked natural-data lines as **one methodological empirical synthesis**, not four independent papers and not a pooled ecological meta-analysis.

The shared scientific object is the validity of a proposed ecological state measurement before residual habitat, origin, or history is interpreted. The four lines instantiate different locations at which that claim can fail:

1. residual context is redundant after an informative partial state;
2. a response-relevant contemporary coordinate is still missing;
3. a plausible biological proxy fails endpoint-relevant measurement adequacy;
4. preprocessing erases the mechanistic information that the richer measurement was intended to add.

The datasets remain separate demonstrations at their native holdout units. No common effect size, common ecological mechanism, or cross-origin coefficient is estimated.

## Why not four papers

### Line 1 alone

Honshu–Izu, Zurich, and Toronto provide a useful multi-system negative residual-context result, but the defensible claim is narrow: no detected transferable residual-context gain after each locked partial state. It does not establish state completeness. As a standalone paper it risks reading as a heterogeneous collection of null results.

### Line 2 alone

The *Oenothera harringtonii* result is a clean positive missing-coordinate case, with a 20.93% leave-one-maternal-plant-out MSE improvement and locked permutation `p=0.00130`. It is scientifically interpretable but is one system and one declared endpoint; by itself it is better used as the positive branch of a general measurement-gate framework.

### Line 3 alone

*Eschscholzia californica* and Mallorca carob are strong fail-closed examples because they preserve `not_identifiable`, metadata STOP, and proxy-adequacy failure rather than repairing the analysis after seeing the consequence. Their value is methodological governance across outcomes, not a shared biological effect.

### Line 4 alone

*Campanula americana* provides a particularly clear analytical mechanism: feature-wise standardisation made effective-transfer coordinates numerically identical to phase-visitation coordinates up to `8.88e-16`, erasing the efficiency multiplier. This is a strong representation warning but one case alone would support a technical note more naturally than a broad ecology paper.

Together, the four lines form a stronger argument because the same ordered decision tree produces positive, negative, non-identifiable, non-estimable, and STOP outcomes without changing endpoints after the fact.

## Why not a pooled synthesis

The programme does not identify one common ecological effect. Taxa, endpoints, biological coordinates, designs, and holdout units differ. Honshu–Izu and Zurich already demonstrate the key confounding problem for an origin-level synthesis: study, origin, protocol, taxa, and response construction are not separable. The locked `cross_origin_convergence_not_identifiable_from_existing_archives` decision therefore remains mandatory.

The synthesis is **logical and methodological**, not statistical pooling.

## Proposed paper thesis

> Before residual environmental or historical context is interpreted as evidence that an ecological state is incomplete, the state claim must pass separable gates for endpoint-relevant measurement adequacy and information-preserving representation. Natural datasets show that these gates yield empirically distinct outcomes: residual context can be redundant, a process coordinate can remain missing, a plausible proxy can fail adequacy, and preprocessing can erase a real mechanistic distinction.

A shorter operational formulation is:

> Test the state before interpreting the residual.

## Proposed manuscript architecture

### Introduction

Frame the common problem: ecological analyses often add geography, habitat, origin, or history after constructing a biological state proxy and interpret residual predictive gain as evidence for missing context. That interpretation is only valid if the proposed state measurement itself is endpoint-relevant and the analytical representation preserves the information it claims to add.

Do not motivate the paper through EGWE genetic-warning validity. The empirical programme must stand without the parent warning paper.

### Methods — four ordered gates

1. **Measurement gate:** does the candidate state/proxy improve the declared held-out endpoint under the frozen design?
2. **Representation gate:** does preprocessing preserve the mechanistic distinction between the richer measurement and the simpler proxy?
3. **Residual-context gate:** only after 1–2 pass, does residual habitat/origin/history add transferable held-out gain?
4. **Identifiability gate:** if designs or archives cannot separate origin/study/protocol, return `not_identifiable` or STOP rather than pool.

The existing four empirical lines map onto different branches of this ordered workflow; they are not four severity levels.

### Results

Present by inferential outcome rather than by organism:

1. **Residual context not supported after partial state:** Honshu–Izu, Zurich, Toronto.
2. **State incompleteness positively detected:** *Oenothera harringtonii*.
3. **Measurement adequacy not earned / endpoint not estimable:** *Eschscholzia californica*, Mallorca carob.
4. **Representation destroys added mechanism information:** *Campanula americana*.
5. **Cross-origin synthesis not identifiable:** retain the existing STOP.

### Discussion

The main contribution is not that one class of context variables matters or does not matter. It is that residual-context interpretation depends on upstream measurement and representation gates, and that a defensible workflow must preserve negative, unsupported, non-identifiable, and STOP outcomes rather than forcing every archive into one regression.

## Figure plan

### Figure 1 — four-gate decision tree

A state proxy enters the measurement gate. If it fails, residual context is not interpreted. If it passes, representation preservation is checked. Only then is residual context tested. Independent identifiability/access checks can terminate the branch with `not_identifiable`, `not_estimable`, or STOP.

### Figure 2 — empirical branch map

Place each natural system on the decision tree, with the locked outcome and holdout unit. This should replace any temptation to pool effect sizes.

### Figure 3 — held-out gain evidence

Display only commensurable within-study contrasts, separately faceted by system: Honshu–Izu, Zurich, Toronto, *Oenothera*, Mallorca. Do not put them on one common effect-size axis unless the scale is explicitly standardized within study and interpreted only as direction/gate outcome.

### Figure 4 — representation-collapse diagnostic

For *Campanula americana*, show the phase-visitation and effective-transfer coordinates before and after preprocessing, making the `8.88e-16` post-standardisation equivalence visually obvious.

## Claim ceilings

The paper may claim:

- the four gate outcomes are empirically distinguishable in existing natural datasets;
- residual-context inference is conditional on the adequacy and representation of the biological state supplied first;
- fail-closed outcomes are scientifically informative for deciding what may be interpreted next;
- preprocessing can make a biologically richer measurement analytically non-distinct.

The paper may not claim:

- one cross-system ecological effect or universal urban/island law;
- that distance, urbanisation, habitat, or pollinators are generally irrelevant;
- state completeness from a negative residual-context test;
- a common origin effect from the existing archives;
- predictive validity for the separate EGWE warning statistic;
- that a failed proxy implies the underlying biological process is irrelevant.

## Development gate

No new endpoint, source repair, proxy substitution, or post-result redefinition should be opened by default. Additional analysis is justified only if it strengthens the common four-gate manuscript without altering a frozen decision after seeing its result.

Highest-value remaining work:

1. create a single machine-readable table mapping system → proposed state → endpoint → holdout unit → gate reached → locked outcome → claim ceiling;
2. create the decision-tree figure from that table;
3. audit nearest methodological literature and current journal scope;
4. decide whether a journal requires a more explicit reusable algorithm/checklist than the current gate logic;
5. only then write the independent manuscript.

## Provisional venue logic

The natural package is best treated as an ecological measurement/indicator validity paper rather than a warning-statistic paper or a general theoretical-ecology paper. Final venue ranking should use current journal scopes and article requirements rather than historical assumptions.
