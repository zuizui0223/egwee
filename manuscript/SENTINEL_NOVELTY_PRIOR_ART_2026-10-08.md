# Novelty boundary: pollen-limitation inference versus sentinel sufficiency — 2026-10-08

## Nearest ecological precedents

### Aguilar et al. 2006 — aggregate coupling supports a pollen-limitation explanation

The early fragmentation meta-analysis found negative mean effects on pollination and plant reproduction and an association between their fragmentation effect sizes. Its interpretation was that pollen limitation could be an important proximate contributor to reproductive loss.

Aguilar et al. 2025 (Annals of Botany 135:57–70, doi:10.1093/aob/mcae076) reaffirm positive aggregate pollination–female-fitness coupling (published r=0.421, n=82 simultaneous species). Neither an aggregate correlation nor a positive conditional coefficient alone establishes that pollination response **identifies the reproductive condition of a particular fragmented population**.

Source: Aguilar et al. 2006, Ecology Letters, doi:10.1111/j.1461-0248.2006.00927.x.

### Lázaro et al. 2020 — local visit–seed pathways already fail

A landscape-fragmentation SEM across 24 Norwegian habitat fragments and four abundant plant species found no direct visitation-rate→reproductive-success link for those species. Several landscape variables affected seed production directly, with marked differences among species.

Therefore EGWEE must **not** claim to be the first demonstration that visitation and seed production decouple under fragmentation.

Source: Lázaro et al. 2020, Ecological Applications, doi:10.1002/eap.2099.

### Landscape-scale pollination studies — habitat can influence reproduction beyond visitation

In landscape-scale experimental pollination research on cherry trees, visitation responded to local and landscape context while fruit set depended on isolation and heterospecific floral density rather than directly on visit rate. This shows that a one-path fragmentation→visitation→fitness picture was already inadequate.

Source: Disentangling multiple drivers of pollination in a landscape-scale experiment, PMC3843845.

### Pollen quantity, pollen quality and resources are established concepts

Aizen & Harder (2007), Ecology, doi:10.1890/06-1017, explicitly distinguished quantity- and quality-limitation. Knight et al. (2005), Annual Review of Ecology, Evolution, and Systematics, doi:10.1146/annurev.ecolsys.36.102403.115320, treated ecological and historical constraints on pollen limitation. The broad idea of reproduction limited by non-substitutable pollen and resources has a long history.

Thus the Q×P×V / reproductive-assurance bookkeeping used in EGWEE is **not a new causal theory**.

## What EGWEE adds beyond those precedents

1. A frozen matched-programme empirical accounting distinguishes three representation-stable resolved **downstream false-reassurance** cases from exploratory sign geometry and from standardized-effect ranking artifacts.
2. The external Aguilar public-S1 reanalysis asks a **different estimand** from the source paper's positive mean correlation: can a pollination-effect sign identify female-fitness-effect sign? Corrected constituent consensus is many-to-many (12 mismatches/54), and remains so in a source-publication-disjoint subset (7/31).
3. In the same external subset, the **best binary lookup provides no improvement over the majority-state baseline** at F<0. This does not mean no information: the in-sample empirical mutual information is positive (0.00543 bits/pair).
4. More stringent held-publication and held-species tests with a simple sign-conditional probability model worsen Brier and log-loss scores relative to a baseline using only the training-set F-state frequency, for both complete and source-disjoint public-S1 subsets. Continuous d_I still has a small out-of-publication MSE improvement (~2–4%), and post hoc severity thresholds sometimes have meaningful AUC, so the result is **insufficiency, not ecological irrelevance**.
5. The biological counterexamples suggest at least two distinct routes under fragmentation: altered compatible transfer or selective filtering within pollination/mating; and a parallel downstream failure such as seed dispersal or survival. Current mixed evidence does not quantify the causal contribution of these routes.

The empirical contribution is therefore a fragmentation-specific test of **incremental sentinel value across studies**, not the discovery that interaction quality, resources or multiple pathways exist.


### 17 October 2026: same-case numeric/directional target audit

To prevent conflating **predictor representation**, **outcome target**, and **different eligible cohort denominators**, [the 17 October SF06 source-heldout audit](SF06_MATCHED_TARGET_REPRESENTATION_TRANSFER_2026-10-17.md) keeps identical 54 constituent-sign-consensus pairs (32 publications) for numeric-female and point-sign-female targets; its 31-pair / 23-publication comparison excludes all publications overlapping the primary EGWEE matched I–F map.

- On **continuous female effect `d_F`** (held-publication MSE), direction-only and continuous `d_I` have small and **source-frame-dependent** improvements: on all 54, intercept 0.462895, sign 0.446734, numeric `d_I` 0.452495; on source-disjoint 31, intercept 0.623925, sign **worse** at 0.657612, numeric **slightly better** at 0.614103.
- On the **binary F lower/nonlower point-sign** (held-publication Brier), neither representation beats the baseline in either frame: full baseline 0.176739, sign 0.181503, continuous predictor 0.177584; disjoint baseline 0.183269, sign 0.193949, continuous predictor 0.190088.
- The numeric comparison is **exactly case-matched** to the sign-predictor comparison; it must not be conflated with the separate 55 numerically eligible fragmentation pairs, 49 SI/SC-known pairs or 26 source-disjoint SI/SC-known pairs. All sign targets are **point consensus, not 95%-resolved female outcomes**; only three source pairs are jointly 95%-resolved at both margins.

The resulting ecological statement is **not** that female reproductive fitness is independent of pollination, that binarization always loses information, or that one biological predictor is universally best. Rather, coarse quantity-based sentinels exhibit **outcome-target and source-population-dependent conditional diagnostic performance** under the simple held-source models. This is a *practical prediction estimand*, not yet an identified causal mechanism or universal species-level law.

## What this does not establish

- Zero true conditional information, or the failure of every possible nonlinear/probabilistic predictor.
- A random-sample prevalence of field monitoring errors: SF06 is a selected literature subset and only 3 pairs have both marginal endpoint directions resolved at 95%.
- Site/year synchronized I→F causation: SF06 pairs publication × species × land-use rather than verifying coincident sites and years.
- Confirmation that any one mechanistic pathway explains all three EGWEE false-reassurance anchors.
- That earlier research did not separately demonstrate these phenomena.

## More informative forward biological question

> **Under what ecological conditions does fragmentation shift the limiting stage of reproduction without an equivalent shift in observed pollination quantity?**

The next genuinely discriminating comparison is synchronized measurement of visit/pollen quantity, donor provenance/compatibility, embryo survival and final recruitment in the same sites and reproductive episode, paired with source-specific ecological routes (selfing, dispersal, resources). A gain in causal knowledge would come from predicting *which pathway fails where*, not merely from showing another mismatched sign.
